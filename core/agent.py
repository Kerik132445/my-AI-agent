from core.prompts import SYSTEM_PROMPT
from core.tool_manager import TOOL_SCHEMAS, execute_tool
from utils.logger import debug
import uuid


class Agent:

    def __init__(self, model_client=None):
        self.max_iterations = 20
        self.iterations = 0

        if model_client is None:
            from models.client_factory import get_model_client
            model_client = get_model_client()

        self.model_client = model_client
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def ask(self, user_message: str):
        self.iterations = 0
        self.messages.append({
            "role": "user",
            "content": user_message,
        })

        while self.iterations < self.max_iterations:
            self.iterations += 1
            response = self.model_client(
                self.messages,
                tools=TOOL_SCHEMAS,
            )

            debug(
                f"Модель ответила. Tool calls: "
                f"{bool(response.tool_calls)}"
            )

            for call in response.tool_calls:
                if not call.call_id:
                    call.call_id = f"call_{uuid.uuid4().hex[:8]}"

            assistant_message = {
                "role": "assistant",
                "content": response.content or "",
            }

            if response.tool_calls:
                assistant_message["tool_calls"] = [
                    {
                        "id": call.call_id,
                        "name": call.name,
                        "arguments": call.arguments,
                    }
                    for call in response.tool_calls
                ]

            self.messages.append(assistant_message)

            tool_calls = response.tool_calls

            if not tool_calls:
                return response.content

            for tool_call in tool_calls:
                tool_name = tool_call.name
                arguments = tool_call.arguments

                debug(f"Выбран инструмент: {tool_name}")
                debug(f"Аргументы: {arguments}")

                result = execute_tool(
                    tool_name,
                    arguments,
                )

                debug(f"Результат инструмента: {result}")

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.call_id,
                    "name": tool_name,
                    "content": str(result),
                })
        return "Я не смогла завершить выполнение команды."
