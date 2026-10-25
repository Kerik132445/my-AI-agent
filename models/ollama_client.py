import ollama
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


def list_models():
    """Получить список установленных локальных моделей Ollama."""
    try:
        response = ollama.list()
        return [m.model for m in response.models]
    except Exception as e:
        return [f"Ошибка при получении моделей Ollama: {e}"]


def set_model(model_name: str):
    """Сменить текущую локальную модель."""
    global MODEL_NAME
    MODEL_NAME = model_name
    return MODEL_NAME


def get_current_model():
    """Узнать текущую локальную модель."""
    return MODEL_NAME
