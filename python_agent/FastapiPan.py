"""FastAPI 应用入口：生命周期管理与轻量路由。"""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agentService.attraction_search_agent import AttractionSearchAgent
from agentService.mcp_connector import McpConnector

logger = logging.getLogger(__name__)


class AgentQueryRequest(BaseModel):
	"""智能体请求体。"""

	user_input: str = Field(..., description="用户输入的旅行需求")


class AgentQueryResponse(BaseModel):
	"""智能体响应体。"""

	answer: str = Field(..., description="智能体生成的推荐内容")


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""管理应用生命周期。

	启动阶段：
	1. 创建并连接 McpConnector；
	2. 预加载 MCP 工具；
	3. 预创建 AttractionSearchAgent；
	4. 挂载到 app.state 供路由复用。

	关闭阶段：
	1. 关闭 MCP 长连接与会话资源。

	参数:
		app: FastAPI 应用实例。

	返回值:
		None
	"""
	connector = McpConnector()
	await connector.connect()

	app.state.mcp_connector = connector
	app.state.agent = AttractionSearchAgent(tools=connector.tools)

	try:
		yield
	finally:
		await connector.close()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
	"""健康检查接口。

	返回值:
		dict[str, str]: 当前服务状态。
	"""
	return {"status": "ok"}


@app.post("/agent/query", response_model=AgentQueryResponse)
async def query_agent(payload: AgentQueryRequest) -> AgentQueryResponse:
	"""调用预创建的 Agent 执行查询。

	参数:
		payload: 请求体，包含用户输入。

	返回值:
		AgentQueryResponse: 智能体回复。
	"""
	# 路由层不持有任何连接状态，仅从 app.state 获取已创建实例。
	agent: AttractionSearchAgent | None = getattr(app.state, "agent", None)
	if agent is None:
		raise HTTPException(status_code=503, detail="Agent 尚未就绪")

	try:
		# 为每个请求增加超时保护，避免单请求长时间占用工作线程。
		answer = await asyncio.wait_for(agent.ainvoke(payload.user_input), timeout=45)
		return AgentQueryResponse(answer=answer)
	except TimeoutError as exc:
		raise HTTPException(status_code=504, detail="请求超时，请稍后重试") from exc
	except Exception as exc:
		logger.exception("调用 Agent 失败")
		raise HTTPException(status_code=500, detail="服务内部错误") from exc
