import argparse
import asyncio

from agentService.attraction_search_agent import AttractionSearchAgent


async def _run_once(city: str, preference: str, limit: int) -> None:
    agent = AttractionSearchAgent()
    result = await agent.run(city=city, preference=preference, limit=limit)
    print(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AttractionSearchAgent once")
    parser.add_argument("--city", default="北京", help="City to search")
    parser.add_argument("--preference", default="历史文化", help="Travel preference")
    parser.add_argument("--limit", type=int, default=5, help="Max items to request")
    args = parser.parse_args()

    asyncio.run(_run_once(args.city, args.preference, args.limit))


if __name__ == "__main__":
    main()
