"""酒店搜索 Agent：通过提示词驱动自动工具调用与总结。"""

from __future__ import annotations

from typing import Any

from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agentService.entity.api_keys import MODEL, QWEN_API_KEY
from agentService.prompts.prompt import HOTEL_AGENT_SYSTEM_PROMPT, HOTEL_AGENT_USER_PROMPT
from agentService.entity.BasicClass import HotelSearchResponse, TripRequest


class HotelSearchAgent:
    """酒店搜索 Agent（极简复用型）。

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
            response_format=HotelSearchResponse,
        )

    async def ainvoke(self, request: TripRequest) -> HotelSearchResponse:
        """执行一次酒店搜索并返回中文摘要。

        参数:
            request: 结构化 TripRequest 请求对象。

        返回值:
            HotelSearchResponse: 酒店结构化结果和补充信息。
        """
        # 将 TripRequest 转成结构化提示词输入，直接喂给模型。
        user_prompt = HOTEL_AGENT_USER_PROMPT.format(
            city=request.city,
            accommodation=request.accommodation,
            budget_note=f"总预算约 {request.budget} 元",
            start_date=request.start_date,
            end_date=request.end_date,
        )

        tool_result = await self.agent.ainvoke(
            {
                "messages": [
                    {"role": "system", "content": HOTEL_AGENT_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
            }
        )

        # 调试输出：查看模型和工具链的原始返回，便于判断空结果来源。
        # print("[HOTEL] tool_result:", tool_result)

        if not isinstance(tool_result, dict):
            return HotelSearchResponse(hotels=[], message="")

        structured = tool_result.get("structured_response")
        # print("[HOTEL] structured_response:", structured)
        if structured is None:
            return HotelSearchResponse(hotels=[], message="")

        if isinstance(structured, HotelSearchResponse):
            return structured

        return HotelSearchResponse.model_validate(structured)
