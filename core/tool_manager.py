from tools.system import (
    get_time,
    get_date,
    set_volume,
    mute_volume,
    collapse_win,
)
from tools.steam_api import get_owned_games

from tools.applications import open_app

from tools.screen import take_screen

from memory.memory import add_fact, get_facts

from tools.steam import (
    launch_steam_section,
    launch_steam_game,
)

TOOLS = {
    "get_time": get_time,
    "get_date": get_date,
    "open_app": open_app,
    "set_volume": set_volume,
    "mute_volume": mute_volume,
    "collapse_win": collapse_win,
    "take_screen": take_screen,
    "launch_steam_section": launch_steam_section,
    "launch_steam_game": launch_steam_game,
    "get_owned_games": get_owned_games,
    "add_fact": add_fact,
    "get_facts": get_facts
}


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Получить текущее время.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_facts",
            "description": "Получить сохранённые долгосрочные факты о пользователе из памяти.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_date",
            "description": "Получить текущую дату.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Открыть приложение на компьютере.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name_app": {
                        "type": "string",
                        "description": "Название приложения.",
                    },
                },
                "required": ["name_app"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "set_volume",
            "description": "Установить громкость компьютера в процентах.",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "integer",
                        "description": "Громкость от 0 до 100.",
                    },
                },
                "required": ["level"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "add_fact",
            "description": "Сохранить важный долгосрочный факт о пользователе в память.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fact": {
                        "type": "string",
                        "description": "Факт о пользователе, который нужно сохранить.",
                    },
                },
                "required": ["fact"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "mute_volume",
            "description": "Включить или выключить звук.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "collapse_win",
            "description": "Свернуть или развернуть все окна через Win+D.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "take_screen",
            "description": "Сделать скриншот экрана и сохранить его.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "launch_steam_section",
            "description": "Открыть раздел Steam.",
            "parameters": {
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "description": "Раздел Steam, например библиотека, друзья или магазин.",
                    },
                },
                "required": ["section"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "launch_steam_game",
            "description": "Запустить игру через Steam.",
            "parameters": {
                "type": "object",
                "properties": {
                    "game_name": {
                        "type": "string",
                        "description": "Название игры или Steam AppID.",
                    },
                },
                "required": ["game_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_owned_games",
            "description": "Получить список игр пользователя в Steam.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

]


def execute_tool(tool_name: str, arguments: dict):
    tool = TOOLS.get(tool_name)

    if not tool:
        return f"Инструмент '{tool_name}' не найден."

    try:

        return tool(**arguments)

    except Exception as e:
        return f"Ошибка при выполнении '{tool_name}': {str(e)}"
