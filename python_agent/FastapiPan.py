"""FastAPI 应用入口：生命周期管理与轻量路由。"""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from agentService.agent.trip_orchestrator_agent import TripOrchestratorAgent
from agentService.entity.BasicClass import TripPlan, TripRequest
from agentService.tools.AmapTool import amap_search, amap_weather_search

logger = logging.getLogger(__name__)




@asynccontextmanager
async def lifespan(app: FastAPI):
	"""管理应用生命周期。

	"""
	# 直接注入本地高德工具，避免依赖已移除的 MCP 连接。
	app.state.agent = TripOrchestratorAgent(tools=[amap_search, amap_weather_search])
	yield



app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
	"""健康检查接口。

	返回值:
		dict[str, str]: 当前服务状态。
	"""
	return {"status": "ok"}


@app.post("/agent/query", response_model=TripPlan)
async def query_agent(payload: TripRequest) -> TripPlan:
	"""调用预创建的 Agent 执行查询。

	参数:
		payload: 请求体，包含用户输入。

	返回值:
		TripPlan: 结构化的行程规划结果。
	"""
	# 路由层不持有任何连接状态，仅从 app.state 获取已创建实例。
	agent: TripOrchestratorAgent | None = getattr(app.state, "agent", None)
	if agent is None:
		raise HTTPException(status_code=503, detail="Agent 尚未就绪")

	
	answer = await asyncio.wait_for(agent.ainvoke(payload), timeout=60)
	return answer
