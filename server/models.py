from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class AgentStreamRequest(BaseModel):
    # 客户端请求契约：定义调用流式接口时允许提交的字段。
    agent_id: str = Field(..., description="Agent unique id")
    message: str = Field(..., min_length=1, description="Input prompt or task")
    metadata: dict[str, Any] = Field(default_factory=dict)
    stream_interval_ms: int = Field(default=250, ge=50, le=5000)
    max_chunks: int = Field(default=8, ge=1, le=100)


class StreamEvent(BaseModel):
    # 服务端统一事件信封：每一条 SSE 事件都遵循这个结构。
    version: str = "1.0"
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event: str
    payload: dict[str, Any] = Field(default_factory=dict)
    done: bool = False
    error: str | None = None
