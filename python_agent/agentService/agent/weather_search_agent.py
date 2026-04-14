"""天气搜索 Agent：通过提示词驱动自动工具调用与总结。"""

from __future__ import annotations

from typing import Any

from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agentService.entity.api_keys import MODEL, QWEN_API_KEY
from agentService.prompts.prompt import WEATHER_AGENT_SYSTEM_PROMPT, WEATHER_AGENT_USER_PROMPT
from agentService.entity.BasicClass import TripRequest, WeatherSearchResponse


class WeatherSearchAgent:
    """天气搜索 Agent（极简复用型）。

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
            response_format=WeatherSearchResponse,
        )

    async def ainvoke(self, request: TripRequest) -> WeatherSearchResponse:
        """执行一次天气查询并返回中文摘要。

        参数:
            request: 结构化 TripRequest 请求对象。

        返回值:
            WeatherSearchResponse: 天气结构化结果和补充信息。
        """
        # 将 TripRequest 转成结构化提示词输入，直接喂给模型。
        user_prompt = WEATHER_AGENT_USER_PROMPT.format(
            city=request.city,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        tool_result = await self.agent.ainvoke(
            {
                "messages": [
                    {"role": "system", "content": WEATHER_AGENT_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
            }
        )

        if not isinstance(tool_result, dict):
            return WeatherSearchResponse(weather_info=[], message="")

        structured = tool_result.get("structured_response")
        if structured is None:
            return WeatherSearchResponse(weather_info=[], message="")

        if isinstance(structured, WeatherSearchResponse):
            return structured

        return WeatherSearchResponse.model_validate(structured)
