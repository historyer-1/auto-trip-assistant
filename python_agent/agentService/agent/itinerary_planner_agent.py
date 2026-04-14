"""行程规划 Agent：读取共享上下文，输出 TripPlan。"""

from __future__ import annotations

import json

from pydantic import SecretStr
from langchain_openai import ChatOpenAI

from agentService.entity.api_keys import MODEL, QWEN_API_KEY
from agentService.prompts.prompt import PLANNER_AGENT_PROMPT, PLANNER_AGENT_USER_PROMPT
from agentService.entity.trip_plan_formatter import TripPlanFormatter
from agentService.entity.trip_workflow_context import TripWorkflowContext
from agentService.entity.BasicClass import TripPlan


class ItineraryPlannerAgent:
    """行程规划 Agent（不使用工具）。

    说明：
    - 仅依赖大模型做总结和格式化；
    - 输入来自共享上下文；
    - 输出强制落到 TripPlan 结构。
    """

    def __init__(self) -> None:
        """初始化规划 Agent。

        返回值:
            None
        """
        self.llm = ChatOpenAI(
            model=MODEL,
            temperature=0.1,
            api_key=SecretStr(QWEN_API_KEY),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        # 千问兼容模式下，按官方方式使用 response_format 开启 JSON 对象输出。
        self.agent = self.llm.bind(response_format={"type": "json_object"})
        self.formatter = TripPlanFormatter()

    async def ainvoke(self, context: TripWorkflowContext) -> TripPlan:
        """根据共享上下文生成结构化 TripPlan。

        参数:
            context: 编排流程共享上下文。

        返回值:
            TripPlan: 结构化行程结果。
        """
        request = context.request

        attraction_result = json.dumps(
            context.attraction_response.model_dump(mode="json"),
            ensure_ascii=False,
            indent=2,
        )
        weather_result = json.dumps(
            context.weather_response.model_dump(mode="json"),
            ensure_ascii=False,
            indent=2,
        )
        hotel_result = json.dumps(
            context.hotel_response.model_dump(mode="json"),
            ensure_ascii=False,
            indent=2,
        )
        meals_result = json.dumps(
            context.meals_response.model_dump(mode="json"),
            ensure_ascii=False,
            indent=2,
        )

        # 组装最小输入，让规划 Agent 聚合三个搜索结果并输出 JSON。
        user_prompt = PLANNER_AGENT_USER_PROMPT.format(
            city=request.city,
            start_date=request.start_date,
            end_date=request.end_date,
            transportation=request.transportation,
            accommodation=request.accommodation,
            preferences=request.preference,
            budget_note=f"总预算约 {request.budget} 元",
            attraction_result=attraction_result,
            weather_result=weather_result,
            hotel_result=hotel_result,
            meals_result=meals_result,
        )
        user_prompt += "\n\n请仅返回 JSON 对象。"

        response = await self.agent.ainvoke(
            [
                {"role": "system", "content": PLANNER_AGENT_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )
        raw_content = response.content if isinstance(response.content, str) else str(response.content)
        return self.formatter.format(raw_content)

