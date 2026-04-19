import asyncio
import json

from agentService.agent.attraction_search_agent import AttractionSearchAgent
from agentService.agent.hotel_search_agent import HotelSearchAgent
from agentService.agent.itinerary_planner_agent import ItineraryPlannerAgent
from agentService.agent.meal_search_agent import MealSearchAgent
from agentService.agent.trip_orchestrator_agent import TripOrchestratorAgent
from agentService.agent.weather_search_agent import WeatherSearchAgent
from agentService.entity.trip_workflow_context import TripWorkflowContext
from agentService.tools.AmapTool import amap_search, amap_weather_search
from agentService.entity.BasicClass import (
    TripRequest,
)

PLACE_TOOLS = [amap_search]
WEATHER_TOOLS = [amap_weather_search]
ALL_TOOLS = [amap_search, amap_weather_search]


def _build_sample_request() -> TripRequest:
    """构造统一的测试请求。

    返回值:
        TripRequest: 用于单独测试各智能体的示例请求。
    """
    return TripRequest(
        city="上海",
        start_date="2026-04-19",
        end_date= "2026-04-20",
        preference="历史文化、自然景观，科技企业，大学",
        accommodation="经济型酒店，交通便利",
        transportation="地铁+步行",
        budget=3000,
        user_input="希望有适合亲子游的景点，最好有博物馆或科技馆",

    )




def _build_sample_context(request: TripRequest) -> TripWorkflowContext:
    """构造规划 Agent 使用的测试上下文。

    参数:
        request: 测试请求对象。

    返回值:
        TripWorkflowContext: 带有示例搜索结果的共享上下文。
    """
    context = TripWorkflowContext(request=request)
    attraction_result = {
        "attractions": [
            {
                "name": "外滩",
                "address": "上海市黄浦区中山东一路",
                "location": {"longitude": 121.4903, "latitude": 31.2410},
                "visit_duration": 120,
                "description": "黄浦江畔经典城市地标，适合傍晚观景和拍照。",
                "category": "城市观光",
                "rating": 4.9,
                "ticket_price": 0,
            },
            {
                "name": "豫园",
                "address": "上海市黄浦区豫园老街",
                "location": {"longitude": 121.4926, "latitude": 31.2271},
                "visit_duration": 180,
                "description": "江南园林代表，适合感受老上海历史文化氛围。",
                "category": "博物馆",
                "rating": 4.8,
                "ticket_price": 30,
            },
            {
                "name": "上海博物馆",
                "address": "上海市黄浦区人民大道201号",
                "location": {"longitude": 121.4737, "latitude": 31.2304},
                "visit_duration": 180,
                "description": "馆藏体系完整，适合了解中国古代艺术与历史。",
                "category": "历史文化",
                "rating": 4.8,
                "ticket_price": 0,
            },
        ],
        "message": "已优先筛选上海城市观光与历史文化类景点。",
    }
    weather_result = {
        "weather_info": [
            {
                "date": "2026-04-16",
                "day_weather": "晴",
                "night_weather": "多云",
                "day_temp": 22,
                "night_temp": 16,
                "wind_direction": "东南风",
                "wind_power": "3级",
            },
            {
                "date": "2026-04-17",
                "day_weather": "多云",
                "night_weather": "晴",
                "day_temp": 24,
                "night_temp": 17,
                "wind_direction": "东风",
                "wind_power": "2级",
            },
        ],
        "message": "上海两天以晴到多云为主，适合城市步行游览，建议带轻薄外套。",
    }
    hotel_result = {
        "hotels": [
            {
                "name": "上海外滩华尔道夫酒店",
                "address": "上海市黄浦区中山东一路2号",
                "location": {"longitude": 121.4913, "latitude": 31.2408},
                "price_range": "1800-2600元/晚",
                "rating": "4.7",
                "distance": "距外滩步行可达",
                "type": "高档酒店",
                "estimated_cost": 2200,
            },
            {
                "name": "上海南京路智选假日酒店",
                "address": "上海市黄浦区福建中路",
                "location": {"longitude": 121.4819, "latitude": 31.2368},
                "price_range": "700-1100元/晚",
                "rating": "4.6",
                "distance": "距南京路步行街较近",
                "type": "精品酒店",
                "estimated_cost": 900,
            },
        ],
        "message": "已按预算和市中心、地铁便利的偏好筛选上海酒店。",
    }
    meals_result = {
        "meals": [
            {"type": "breakfast", "name": "沈大成", "estimated_cost": 30},
            {"type": "lunch", "name": "南翔馒头店", "estimated_cost": 80},
            {"type": "dinner", "name": "老饭店本帮菜", "estimated_cost": 180},
            {"type": "snack", "name": "大壶春生煎", "estimated_cost": 25},
        ],
        "message": "已优先覆盖上海本地早餐、午餐、晚餐与小吃场景。",
    }
    context.save_search_results(
        attraction_result=json.dumps(attraction_result, ensure_ascii=False),
        weather_result=json.dumps(weather_result, ensure_ascii=False),
        hotel_result=json.dumps(hotel_result, ensure_ascii=False),
        meals_result=json.dumps(meals_result, ensure_ascii=False),
    )
    return context




async def test_attraction_search() -> None:
    """测试景点搜索智能体并打印最终输出。

    返回值:
        None
    """
    request = _build_sample_request()
    agent = AttractionSearchAgent(tools=PLACE_TOOLS)
    result = await agent.ainvoke(request)
    print("[ATTRACTION_RESULT]", result)


async def test_hotel_search() -> None:
    """测试酒店搜索智能体并打印最终输出。

    返回值:
        None
    """
    request = _build_sample_request()
    agent = HotelSearchAgent(tools=PLACE_TOOLS)
    result = await agent.ainvoke(request)
    # print("[HOTEL_RESULT]", result)


async def test_meal_search() -> None:
    """测试餐饮搜索智能体并打印最终输出。

    返回值:
        None
    """
    request = _build_sample_request()
    agent = MealSearchAgent(tools=PLACE_TOOLS)
    result = await agent.ainvoke(request)
    # print("[MEAL_RESULT]", result)


async def test_weather_search() -> None:
    """测试天气搜索智能体并打印最终输出。

    返回值:
        None
    """
    request = _build_sample_request()
    agent = WeatherSearchAgent(tools=WEATHER_TOOLS)
    result = await agent.ainvoke(request)
    # print("[WEATHER_RESULT]", result)


async def test_itinerary_planner() -> None:
    """使用模拟上下文测试行程规划智能体。"""
    request = _build_sample_request()
    context = _build_sample_context(request)
    agent = ItineraryPlannerAgent()
    result = await agent.ainvoke(context)
    print("[PLAN_RESULT]", result.model_dump())


async def test_trip_orchestrator() -> None:
    """用真实请求、真实工具和总编排 Agent 跑完整链路。"""
    request = _build_sample_request()
    agent = TripOrchestratorAgent(tools=ALL_TOOLS)
    result = await asyncio.wait_for(agent.ainvoke(request), timeout=600)
    print("[ORCHESTRATOR_RESULT]", result.model_dump())


def test_amap_search() -> None:
    """测试高德地点查询工具并打印返回值。

    返回值:
        None
    """
    result = amap_search.invoke(
        {
            "keywords": "景点",
            "region": "北京市",
            "page_size": 10,
        }
    )
    print("[AMAP]", result)


def test_amap_weather_search() -> None:
    """测试高德天气查询工具并打印返回值。

    返回值:
        None
    """
    result = amap_weather_search.invoke(
        {
            "city": "北京",
        }
    )
    # print("[AMAP_WEATHER]", result)



async def main() -> None:
    """程序入口，并发执行各智能体独立测试。

    返回值:
        None
    """
    return test_amap_search()


if __name__ == "__main__":
    asyncio.run(main())
