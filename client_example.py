from __future__ import annotations

import json  # 用于解析 JSON 格式的流式事件

import httpx  # 现代 Python HTTP 客户端，支持流式读取（不需要一次性等待整个响应）

# 服务端流式接口地址
URL = "http://127.0.0.1:8000/v1/agent/stream"

# 向服务端发送的请求体，必须与 server/models.py 的 AgentStreamRequest 结构对应
payload = {
    "agent_id": "trip-agent-001",  # 发起请求的 agent 标识
    "message": "plan a 3-day trip to Shanghai with metro-based routes",  # 实际任务/提示词
    "metadata": {"user_id": "u-1001"},  # 可选的元数据，比如用户信息、会话标签等
    "stream_interval_ms": 300,  # 服务端每个 chunk 之间的间隔（毫秒）
    "max_chunks": 20,  # 最多返回多少个 chunk（防止无限输出）
}


def main() -> None:
    # 创建 HTTP 客户端，超时时间设置为 30 秒（防止长时间等待造成假死）
    with httpx.Client(timeout=30) as client:
        # 使用 stream 模式发起 POST 请求，这样可以实时接收响应而不是等待整包返回
        # Accept: text/event-stream 告诉服务端我们期望接收 SSE 格式的数据
        with client.stream("POST", URL, json=payload, headers={"Accept": "text/event-stream"}) as response:
            # 如果返回非 2xx 状态码，直接抛异常而不是继续处理错误响应
            response.raise_for_status()
            print(f"[连接成功] status={response.status_code}\n")
            
            # 改用 iter_text() 获取文本块，再手动按换行符分割（避免 iter_lines 的编码问题）
            buffer = ""
            for text_chunk in response.iter_text():
                buffer += text_chunk
                # 按 \n 分割，保留不完整的最后一行在 buffer 里
                lines = buffer.split("\n")
                # 最后一个元素是不完整的行（或空），保留在 buffer
                buffer = lines[-1]

                
                # 处理完整的行
                for line in lines[:-1]:
                    if not line:
                        continue
                    
                    # SSE 协议的第一部分：事件类型行，格式为 "event: xxx"
                    if line.startswith("event:"):
                        event_type = line.removeprefix("event:").strip()
                        print(f"━━━━━━━━━ 事件类型: {event_type} ━━━━━━━━━")
                    
                    # SSE 协议的第二部分：数据行，格式为 "data: xxx"
                    elif line.startswith("data:"):
                        # 去掉 "data:" 前缀和周围空格
                        body = line.removeprefix("data:").strip()
                        # 反序列化 JSON 字符串为 Python 字典
                        data = json.loads(body)
                        # 用缩进格式重新打印，便于人类阅读
                        print(json.dumps(data, ensure_ascii=False, indent=2))
                        print()  # 打印空行分隔不同的事件


if __name__ == "__main__":
    main()


