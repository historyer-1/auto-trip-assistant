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

import json

from pydantic import SecretStr

# Prompt 模板：把系统指令 + 用户输入变量组织起来。
from langchain_core.prompts import ChatPromptTemplate

# 输出解析器：把模型消息对象转成普通字符串，便于直接返回给调用方。
from langchain_core.output_parsers import StrOutputParser

# 这是 OpenAI 聊天模型的 LangChain 封装。
# 如果你后续用其他模型（如千问/智谱），可替换这一行及初始化参数。
from langchain_openai import ChatOpenAI

from agentService.api_keys import QWEN_API_KEY
from agentService.prompts.attraction_prompt import (
    QUERY_SYSTEM_PROMPT_TEMPLATE,
    SUMMARY_HUMAN_PROMPT_TEMPLATE,
    SUMMARY_SYSTEM_PROMPT_TEMPLATE,
)
from agentService.tools.AmapMcpTool import AmapMcpTool


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

        # 第一阶段：根据用户自然语言生成严格工具计划 JSON。
        self.plan_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        QUERY_SYSTEM_PROMPT_TEMPLATE
                    ),
                ),
                (
                    "human",
                    "用户输入: {user_input}\n请输出严格 JSON。",
                ),
            ]
        )
        self.plan_chain = self.plan_prompt | self.llm | StrOutputParser()

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
    def _extract_json_obj(text: str) -> dict:
        """
        从模型输出中提取 JSON；若模型夹带多余文本，尽可能容错解析。
        """
        raw = (text or "").strip()
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            data = json.loads(raw[start : end + 1])
            if isinstance(data, dict):
                return data

        raise ValueError("Planner 未返回可解析的 JSON 对象")

    async def run(
        self,
        user_input: str,
    ) -> str:
        """
        根据用户输入生成严格工具调用 JSON，调用 MCP Tool，再输出景点推荐。

        参数：
        - user_input: 用户自然语言输入（例如：我想在北京找历史文化景点）
        """
        tool_call_text = await self.plan_chain.ainvoke(
            {
                "user_input": user_input,
            }
        )
        tool_call_plan = self._extract_json_obj(tool_call_text)
        print("大模型调用工具")
        print(tool_call_plan)



        #调用类成员函数执行 MCP 工具查询。
        poi_json = await AmapMcpTool.query_attraction(
            tool_call_plan=json.dumps(tool_call_plan, ensure_ascii=False),
            model=self.llm,
        )


        plan_args = AmapMcpTool._extract_plan_arguments(
            json.dumps(tool_call_plan, ensure_ascii=False)
        )

        #把真实查询结果交给总结链，输出最终推荐文案
        output_text = await self.summary_chain.ainvoke(
            {
                "city": plan_args["city"],
                "preferences": plan_args["preferences"],
                "keyword": plan_args["keyword"],
                "limit": plan_args["limit"],
                "poi_json": poi_json,
            }
        )
        return output_text


