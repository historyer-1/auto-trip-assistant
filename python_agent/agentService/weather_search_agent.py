"""天气搜索 Agent：通过提示词驱动自动工具调用与总结。"""

from __future__ import annotations

from typing import Any

from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agentService.api_keys import QWEN_API_KEY
from agentService.prompts.prompt import WEATHER_AGENT_PROMPT, WEATHER_AGENT_USER_PROMPT
from entity.BasicClass import TripRequest


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
            model="qwen-max",  # 切换为新版千问大模型
            temperature=0.1,
            api_key=SecretStr(QWEN_API_KEY),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.agent = create_agent(model=self.llm, tools=tools)

    async def ainvoke(self, request: TripRequest) -> str:
        """执行一次天气查询并返回中文摘要。

        参数:
            request: 结构化 TripRequest 请求对象。

        返回值:
            str: 天气查询结果。
        """
        # 将请求对象格式化为用户提示词，交给模型自动选择工具。
        user_prompt = WEATHER_AGENT_USER_PROMPT.format(
            city=request.city,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        tool_result = await self.agent.ainvoke(
            {
                "messages": [
                    {"role": "system", "content": WEATHER_AGENT_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
            }
        )

        # 保留最小必要解析：取最后一条消息内容。
        messages = tool_result.get("messages", []) if isinstance(tool_result, dict) else []
        if not messages:
            return "未获取到可用天气结果，请稍后重试。"

        content = getattr(messages[-1], "content", "")
        if isinstance(content, str):
            return content
        return str(content)
