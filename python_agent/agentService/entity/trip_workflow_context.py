"""旅行编排共享上下文：在多个智能体之间传递关键结果。"""

from __future__ import annotations

from pydantic import BaseModel, Field

from agentService.entity.BasicClass import (
    AttractionSearchResponse,
    HotelSearchResponse,
    MealSearchResponse,
    TripRequest,
    WeatherSearchResponse,
)


class TripWorkflowContext(BaseModel):
    """共享上下文数据。

    说明：
    - 景点结果保存为完整的搜索响应对象，以匹配当前景点智能体输出；
    - 天气、酒店、餐饮结果也保存为完整的搜索响应对象，便于统一携带 message。
    """

    request: TripRequest = Field(..., description="用户原始旅行请求")
    attraction_response: AttractionSearchResponse = Field(default_factory=AttractionSearchResponse, description="景点搜索响应")
    weather_response: WeatherSearchResponse = Field(default_factory=WeatherSearchResponse, description="天气搜索响应")
    hotel_response: HotelSearchResponse = Field(default_factory=HotelSearchResponse, description="酒店搜索响应")
    meals_response: MealSearchResponse = Field(default_factory=MealSearchResponse, description="餐饮搜索响应")


    def save_search_results(
        self,
        attraction_result: AttractionSearchResponse,
        weather_result: WeatherSearchResponse,
        hotel_result: HotelSearchResponse,
        meals_result: MealSearchResponse,
    ) -> None:
        """写入四个搜索智能体的结果。

        参数:
            attraction_result: 景点搜索结构化结果。
            weather_result: 天气搜索结构化结果。
            hotel_result: 酒店搜索结构化结果。
            meals_result: 餐饮搜索结构化结果。

        返回值:
            None
        """
        self.attraction_response = attraction_result
        self.weather_response = weather_result
        self.hotel_response = hotel_result
        self.meals_response = meals_result
