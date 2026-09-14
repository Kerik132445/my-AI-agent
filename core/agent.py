from models.ollama_client import send_message
from core.prompts import SYSTEM_PROMPT
from core.tool_manager import TOOL_SCHEMAS, execute_tool


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

        self.messages.append(response.message)

        if not response.message.tool_calls:
            return response.message.content

        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            result = execute_tool(
                tool_name,
                arguments,
            )

            self.messages.append({
                "role": "tool",
                "content": str(result),
            })

        final_response = send_message(
            self.messages,
        )

        self.messages.append(final_response.message)

        return final_response.message.content
