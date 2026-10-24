from dataclasses import dataclass


@dataclass
class ModelToolCall:
    name: str
    arguments: dict
    call_id: str | None = None
    raw_call: object = None


@dataclass
class ModelResponse:
    content: str
    tool_calls: list[ModelToolCall]
    raw_response: object = None
