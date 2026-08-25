import os
from AppOpener import open as app_open
from ollama import chat
from datetime import datetime, date


APP_ALIASES = {
    "телеграм": "telegram",
    "тг": "telegram",
    "дискорд": "discord",
    "дс": "discord",
    "блокнот": "notepad",
    "браузер": "chrome",
    "калькулятор": "calc",
}


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def get_date():
    return date.today().strftime("%d.%m.%Y")


def open_app(name_app):

    name_clean = name_app.strip().lower().replace('"', '').replace("'", "")

    if not name_clean or name_clean.strip() in [".", "", "none"]:
        return "Ошибка: имя приложения не указано."

    target = APP_ALIASES.get(name_clean, name_clean)

    try:
        os.startfile(target)
        return f"Приложение {name_app} успешно запущено."
    except Exception:
        pass

    try:
        app_open(target, match_closest=True, output=False)
        return f"приложение {name_app} успешно запущено"

    except Exception as e:
        return f"Не удалось запустить '{name_app}'. Ошибка: {str(e)}"


available_tools = {
    "get_time": get_time,
    "get_date": get_date,
    "open_app": open_app,
}


tools_discription = [
    {
        'type': 'function',
        'function': {
            'name': 'get_time',
            'description': 'Возвращает текущее время',
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_date',
            'description': 'Возвращает текущую дату',
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'open_app',
            'description': 'Открывает приложение по их обычным названиям на русском и английском языке',
            'parameters': {
                'type': 'object',
                'properties': {
                    'name_app': {
                        'type': 'string',
                        'description': 'дискорд, телеграм, chrome, блокнот, steam и другие'
                    }
                },
                'required': ['name_app']
            },
        },
    }
]

messages = [
    {
        'role': 'system',
        'content': ("Ты — Гвен, полезный ИИ-ассистент. Отвечай кратко и по делу."),
    }
]

print("Гвен запущена! (Напиши 'выход' или 'exit' для завершения)\n")

while True:
    user_input = input("Я: ".strip())

    if not user_input:
        continue

    if user_input.lower() in ["выход", "exit", "quit"]:
        print("Гвен: До связи!")
        break

    messages.append(
        {
            'role': 'user',
            'content': user_input
        }
    )

    response = chat(
        model='qwen3:8b',
        messages=messages,
        tools=tools_discription,
    )

    messages.append(response.message)

    if response.message.tool_calls:
        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name  # Допустим там находится "get_time"
            arguments = tool_call.function.arguments

            if tool_name in available_tools:
                function = available_tools[tool_name]
                result = function(**arguments)

            else:
                result = f"Ошибка: инструмент '{tool_name}' не найден."

            messages.append({
                'role': 'tool',
                'content': str(result),
            })
        # Повторный запрос к Ollama ПОСЛЕ выполнения всех тулов
        final_response = chat(
            model='qwen3:8b',
            messages=messages,
        )

        messages.append(final_response.message)
        print(f"Гвен: {final_response.message.content}\n")

    else:
        print(f"Гвен: {response.message.content}")
