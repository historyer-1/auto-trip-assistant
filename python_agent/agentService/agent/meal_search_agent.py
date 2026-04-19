"""餐饮搜索 Agent：通过提示词驱动自动工具调用与总结。"""

from __future__ import annotations

from typing import Any, cast

from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents.middleware import ToolCallLimitMiddleware

from agentService.entity.api_keys import MODEL, QWEN_API_KEY
from agentService.prompts.prompt import MEAL_AGENT_SYSTEM_PROMPT, MEAL_AGENT_USER_PROMPT
from agentService.entity.BasicClass import TripRequest


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
        self.tool_limiter = ToolCallLimitMiddleware(thread_limit=4, run_limit=4)
        self.llm_limiter = ModelCallLimitMiddleware(thread_limit=6, run_limit=6)
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
            middleware=cast(Any, [self.tool_limiter, self.llm_limiter]),
        )

    async def ainvoke(self, request: TripRequest) -> str:
        """执行一次餐饮搜索并返回结构化结果。

        参数:
            request: 结构化 TripRequest 请求对象。

        返回值:
            str: 模型与工具链路原始输出字符串。
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
        return str(tool_result)
