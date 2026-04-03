"""MCP 长连接管理器。"""

from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

from agentService.api_keys import AMAP_WEB_API_KEY


class McpConnector:
    """负责 MCP Server 长连接、Session 初始化与工具加载。"""

    def __init__(self) -> None:
        """初始化连接管理器，不建立网络连接。"""
        self._server_params = StdioServerParameters(
            command="uvx",
            args=["amap-mcp-server"],
            env={"AMAP_MAPS_API_KEY": AMAP_WEB_API_KEY},
        )
        self._exit_stack = AsyncExitStack()
        self._session: ClientSession | None = None
        self._tools: list[Any] = []
        self._connected = False

    @property
    def tools(self) -> list[Any]:
        """返回加载后的 MCP 工具列表。"""
        return self._tools

    @property
    def connected(self) -> bool:
        """返回当前连接状态。"""
        return self._connected

    async def connect(self) -> None:
        """建立 MCP 长连接并加载工具。

        返回值:
            None
        """
        if self._connected:
            return

        # 1) 建立 stdio 长连接并进入上下文。
        read, write = await self._exit_stack.enter_async_context(
            stdio_client(self._server_params)
        )

        # 2) 创建会话并初始化。
        session = await self._exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        await session.initialize()
        self._session = session

        # 3) 仅在启动阶段加载一次工具，后续请求复用。
        self._tools = await load_mcp_tools(self._session)
        self._connected = True

    async def close(self) -> None:
        """关闭 MCP 长连接，确保资源释放。

        返回值:
            None
        """
        if not self._connected:
            return

        # 统一由 ExitStack 关闭 session 与 stdio 连接。
        await self._exit_stack.aclose()
        self._session = None
        self._tools = []
        self._connected = False
