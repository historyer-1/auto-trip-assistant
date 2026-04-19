"""景点搜索 Agent：通过提示词驱动自动工具调用与总结。"""

from __future__ import annotations

from typing import Any, cast

from pydantic import SecretStr

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agentService.entity.api_keys import MODEL, QWEN_API_KEY
from agentService.entity.debug_callbacks import DebugTraceCallbackHandler
from agentService.prompts.prompt import ATTRACTION_AGENT_SYSTEM_PROMPT, ATTRACTION_AGENT_USER_PROMPT

from agentService.entity.BasicClass import TripRequest
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.agents.middleware import ModelCallLimitMiddleware

class AttractionSearchAgent:
    """景点搜索 Agent（极简复用型）。

    说明：
    - 不负责 MCP 连接管理；
    - 启动阶段注入已加载的 tools，并预创建agent；
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

        self.tool_limiter = ToolCallLimitMiddleware(thread_limit=4, run_limit=4)
        self.llm_limiter = ModelCallLimitMiddleware(thread_limit=6, run_limit=6)
        self.llm = ChatOpenAI(
            model=MODEL,
            temperature=0.1,
            api_key=SecretStr(QWEN_API_KEY),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            extra_body={
                "enable_thinking": False,
            },
        )

        # 启动时预创建一次工具 Agent，后续请求全部复用。
        self.agent = create_agent(
            model=self.llm,
            tools=tools,
            middleware=cast(Any, [self.tool_limiter, self.llm_limiter]),
        )

    async def ainvoke(
        self,
        request: TripRequest,
    ) -> str:
        """
        执行一次景点查询：由模型自行决定工具调用并完成总结。

        参数:
            request: 结构化的 TripRequest 请求对象。

        返回值:
            str: 模型与工具链路原始输出字符串。
        """
        # 将 TripRequest 转成结构化提示词输入，直接喂给模型。
        user_prompt = ATTRACTION_AGENT_USER_PROMPT.format(**request.model_dump())

        # 由提示词驱动：模型先调工具，再基于工具结果总结。
        debug_callback = DebugTraceCallbackHandler(label="ATTRACTION")
        tool_result = await self.agent.ainvoke(
            {
                "messages": [
                    {"role": "system", "content": ATTRACTION_AGENT_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
            },
            #config={"callbacks": [debug_callback]},
        )
        return str(tool_result)


