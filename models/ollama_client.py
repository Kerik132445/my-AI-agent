from ollama import chat
from models.base_client import ModelResponse, ModelToolCall


MODEL_NAME = "qwen3:8b"


def send_message(messages, tools=None):
    response = chat(
        model=MODEL_NAME,
        messages=format_messages(messages),
        tools=tools,
    )

    tool_calls = [
        ModelToolCall(
            name=call.function.name,
            arguments=dict(call.function.arguments),
            raw_call=call,
        )
        for call in (response.message.tool_calls or [])
    ]

    return ModelResponse(
        content=response.message.content,
        tool_calls=tool_calls,
        raw_response=response,
    )


def format_messages(messages):
    formatted = []

    for message in messages:
        role = message["role"]

        if role == "tool":
            formatted.append({
                "role": "tool",
                "tool_name": message["name"],
                "content": message["content"],
            })

        elif role == "assistant" and message.get("tool_calls"):
            formatted.append({
                "role": "assistant",
                "content": message.get("content") or "",
                "tool_calls": [
                    {
                        "function": {
                            "name": call["name"],
                            "arguments": call["arguments"],
                        }
                    }
                    for call in message["tool_calls"]
                ],
            })

        else:
            formatted.append({
                "role": role,
                "content": message.get("content", ""),
            })

    return formatted
