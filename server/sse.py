from __future__ import annotations

import json
from typing import AsyncGenerator

from .models import StreamEvent


def encode_sse(event_name: str, data: dict) -> str:
    # SSE 协议要求以空行结束一帧；缺少 \n\n 会导致客户端无法正确切分事件。
    body = json.dumps(data, ensure_ascii=False)
    return f"event: {event_name}\\ndata: {body}\n\n"


async def to_sse_events(events: AsyncGenerator[StreamEvent, None]) -> AsyncGenerator[str, None]:
    # 将类型化事件按需转换为 SSE 文本帧，边生成边发送。
    async for event in events:
        yield encode_sse(event.event, event.model_dump())
