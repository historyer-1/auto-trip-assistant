"""行程计划格式化兜底器。"""

from __future__ import annotations

import json

from json_repair import repair_json

from agentService.entity.BasicClass import Attraction, Budget, DayPlan, Hotel, Meal, TripPlan, WeatherInfo


class TripPlanFormatter:
    """将非标准行程 JSON 规整为 TripPlan。"""

    def format(self, raw_content: str) -> TripPlan:
        """把模型原始输出整理成 TripPlan。

        参数:
            raw_content: 模型返回的原始文本内容。

        返回值:
            TripPlan: 结构化行程计划对象。
        """
        # 优先直接解析完整 JSON，失败后只保留首尾大括号之间的内容。
        payload = self._load_json_payload(raw_content)

        # 按 TripPlan 结构做最小字段规整，避免模型把字段名写偏。
        days_payload = payload.get("days", [])
        weather_payload = payload.get("weather_info", [])
        if not isinstance(days_payload, list):
            days_payload = []
        if not isinstance(weather_payload, list):
            weather_payload = []
        days = [self._build_day_plan(day, index) for index, day in enumerate(days_payload) if isinstance(day, dict)]
        weather_info = [self._build_weather_info(item) for item in weather_payload if isinstance(item, dict)]

        budget_payload = payload.get("budget")
        budget = Budget.model_validate(budget_payload) if isinstance(budget_payload, dict) else None

        return TripPlan.model_validate(
            {
                "city": payload.get("city", ""),
                "start_date": payload.get("start_date", ""),
                "end_date": payload.get("end_date", ""),
                "days": days,
                "weather_info": weather_info,
                "overall_suggestions": payload.get("overall_suggestions", ""),
                "budget": budget,
            }
        )

    def _load_json_payload(self, raw_content: str) -> dict:
        """从原始文本中提取 JSON 对象。

        参数:
            raw_content: 模型返回的原始文本。

        返回值:
            dict: 解析后的 JSON 对象。
        """
        cleaned_content = self._strip_code_fences(raw_content)
        try:
            payload = json.loads(cleaned_content)
        except json.JSONDecodeError as first_error:
            start = cleaned_content.find("{")
            end = cleaned_content.rfind("}")
            if start < 0 or end <= start:
                raise
            json_text = cleaned_content[start : end + 1]
            try:
                payload = json.loads(json_text)
            except json.JSONDecodeError:
                if repair_json is None:
                    raise first_error
                # 使用 json-repair 直接返回对象，避免修复后再次 loads 失败。
                payload = repair_json(
                    json_text,
                    return_objects=True,
                    skip_json_loads=True,
                )

        if not isinstance(payload, dict):
            raise ValueError("行程规划结果必须是 JSON 对象")

        return payload

    def _strip_code_fences(self, raw_content: str) -> str:
        """移除模型可能附带的代码块标记。

        参数:
            raw_content: 模型返回的原始文本。

        返回值:
            str: 去除代码块标记后的文本。
        """
        content = raw_content.strip()
        if content.startswith("```"):
            first_newline = content.find("\n")
            if first_newline >= 0:
                content = content[first_newline + 1 :]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()

    def _build_day_plan(self, day: dict, index: int) -> DayPlan:
        """规整单日行程字段。

        参数:
            day: 单日行程原始数据。
            index: 当前天序号。

        返回值:
            DayPlan: 规整后的单日行程。
        """
        attractions_payload = day.get("attractions", [])
        meals_payload = day.get("meals", [])
        if not isinstance(attractions_payload, list):
            attractions_payload = []
        if not isinstance(meals_payload, list):
            meals_payload = []

        attractions = [self._build_attraction(item) for item in attractions_payload if isinstance(item, dict)]
        meals = [self._build_meal(item) for item in meals_payload if isinstance(item, dict)]

        attraction1_payload = day.get("attractions1")
        attraction2_payload = day.get("attractions2")
        lunch_payload = day.get("lunch")
        dinner_payload = day.get("dinner")

        if isinstance(attraction1_payload, dict):
            attractions.insert(0, self._build_attraction(attraction1_payload))
        if isinstance(attraction2_payload, dict):
            attractions.append(self._build_attraction(attraction2_payload))

        if isinstance(lunch_payload, dict):
            meals.insert(0, self._build_meal(lunch_payload))
        if isinstance(dinner_payload, dict):
            meals.append(self._build_meal(dinner_payload))

        attractions = self._dedupe_attractions(attractions)
        meals = self._dedupe_meals(meals)
        hotel_payload = day.get("hotel")
        hotel = self._build_hotel(hotel_payload) if isinstance(hotel_payload, dict) else None

        return DayPlan.model_validate(
            {
                "date": day.get("date", ""),
                "day_index": day.get("day_index", index),
                "description": day.get("description") or day.get("summary") or day.get("weather") or f"第{index + 1}天行程",
                "transportation": day.get("transportation") or "根据实际情况安排",
                "accommodation": day.get("accommodation") or "按酒店入住安排",
                "hotel": hotel,
                "attractions": attractions,
                "meals": meals,
            }
        )

    def _dedupe_attractions(self, attractions: list[Attraction]) -> list[Attraction]:
        """按名称+地址去重景点，避免新旧字段同时存在时重复。"""
        seen: set[tuple[str, str]] = set()
        result: list[Attraction] = []
        for attraction in attractions:
            key = (attraction.name.strip(), attraction.address.strip())
            if key in seen:
                continue
            seen.add(key)
            result.append(attraction)
        return result

    def _dedupe_meals(self, meals: list[Meal]) -> list[Meal]:
        """按类型+名称+地址去重餐饮，避免新旧字段同时存在时重复。"""
        seen: set[tuple[str, str, str]] = set()
        result: list[Meal] = []
        for meal in meals:
            key = (meal.type.strip().lower(), meal.name.strip(), (meal.address or "").strip())
            if key in seen:
                continue
            seen.add(key)
            result.append(meal)
        return result

    def _build_attraction(self, attraction: dict) -> Attraction:
        """规整单条景点信息。

        参数:
            attraction: 单条景点原始数据。

        返回值:
            Attraction: 规整后的景点信息。
        """
        return Attraction.model_validate(
            {
                "name": attraction.get("name") or attraction.get("title") or "景点",
                "address": attraction.get("address") or "",
                "location": self._build_location(attraction.get("location")),
                "visit_duration": attraction.get("visit_duration") or attraction.get("duration") or 60,
                "description": attraction.get("description") or attraction.get("note") or "",
                "category": attraction.get("category") or "景点",
                "rating": attraction.get("rating"),
                "image_url": attraction.get("image_url"),
                "ticket_price": attraction.get("ticket_price") or attraction.get("price") or 0,
            }
        )

    def _build_hotel(self, hotel: dict) -> Hotel:
        """规整单条酒店信息。

        参数:
            hotel: 单条酒店原始数据。

        返回值:
            Hotel: 规整后的酒店信息。
        """
        return Hotel.model_validate(
            {
                "name": hotel.get("name") or hotel.get("title") or "酒店",
                "address": hotel.get("address") or "",
                "location": self._build_location(hotel.get("location")),
                "price_range": hotel.get("price_range") or hotel.get("price") or "",
                "rating": hotel.get("rating") or "",
                "distance": hotel.get("distance") or "",
                "type": hotel.get("type") or hotel.get("category") or "",
                "estimated_cost": hotel.get("estimated_cost") or hotel.get("cost") or 0,
            }
        )

    def _build_location(self, location: object) -> dict | None:
        """规整经纬度坐标。

        参数:
            location: 原始坐标对象。

        返回值:
            dict | None: 可被 Location 模型识别的坐标字典，无法识别时返回 None。
        """
        if not isinstance(location, dict):
            return None

        longitude = location.get("longitude", location.get("lng", location.get("lon")))
        latitude = location.get("latitude", location.get("lat"))

        if longitude is None or latitude is None:
            return None

        try:
            longitude_value = float(longitude)
            latitude_value = float(latitude)
        except (TypeError, ValueError):
            return None

        return {
            "longitude": longitude_value,
            "latitude": latitude_value,
        }

    def _build_meal(self, meal: dict) -> Meal:
        """规整单条餐饮信息。

        参数:
            meal: 单条餐饮原始数据。

        返回值:
            Meal: 规整后的餐饮信息。
        """
        meal_type = str(meal.get("type") or meal.get("meal_type") or "").strip()
        name = str(meal.get("name") or meal_type or "餐食安排").strip()

        return Meal.model_validate(
            {
                "type": meal_type or "breakfast",
                "name": name,
                "address": meal.get("address") or "",
                "location": self._build_location(meal.get("location")),
                "description": meal.get("description") or meal.get("note") or "",
                "estimated_cost": meal.get("estimated_cost") or meal.get("cost") or 0,
            }
        )

    def _build_weather_info(self, weather: dict) -> WeatherInfo:
        """规整单日天气字段。

        参数:
            weather: 单日天气原始数据。

        返回值:
            WeatherInfo: 规整后的天气信息。
        """
        return WeatherInfo.model_validate(
            {
                "date": weather.get("date", ""),
                "day_weather": weather.get("day_weather") or weather.get("weather") or weather.get("day") or "",
                "night_weather": weather.get("night_weather") or weather.get("night") or weather.get("weather") or "",
                "day_temp": weather.get("day_temp") or weather.get("temperature") or 0,
                "night_temp": weather.get("night_temp") or weather.get("temperature") or 0,
                "wind_direction": weather.get("wind_direction") or "",
                "wind_power": weather.get("wind_power") or "",
            }
        )