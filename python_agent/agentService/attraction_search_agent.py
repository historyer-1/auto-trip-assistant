"""景点搜索 Agent：通过提示词驱动自动工具调用与总结。"""

from __future__ import annotations

from typing import Any

from pydantic import SecretStr

# 这是 OpenAI 聊天模型的 LangChain 封装。
# 如果你后续用其他模型（如千问/智谱），可替换这一行及初始化参数。
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agentService.api_keys import QWEN_API_KEY
from agentService.prompts.attraction_prompt import (
    AGENT_SYSTEM_PROMPT,
)


class AttractionSearchAgent:
    """景点搜索 Agent（极简复用型）。

    说明：
    - 不负责 MCP 连接管理；
    - 启动阶段注入已加载的 tools，并预创建 tool agent；
    - 请求阶段仅调用 ainvoke，流程由提示词驱动。
    """

    def __init__(
        self,
        tools: list[Any],
    ) -> None:
        """
        初始化 Agent。

        参数:
            tools: 已由 McpConnector 加载好的 MCP 工具列表。

        返回值:
            None
        """

        # 兼容说明：
        # 1) 优先支持外部注入 llm；
        # 2) 若未注入，则默认使用千问 Qwen3-max（OpenAI 兼容接口）。
        self.llm = ChatOpenAI(
            model="qwen3-max",
            temperature=0.1,
            api_key=SecretStr(QWEN_API_KEY),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        # 启动时预创建一次工具 Agent，后续请求全部复用。
        self.tool_agent = create_agent(model=self.llm, tools=tools)

    async def ainvoke(
        self,
        user_input: str,
    ) -> str:
        """
        执行一次景点查询：由模型自行决定工具调用并完成总结。

        参数:
            user_input: 用户自然语言输入。

        返回值:
            str: 最终推荐文案。
        """
        # 由提示词驱动：模型先调工具，再基于工具结果总结。
        tool_result = await self.tool_agent.ainvoke(
            {
                "messages": [
                    {"role": "system", "content": AGENT_SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ]
            }
        )

        # 保留最小必要解析：提取 Agent 最后一条消息作为响应。
        messages = tool_result.get("messages", []) if isinstance(tool_result, dict) else []
        if not messages:
            return "未获取到可用结果，请稍后重试。"

        content = getattr(messages[-1], "content", "")
        if isinstance(content, str):
            return content

        return str(content)


