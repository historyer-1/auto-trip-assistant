import asyncio

from agentService.attraction_search_agent import AttractionSearchAgent
from agentService.mcp_connector import McpConnector


async def _run_once(user_input: str) -> None:
    """命令行调试入口。

    参数:
        user_input: 用户输入。

    返回值:
        None
    """
    connector = McpConnector()
    await connector.connect()

    try:
        # 复用启动阶段加载的工具创建 Agent。
        agent = AttractionSearchAgent(tools=connector.tools)
        result = await agent.ainvoke(user_input=user_input)
        print(result)
    finally:
        await connector.close()


def main() -> None:
    user_input = input("请输入旅行需求（如：我想在北京找历史文化景点，5个）：").strip()

    asyncio.run(_run_once(user_input))


if __name__ == "__main__":
    main()
