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

from tools.files import list_files, read_file, open_file, create_file, copy_file, move_file, find_files, delete_file

from memory.memory import (
    add_fact,
    get_facts,
    delete_fact,
    update_fact,
)

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
    "get_facts": get_facts,
    "delete_fact": delete_fact,
    "update_fact": update_fact,
    "list_files": list_files,
    "read_file": read_file,
    "open_file": open_file,
    "create_file": create_file,
    "copy_file": copy_file,
    "move_file": move_file,
    "find_files": find_files,
    "delete_file": delete_file,
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
            "description": "Открыть раздел интерфейса Steam, например библиотеку, магазин, друзья. Не используй этот инструмент для запуска игр.",
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
            "description": "Запустить конкретную игру через Steam. Используй этот инструмент, если пользователь говорит название игры, например Project Zomboid или проджект зомбоид, Squad или сквад, CS2 или кс 2. Не используй для открытия разделов Steam.",
            "parameters": {
                "type": "object",
                "properties": {
                    "game_name": {
                        "type": "string",
                        "description": "Название конкретной игры, например сквад(Squad), проджект зомбоид(Project Zomboid) или майнакрафт(Minecraft), либо её Steam AppID.",
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

    {
        "type": "function",
        "function": {
            "name": "delete_fact",
            "description": "Удалить конкретный факт из долговременной памяти пользователя.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fact": {
                        "type": "string",
                        "description": "Точный факт, который нужно удалить.",
                    },
                },
                "required": ["fact"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Используй этот инструмент, когда пользователь хочет увидеть содержимое конкретной папки. НЕ используй для поиска конкретного файла по имени.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name_dir": {
                        "type": "string",
                        "description": "Название папки",
                    },
                },
                "required": ["name_dir"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Прочитать содержимое конкретного текстового файла. Используй, когда пользователь просит прочитать, показать содержимое или посмотреть код конкретного файла. НЕ используй для получения списка файлов в папке.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь к текстовому файлу",
                    },
                },
                "required": ["path"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "open_file",
            "description": "Открыть файл",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь к файлу",
                    },
                },
                "required": ["path"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Удалить файл",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь к файлу",
                    },
                },
                "required": ["path"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "find_files",
            "description": "Используй этот инструмент, когда пользователь хочет найти конкретный файл по его имени. Можно указать папку, в которой нужно искать. НЕ используй list_files для поиска конкретного файла.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Имя файла",
                    },
                    "directory": {
                        "type": "string",
                        "description": "Папка в которой нужно искать файл",
                    },
                },
                "required": ["name"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Создать файл",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь, по которому нужно создать файл",
                    },
                    "content": {
                        "type": "string",
                        "description": "Содержимое нового файла",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "copy_file",
            "description": "Скопировать файл",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Файл, который нужно скопировать",
                    },
                    "destination": {
                        "type": "string",
                        "description": "место, куда нужно скопировать",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "move_file",
            "description": "Переместить файл из одного места в другое",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Файл, который нужно переместить",
                    },
                    "destination": {
                        "type": "string",
                        "description": "место, куда нужно переместить",
                    },
                },
                "required": ["source", "destination"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "update_fact",
            "description": "Заменить существующий факт пользователя на новый.",
            "parameters": {
                "type": "object",
                "properties": {
                    "old_fact": {
                        "type": "string",
                        "description": "Старый факт, который нужно заменить.",
                    },
                    "new_fact": {
                        "type": "string",
                        "description": "Новый факт, который должен его заменить.",
                    },
                },
                "required": ["old_fact", "new_fact"],
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
