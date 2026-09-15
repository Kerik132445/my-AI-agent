from models.ollama_client import send_message
from core.prompts import SYSTEM_PROMPT
from core.tool_manager import TOOL_SCHEMAS, execute_tool
from utils.logger import debug


class Agent:

    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def ask(self, user_message: str):
        self.messages.append({
            "role": "user",
            "content": user_message,
        })

        response = send_message(
            self.messages,
            tools=TOOL_SCHEMAS,
        )

        debug(
            f"Ollama ответила. Tool calls: {bool(response.message.tool_calls)}")

        self.messages.append(response.message)

        if not response.message.tool_calls:
            return response.message.content

        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            debug(f"Выбран инструмент: {tool_name}")
            debug(f"Аргументы: {arguments}")

            result = execute_tool(
                tool_name,
                arguments,
            )

            debug(f"Результат инструмента: {result}")

            self.messages.append({
                "role": "tool",
                "content": str(result),
            })

        final_response = send_message(
            self.messages,
        )

        debug(f"Финальный ответ Ollama: {final_response.message.content}")
        self.messages.append(final_response.message)

        return final_response.message.content
