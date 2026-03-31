from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import asynccontextmanager

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent

from api_keys import AMAP_WEB_API_KEY

class AmapMcpTool:
    amap_server_params = StdioServerParameters(
        command="uvx",
        args=["-y", "@sugarforever/amap-mcp-server"],
        env={
            "AMAP_API_KEY": AMAP_WEB_API_KEY,
        },
    )

    def __init__(self):
        pass
    
    @staticmethod
    @asynccontextmanager
    async def getTools():
        async with stdio_client(AmapMcpTool.amap_server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools = await load_mcp_tools(session)

                yield tools 

                