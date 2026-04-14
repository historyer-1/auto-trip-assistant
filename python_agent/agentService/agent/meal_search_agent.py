"""餐饮搜索 Agent：通过提示词驱动自动工具调用与总结。"""

from __future__ import annotations

from typing import Any

from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agentService.entity.api_keys import MODEL, QWEN_API_KEY
from agentService.prompts.prompt import MEAL_AGENT_SYSTEM_PROMPT, MEAL_AGENT_USER_PROMPT
from agentService.entity.BasicClass import MealSearchResponse, TripRequest


class MealSearchAgent:
    """餐饮搜索 Agent（极简复用型）。

    说明：
    - 不负责 MCP 连接管理；
    - 启动阶段注入已加载的 tools，并预创建 agent；
    - 请求阶段仅调用 ainvoke，流程由提示词驱动。
    """

    def __init__(self, tools: list[Any]) -> None:
        """初始化 Agent。

        参数:
            tools: 已由 McpConnector 加载好的 MCP 工具列表。

        返回值:
            None
        """
        self.llm = ChatOpenAI(
            model=MODEL,
            temperature=0.1,
            api_key=SecretStr(QWEN_API_KEY),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            extra_body={"enable_thinking": False},
        )
        self.agent = create_agent(
            model=self.llm,
            tools=tools,
            response_format=MealSearchResponse,
        )

    async def ainvoke(self, request: TripRequest) -> MealSearchResponse:
        """执行一次餐饮搜索并返回结构化结果。

        参数:
            request: 结构化 TripRequest 请求对象。

        返回值:
            MealSearchResponse: 餐饮结构化结果和补充信息。
        """
        # 将 TripRequest 转成结构化提示词输入，直接喂给模型。
        user_prompt = MEAL_AGENT_USER_PROMPT.format(
            city=request.city,
            preference=request.preference,
            accommodation=request.accommodation,
            budget_note=f"总预算约 {request.budget} 元",
            start_date=request.start_date,
            end_date=request.end_date,
        )

        tool_result = await self.agent.ainvoke(
            {
                "messages": [
                    {"role": "system", "content": MEAL_AGENT_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
            }
        )

        # 调试输出：查看模型和工具链的原始返回，便于判断空结果来源。
        # print("[MEAL] tool_result:", tool_result)

        if not isinstance(tool_result, dict):
            return MealSearchResponse(meals=[], message="")

        structured = tool_result.get("structured_response")
        # print("[MEAL] structured_response:", structured)
        if structured is None:
            return MealSearchResponse(meals=[], message="")

        if isinstance(structured, MealSearchResponse):
            return structured

        return MealSearchResponse.model_validate(structured)
