"""调试回调：打印模型调用与工具调用的输入输出。"""

from __future__ import annotations

from typing import Any

from langchain_core.callbacks import BaseCallbackHandler


class DebugTraceCallbackHandler(BaseCallbackHandler):
    """按请求打印模型和工具的输入输出，便于排查链路。"""

    def __init__(self, label: str) -> None:
        self.label = label

    def on_chat_model_start(self, serialized: dict[str, Any], messages: list[list[Any]], **kwargs: Any) -> None:
        model_name = serialized.get("name") or serialized.get("id") or "chat_model"
        print(f"\n[{self.label}][MODEL][START] {model_name}")
        print(f"[{self.label}][MODEL][INPUT] {messages}")

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        print(f"[{self.label}][MODEL][END] {response}")

    def on_chat_model_end(self, response: Any, **kwargs: Any) -> None:
        print(f"[{self.label}][CHAT_MODEL][END] {response}")

    def on_tool_start(self, serialized: dict[str, Any], input_str: str, **kwargs: Any) -> None:
        tool_name = serialized.get("name") or serialized.get("id") or "tool"
        print(f"\n[{self.label}][TOOL][START] {tool_name}")
        print(f"[{self.label}][TOOL][INPUT] {input_str}")

    def on_tool_end(self, output: Any, **kwargs: Any) -> None:
        print(f"[{self.label}][TOOL][END] {output}")

    def on_chain_end(self, outputs: Any, **kwargs: Any) -> None:
        print(f"[{self.label}][CHAIN][END] {outputs}")
