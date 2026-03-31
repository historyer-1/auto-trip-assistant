"""
AttractionSearchAgent（景点搜索专家）

这个文件是单文件教学版实现：
- 目标：帮助你看懂 LangChain 最基础的输入输出处理；
- 职责：根据用户偏好整理景点推荐结果；
- 外部依赖：无（本文件不直接调用任何地图 API）。

重要说明：
- 按你当前要求，智能体不再集成高德 API 查询；
- 外部（例如 MCP 工具调用层）只需把 POI JSON 结果传入本智能体；
- 本智能体只负责输入整理、关键词逻辑、以及最终文案输出。
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional
import json
from pydantic import SecretStr

# Prompt 模板：把系统指令 + 用户输入变量组织起来。
from langchain_core.prompts import ChatPromptTemplate

# 输出解析器：把模型消息对象转成普通字符串，便于直接返回给调用方。
from langchain_core.output_parsers import StrOutputParser
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent

# 这是 OpenAI 聊天模型的 LangChain 封装。
# 如果你后续用其他模型（如千问/智谱），可替换这一行及初始化参数。
from langchain_openai import ChatOpenAI

from agentService.api_keys import QWEN_API_KEY
from agentService.prompts.attraction_prompt import (
    QUERY_HUMAN_PROMPT_TEMPLATE,
    QUERY_SYSTEM_PROMPT_TEMPLATE,
    SUMMARY_HUMAN_PROMPT_TEMPLATE,
    SUMMARY_SYSTEM_PROMPT_TEMPLATE,
)
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agentService.api_keys import AMAP_WEB_API_KEY


class AttractionSearchAgent:
    """
    景点搜索 Agent（教学版）

    你可以把它理解成：
    - 大脑是 LLM（ChatOpenAI）
    - 输入材料是外部传入的 POI JSON（由 MCP 工具层负责查询）
    - 行为规范是 Prompt（系统指令）

    这里采用两段式流程：
    1) 先用 Python 规则把偏好映射成关键词（供外部查询层使用）；
    2) 外部查询层把 POI JSON 回传后，再由本 Agent 整理为最终推荐文案。
    """

    amap_server_params = StdioServerParameters(
        command="uvx",
        args=["amap-mcp-server"],
        env={
            "AMAP_MAPS_API_KEY": AMAP_WEB_API_KEY,
        },
    )

    def __init__(
        self
    ) -> None:
        """
        初始化 Agent。

        参数说明：
        - model_name: 使用哪个模型，如 gpt-4o-mini。
        - temperature: 采样温度，越低越稳定，搜索任务建议低温。
        - llm: 可选，允许从外部注入已配置好的 LangChain 聊天模型对象。
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

        # 第一阶段：生成“可执行的工具调用 JSON”
        # 说明：这个链只负责告诉工具层“该怎么查”，不直接输出景点推荐。
        self.query_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", QUERY_SYSTEM_PROMPT_TEMPLATE),
                ("human", QUERY_HUMAN_PROMPT_TEMPLATE),
            ]
        )
        self.query_chain = self.query_prompt | self.llm | StrOutputParser()

        # 第二阶段：拿到真实 POI 返回后，输出最终推荐文案。
        self.summary_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SUMMARY_SYSTEM_PROMPT_TEMPLATE),
                ("human", SUMMARY_HUMAN_PROMPT_TEMPLATE),
            ]
        )
        self.summary_chain = self.summary_prompt | self.llm | StrOutputParser()


    @staticmethod
    def _map_preference_to_keyword(preference: str) -> str:
        """
        把用户偏好映射为更适合检索的关键词。

        说明：
        - 用户表达常常较抽象（如历史文化）；
        - 检索系统对具体名词（如博物馆）通常命中更好。
        """
        mapping = {
            "历史文化": "博物馆",
            "自然风光": "自然公园",
            "亲子": "动物园",
            "网红打卡": "景区",
            "休闲散步": "城市公园",
        }
        return mapping.get(preference.strip(), preference.strip() or "景点")

    @staticmethod
    def _normalize_tool_result(tool_result: Any) -> str:
        """
        将工具 Agent 的输出统一为字符串，作为总结链输入。
        """
        if isinstance(tool_result, str):
            return tool_result

        if isinstance(tool_result, dict):
            messages = tool_result.get("messages")
            if isinstance(messages, list) and messages:
                last_msg = messages[-1]
                content = getattr(last_msg, "content", None)
                if isinstance(content, str):
                    return content
            return json.dumps(tool_result, ensure_ascii=False, default=str)

        return str(tool_result)

    async def _query_poi_with_mcp(
        self,
        city: str,
        preference: str,
        keyword: str,
        limit: int,
        tool_call_plan: str,
    ) -> str:
        """
        调用 MCP 工具查询景点，并返回可传入总结链的字符串。
        """
        async with stdio_client(self.amap_server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)

                tool_agent = create_agent(
                    model=self.llm,
                    tools=tools,
                )
                tool_result = await tool_agent.ainvoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": (
                                    "请根据参数调用合适的高德 MCP 工具查询景点，并返回结构化结果。\n"
                                    f"city={city}\n"
                                    f"preferences={preference}\n"
                                    f"keyword={keyword}\n"
                                    f"limit={limit}\n"
                                    f"tool_call_plan={tool_call_plan}"
                                ),
                            }
                        ]
                    }
                )

        return self._normalize_tool_result(tool_result)


    async def run(
        self,
        city: str,
        preference: str,
        limit: int = 5,
        #tool_invoker: Optional[Callable[[str, Dict[str, Any]], Dict[str, Any]]] = None,
    ) -> str:
        """
        先生成工具查询参数，再调用 MCP Tool，最后输出景点推荐。

        参数：
        - city: 城市名称
        - preference: 用户偏好（如历史文化）
        - limit: 目标结果上限，用于提示模型控制输出规模
        - tool_invoker: 外部注入的 MCP 调用函数
          签名约定: tool_invoker(tool_name, arguments) -> dict
        """
        keyword = self._map_preference_to_keyword(preference)

        # 第一步：让大模型输出“工具调用 JSON”
        tool_call = await self.query_chain.ainvoke(
            {
                "city": city,
                "preferences": preference,
                "keyword": keyword,
                "limit": limit,
            }
        )

        # 第二步：调用类成员函数执行 MCP 工具查询。
        poi_json = await self._query_poi_with_mcp(
            city=city,
            preference=preference,
            keyword=keyword,
            limit=limit,
            tool_call_plan=tool_call,
        )


        # 第三步：把真实查询结果交给总结链，输出最终推荐文案
        output_text = await self.summary_chain.ainvoke(
            {
                "city": city,
                "preferences": preference,
                "keyword": keyword,
                "limit": limit,
                "poi_json": poi_json,
            }
        )
        return output_text


