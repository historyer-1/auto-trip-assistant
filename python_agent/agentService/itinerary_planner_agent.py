"""行程规划 Agent：读取共享上下文，输出 TripPlan。"""

from __future__ import annotations

from pydantic import SecretStr
from langchain_openai import ChatOpenAI

from agentService.api_keys import QWEN_API_KEY
from agentService.prompts.prompt import PLANNER_AGENT_PROMPT, PLANNER_AGENT_USER_PROMPT
from agentService.trip_plan_formatter import TripPlanFormatter
from agentService.trip_workflow_context import TripWorkflowContext
from entity.BasicClass import TripPlan


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
            model="qwen-max",  # 切换为新版千问大模型
            temperature=0.1,
            api_key=SecretStr(QWEN_API_KEY),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.formatter = TripPlanFormatter()

    async def ainvoke(self, context: TripWorkflowContext) -> TripPlan:
        """根据共享上下文生成结构化 TripPlan。

        参数:
            context: 编排流程共享上下文。

        返回值:
            TripPlan: 结构化行程结果。
        """
        request = context.request

        # 组装最小输入，让规划 Agent 聚合三个搜索结果并输出 JSON。
        user_prompt = PLANNER_AGENT_USER_PROMPT.format(
            city=request.city,
            start_date=request.start_date,
            end_date=request.end_date,
            transportation=request.transportation,
            accommodation=request.accommodation,
            preferences=request.preference,
            budget_note=f"总预算约 {request.budget} 元",
            attraction_result=context.attraction_result,
            weather_result=context.weather_result,
            hotel_result=context.hotel_result,
        )

        response = await self.llm.ainvoke(
            [
                {"role": "system", "content": PLANNER_AGENT_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )

        # 先按 TripPlan 严格解析，失败后交给独立格式化类做字段兜底。
        raw_content = response.content if isinstance(response.content, str) else str(response.content)
        try:
            return TripPlan.model_validate_json(raw_content)
        except Exception:
            return self.formatter.format(raw_content)
