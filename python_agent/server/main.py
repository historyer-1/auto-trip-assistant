from __future__ import annotations

import asyncio
import logging
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from .models import AgentStreamRequest, StreamEvent
from .sse import to_sse_events

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Auto Trip Assistant Stream Server", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


async def generate_agent_events(request: AgentStreamRequest) -> AsyncGenerator[StreamEvent, None]:
    message_id: str | None = None

    try:
        # 先发送 start 事件，通知客户端本次流式会话已建立。
        start_event = StreamEvent(
            agent_id=request.agent_id,
            event="start",
            payload={
                "input_length": len(request.message),
                "metadata": request.metadata,
            },
            done=False,
        )
        message_id = start_event.message_id
        yield start_event

        # 这里是演示逻辑：按空格切分输入，后续可替换为真实 Agent 增量输出。
        chunks = request.message.split()
        if not chunks:
            chunks = [request.message]

        for index in range(min(request.max_chunks, len(chunks))):
            # 模拟增量生成节奏，每个时间片输出一个 chunk 事件。
            await asyncio.sleep(request.stream_interval_ms / 1000)
            yield StreamEvent(
                message_id=message_id,
                agent_id=request.agent_id,
                event="chunk",
                payload={
                    "index": index,
                    "text": chunks[index],
                },
                done=False,
            )

        # 发送 end 事件，标记本次流式输出正常结束。
        await asyncio.sleep(request.stream_interval_ms / 1000)
        yield StreamEvent(
            message_id=message_id,
            agent_id=request.agent_id,
            event="end",
            payload={
                "summary": "stream completed",
                "chunk_count": min(request.max_chunks, len(chunks)),
            },
            done=True,
        )
    except asyncio.CancelledError:
        # 客户端主动断开连接时会触发取消异常，记录后继续抛出以完成清理。
        logger.info("Client disconnected. agent_id=%s message_id=%s", request.agent_id, message_id)
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Stream generation failed")
        yield StreamEvent(
            message_id=message_id or "",
            agent_id=request.agent_id,
            event="error",
            payload={},
            done=True,
            error=str(exc),
        )


@app.post("/v1/agent/stream")
async def stream_agent_message(request: AgentStreamRequest) -> StreamingResponse:
    # 将事件生成器封装为 text/event-stream 响应，交给客户端持续消费。
    events = to_sse_events(generate_agent_events(request))
    return StreamingResponse(
        events,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": str(exc.status_code),
                "message": exc.detail,
            }
        },
    )
