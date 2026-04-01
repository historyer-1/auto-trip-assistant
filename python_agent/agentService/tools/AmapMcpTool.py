import json
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel

from agentService.api_keys import AMAP_WEB_API_KEY

class AmapMcpTool:
    amap_server_params = StdioServerParameters(
        command="uvx",
        args=["amap-mcp-server"],
        env={
            "AMAP_MAPS_API_KEY": AMAP_WEB_API_KEY,
        },
    )

    def __init__(self):
        pass

    @staticmethod
    def _extract_plan_arguments(tool_call_plan: str) -> dict:
        """
        解析并标准化 Planner 输出的工具调用 JSON。
        """
        plan = json.loads((tool_call_plan or "").strip())
        if not isinstance(plan, dict):
            raise ValueError("tool_call_plan 必须是 JSON 对象")

        arguments = plan.get("arguments", {})
        if not isinstance(arguments, dict):
            arguments = {}

        city = str(arguments.get("city", "")).strip() or "北京"
        preference = str(arguments.get("preferences", "")).strip() or "休闲散步"
        keyword = str(arguments.get("keyword", "")).strip() or "景点"
        limit_raw = arguments.get("limit", 5)
        try:
            limit = int(limit_raw)
        except (TypeError, ValueError):
            limit = 5
        limit = min(max(limit, 1), 20)

        return {
            "city": city,
            "preferences": preference,
            "keyword": keyword,
            "limit": limit,
        }

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
    
    @staticmethod
    async def query_attraction(
        tool_call_plan: str,
        model: BaseChatModel,
    ) -> str:
        print("正在调用mcp工具\n")
        tool_call = json.loads(tool_call_plan)

        async with stdio_client(AmapMcpTool.amap_server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools = await load_mcp_tools(session)

                tool_agent = create_agent(
                    model=model,
                    tools=tools,
                )



                tool_result = await tool_agent.ainvoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": (
                                    "请根据参数调用合适的高德 MCP 工具查询景点，并返回结构化结果。\n"
                                    f"tool_call={tool_call}\n"
                                ),
                            }
                        ]
                    }
                )

        return AmapMcpTool._normalize_tool_result(tool_result)
 

                