import asyncio

from agentService.agent.attraction_search_agent import AttractionSearchAgent
from agentService.agent.hotel_search_agent import HotelSearchAgent
from agentService.agent.itinerary_planner_agent import ItineraryPlannerAgent
from agentService.agent.meal_search_agent import MealSearchAgent
from agentService.agent.weather_search_agent import WeatherSearchAgent
from agentService.entity.trip_workflow_context import TripWorkflowContext
from agentService.tools.AmapTool import amap_search, amap_weather_search
from agentService.entity.BasicClass import (
    Attraction,
    AttractionSearchResponse,
    Hotel,
    HotelSearchResponse,
    Location,
    Meal,
    MealSearchResponse,
    TripRequest,
    WeatherInfo,
    WeatherSearchResponse,
)

PLACE_TOOLS = [amap_search]
WEATHER_TOOLS = [amap_weather_search]


def _build_sample_request() -> TripRequest:
    """构造统一的测试请求。

    返回值:
        TripRequest: 用于单独测试各智能体的示例请求。
    """
    return TripRequest(
        city="北京",
        start_date="2026-04-15",
        end_date="2026-04-16",
        preference="历史文化",
        accommodation="市中心",
        transportation="地铁",
        budget=2000,
        user_input="我想安排一个三天两晚的北京行程，优先历史文化景点。",
    )


def _build_sample_context(request: TripRequest) -> TripWorkflowContext:
    """构造规划 Agent 使用的测试上下文。

    参数:
        request: 测试请求对象。

    返回值:
        TripWorkflowContext: 带有示例搜索结果的共享上下文。
    """
    context = TripWorkflowContext(request=request)
    context.save_search_results(
        attraction_result=AttractionSearchResponse(
            attractions=[
                Attraction(
                    name="故宫博物院",
                    address="北京市东城区景山前街4号",
                    location=Location(longitude=116.3975, latitude=39.9163),
                    visit_duration=240,
                    description="中国明清两代皇家宫殿，历史文化价值极高。",
                    category="历史文化",
                    rating=4.9,
                    ticket_price=60,
                ),
                Attraction(
                    name="国家博物馆",
                    address="北京市东城区东长安街16号",
                    location=Location(longitude=116.4074, latitude=39.9057),
                    visit_duration=180,
                    description="馆藏丰富，适合深度了解中国历史文化。",
                    category="博物馆",
                    rating=4.8,
                    ticket_price=0,
                ),
            ],
            message="已优先筛选历史文化类景点。",
        ),
        weather_result=WeatherSearchResponse(
            weather_info=[
                WeatherInfo(
                    date="2026-04-15",
                    day_weather="晴",
                    night_weather="多云",
                    day_temp=21,
                    night_temp=11,
                    wind_direction="东北风",
                    wind_power="3级",
                ),
                WeatherInfo(
                    date="2026-04-16",
                    day_weather="多云",
                    night_weather="晴",
                    day_temp=23,
                    night_temp=12,
                    wind_direction="北风",
                    wind_power="2级",
                ),
            ],
            message="天气总体稳定，建议携带薄外套。",
        ),
        hotel_result=HotelSearchResponse(
            hotels=[
                Hotel(
                    name="北京饭店",
                    address="北京市东城区东长安街33号",
                    location=Location(longitude=116.4102, latitude=39.9085),
                    price_range="800-1200元/晚",
                    rating="4.7",
                    distance="距故宫约2.5公里",
                    type="高档酒店",
                    estimated_cost=1000,
                ),
                Hotel(
                    name="王府井精品酒店",
                    address="北京市东城区王府井大街88号",
                    location=Location(longitude=116.4128, latitude=39.9134),
                    price_range="500-800元/晚",
                    rating="4.5",
                    distance="距国家博物馆约3.0公里",
                    type="精品酒店",
                    estimated_cost=650,
                ),
            ],
            message="已按预算和住宿偏好筛选酒店。",
        ),
        meals_result=MealSearchResponse(
            meals=[
                Meal(type="breakfast", name="护国寺小吃", estimated_cost=35),
                Meal(type="lunch", name="四季民福烤鸭", estimated_cost=180),
                Meal(type="dinner", name="老北京涮肉", estimated_cost=150),
                Meal(type="snack", name="豆汁儿焦圈", estimated_cost=25),
            ],
            message="已优先覆盖早餐、午餐、晚餐与小吃场景。",
        ),
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
    print("[ATTRACTION_RESULT]", result.model_dump())


async def test_hotel_search() -> None:
    """测试酒店搜索智能体并打印最终输出。

    返回值:
        None
    """
    request = _build_sample_request()
    agent = HotelSearchAgent(tools=PLACE_TOOLS)
    result = await agent.ainvoke(request)
    # print("[HOTEL_RESULT]", result.model_dump())


async def test_meal_search() -> None:
    """测试餐饮搜索智能体并打印最终输出。

    返回值:
        None
    """
    request = _build_sample_request()
    agent = MealSearchAgent(tools=PLACE_TOOLS)
    result = await agent.ainvoke(request)
    # print("[MEAL_RESULT]", result.model_dump())


async def test_weather_search() -> None:
    """测试天气搜索智能体并打印最终输出。

    返回值:
        None
    """
    request = _build_sample_request()
    agent = WeatherSearchAgent(tools=WEATHER_TOOLS)
    result = await agent.ainvoke(request)
    # print("[WEATHER_RESULT]", result.model_dump())


async def test_itinerary_planner() -> None:
    """使用模拟上下文测试行程规划智能体。"""
    request = _build_sample_request()
    context = _build_sample_context(request)
    agent = ItineraryPlannerAgent()
    result = await agent.ainvoke(context)
    print("[PLAN_RESULT]", result.model_dump())


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
    # print("[AMAP]", result)


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
    await test_itinerary_planner()


if __name__ == "__main__":
    asyncio.run(main())
