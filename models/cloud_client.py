import json
import os
from openai import OpenAI
from models.base_client import ModelResponse, ModelToolCall
from dotenv import load_dotenv
load_dotenv()

# Чтение настроек подключения
API_KEY = os.getenv("AI_API_KEY", "")
BASE_URL = os.getenv("AI_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("AI_MODEL_NAME", "llama-3.1-8b-instant")

# Инициализация клиента
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def format_messages(messages):
    formatted = []

    for message in messages:
        role = message["role"]

        if role == "tool":
            # Ответ от инструмента
            formatted.append({
                "role": "tool",
                "tool_call_id": message["tool_call_id"],
                "content": message["content"],
            })

        elif role == "assistant" and message.get("tool_calls"):
            # Сообщение ассистента с запросом на вызов инструментов
            groq_tool_calls = []
            for call in message["tool_calls"]:
                groq_tool_calls.append({
                    "id": call["id"],
                    "type": "function",
                    "function": {
                        "name": call["name"],
                        "arguments": json.dumps(call["arguments"]),
                    },
                })

            formatted.append({
                "role": "assistant",
                "content": message.get("content") or "",
                "tool_calls": groq_tool_calls,
            })

        else:
            # Обычные сообщения (user, system, или текстовый assistant)
            formatted.append({
                "role": role,
                "content": message.get("content", ""),
            })

    return formatted


def send_message(messages, tools=None):
    # Если список инструментов передан пустым, OpenAI API ждет None
    openai_tools = tools if tools else None

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=format_messages(messages),
        tools=openai_tools,
    )

    choice = response.choices[0].message

    tool_calls = []
    if choice.tool_calls:
        for call in choice.tool_calls:
            # Превращаем сырую строку JSON от модели в словарь Python
            try:
                args = json.loads(call.function.arguments)
            except json.JSONDecodeError:
                args = {}

            tool_calls.append(
                ModelToolCall(
                    name=call.function.name,
                    arguments=args,
                    call_id=call.id,
                    raw_call=call,
                )
            )

    return ModelResponse(
        content=choice.content or "",
        tool_calls=tool_calls,
        raw_response=response,
    )
