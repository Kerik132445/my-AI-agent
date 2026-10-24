from models.base_client import ModelResponse, ModelToolCall


def send_message(messages, tools=None):
    last_message = messages[-1]

    # Если инструмент уже вернул результат,
    # формируем итоговый ответ.
    if last_message["role"] == "tool":
        tool_results = []

        for message in reversed(messages):
            if message["role"] != "tool":
                break

            tool_results.append(message["content"])

        tool_results.reverse()

        return ModelResponse(
            content="Тест пройден. Результаты: " + " ".join(tool_results),
            tool_calls=[],
        )

    # Иначе имитируем запрос модели
    # на получение текущей даты.
    return ModelResponse(
        content="",
        tool_calls=[
            ModelToolCall(
                name="get_date",
                arguments={},
            ),
            ModelToolCall(
                name="get_time",
                arguments={},
            ),
        ],
    )
