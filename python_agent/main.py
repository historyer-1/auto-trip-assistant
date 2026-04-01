import asyncio

from agentService.attraction_search_agent import AttractionSearchAgent


async def _run_once(user_input: str) -> None:
    agent = AttractionSearchAgent()
    result = await agent.run(user_input=user_input)
    print(result)


def main() -> None:
    user_input = input("请输入旅行需求（如：我想在北京找历史文化景点，5个）：").strip()

    asyncio.run(_run_once(user_input))


if __name__ == "__main__":
    main()
