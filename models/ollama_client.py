from ollama import chat


MODEL_NAME = "qwen3:8b"


def send_message(messages, tools=None):
    response = chat(
        model=MODEL_NAME,
        messages=messages,
        tools=tools,
    )

    return response
