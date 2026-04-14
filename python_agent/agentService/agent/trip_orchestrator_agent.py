"""总编排 Agent：并发执行搜索智能体并调用规划智能体输出 TripPlan。"""

from __future__ import annotations

import asyncio
from typing import Any

from agentService.agent.attraction_search_agent import AttractionSearchAgent
from agentService.agent.hotel_search_agent import HotelSearchAgent
from agentService.agent.itinerary_planner_agent import ItineraryPlannerAgent
from agentService.agent.meal_search_agent import MealSearchAgent
from agentService.agent.weather_search_agent import WeatherSearchAgent
from agentService.entity.trip_workflow_context import TripWorkflowContext
from agentService.entity.BasicClass import TripPlan, TripRequest


class TripOrchestratorAgent:
    """总编排 Agent。

    说明：
    - 在初始化时实例化四个成员 Agent；
    - 在请求阶段并发执行景点/天气/酒店/餐饮搜索；
    - 将搜索结果写入共享上下文后，再执行行程规划。
    """

    def __init__(self, tools: list[Any]) -> None:
        """初始化总编排 Agent。

        参数:
            tools: 已由 McpConnector 加载好的 MCP 工具列表。

        返回值:
            None
        """
        self.attraction_agent = AttractionSearchAgent(tools=tools)
        self.weather_agent = WeatherSearchAgent(tools=tools)
        self.hotel_agent = HotelSearchAgent(tools=tools)
        self.meal_agent = MealSearchAgent(tools=tools)
        self.planner_agent = ItineraryPlannerAgent()

    async def ainvoke(self, request: TripRequest) -> TripPlan:
        """执行完整旅行规划流程。

        参数:
            request: 用户旅行请求。

        返回值:
            TripPlan: 结构化行程规划结果。
        """
        context = TripWorkflowContext(request=request)

        # 并发执行四个搜索任务，利用 LLM/工具 I/O 等待时间提升吞吐。
        attraction_response, weather_result, hotel_result, meals_result = await asyncio.gather(
            self.attraction_agent.ainvoke(request),
            self.weather_agent.ainvoke(request),
            self.hotel_agent.ainvoke(request),
            self.meal_agent.ainvoke(request),
        )

        # 将搜索结果写入共享上下文，供规划 Agent 汇总使用。
        context.save_search_results(
            attraction_result=attraction_response,
            weather_result=weather_result,
            hotel_result=hotel_result,
            meals_result=meals_result,
        )

        # ====== 以下为测试代码：可观测性增强，排查工具链路缺失 ======
        # 打印四个搜索智能体的中间结果，确认是哪一层返回了空值。
        # print("[TEST] attraction_response 前300字：", str(attraction_response)[:300])
        # print("[TEST] weather_result 前300字：", str(weather_result)[:300])
        # print("[TEST] hotel_result 前300字：", str(hotel_result)[:300])
        # print("[TEST] meals_result 前300字：", str(meals_result)[:300])

        # 先执行规划，再打印最终 TripPlan 结果，便于区分“搜索为空”和“规划失败”。
        final_result = await self.planner_agent.ainvoke(context)
        #print("[TEST] final_result：", final_result)
        # ====== 测试代码结束 ======

        # 规划 Agent 读取共享上下文，输出最终 TripPlan。
        return final_result
