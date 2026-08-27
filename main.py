import os
import glob
import difflib
import ctypes
import pyautogui

from comtypes import CLSCTX_ALL
from pathlib import Path
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
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

user_start = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu')
common_start = os.path.expandvars(
    r'%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu')

search_paths = [user_start, common_start]

all_lnks = []

for base_path in search_paths:
    pattern = os.path.join(base_path, '**', '*.lnk')
    found_files = glob.glob(pattern, recursive=True)
    all_lnks.extend(found_files)

clear_lnks = {}

for one_app in all_lnks:
    file_name = os.path.basename(one_app)
    app_name = os.path.splitext(file_name)[0].lower()
    clear_lnks[app_name] = one_app


def get_volume():
    # Инициализируем COM-поток, чтобы Windows не блокировала доступ
    try:
        comtypes.CoInitialize()
    except Exception:
        pass

    # Получаем именно АКТИВНОЕ устройство вывода (по умолчанию)
    enumerator = AudioUtilities.GetDeviceEnumerator()
    # 0 = eRender (вывод), 0 = eConsole (устройство по умолчанию)
    device = enumerator.GetDefaultAudioEndpoint(0, 0)

    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume


def set_volume(level: int):
    try:
        level = int(level)
        volume = get_volume()

        volume.SetMute(False, None)
        target_level = max(0, min(100, level)) / 100.0
        volume.SetMasterVolumeLevelScalar(target_level, None)

        return f"Громкость установленна на {level}%."

    except Exception as e:
        return f"При установке громкости произошла ошибка {str(e)}"


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def get_date():
    return date.today().strftime("%d.%m.%Y")


def open_app(name_app: str):
    # 1. Приводим ввод к нижнему регистру и проверяем локальные алиасы
    clean_input = name_app.strip().lower()
    search_query = APP_ALIASES.get(clean_input, clean_input)

    target_path = None

    # 2. Поиск по частичному вхождению (in)
    for app_name, app_path in clear_lnks.items():
        if search_query in app_name:
            target_path = app_path
            break

    # 3. Нечеткий поиск через difflib, если по 'in' не нашлось
    if not target_path:
        matches = difflib.get_close_matches(
            search_query, clear_lnks.keys(), n=1, cutoff=0.5
        )
        if matches:
            matched_key = matches[0]
            target_path = clear_lnks[matched_key]

    # 4. Проверка: если путь так и не найден
    if not target_path:
        return f"Приложение '{name_app}' не найдено на ПК."

    # 5. Безопасный запуск
    try:
        os.startfile(target_path)
        return f"Приложение '{name_app}' успешно запущено."
    except Exception as e:
        return f"Не удалось запустить '{name_app}'. Ошибка: {str(e)}"


def mute_volume():
    """Включает или выключает звук полностью (Mute)."""
    try:
        volume = get_volume()
        current_mute = volume.GetMute()
        volume.SetMute(not current_mute, None)
        state = "выключен" if not current_mute else "включен"
        return f"Звук {state}."
    except Exception as e:
        return f"Ошибка при переключении звука: {str(e)}"


def collapse_win():
    try:
        pyautogui.hotkey('win', 'd')
        return "Все окна свернуты/развернуты"
    except Exception as e:
        return f"Ошибка при свравчивании/разворачивание окон {str(e)}"


def take_screen():
    try:
        SCREENS_DIR = Path(__file__).resolve().parent / "screens"
        SCREENS_DIR.mkdir(parents=True, exist_ok=True)

        file_name = f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = SCREENS_DIR / file_name

        screen = pyautogui.screenshot()
        screen.save(file_path)
        return f"Скриншот успешно сохранен в: {SCREENS_DIR}"

    except Exception as e:
        return f"Ошибка при создании скриншота: {str(e)}"


available_tools = {
    "get_time": get_time,
    "get_date": get_date,
    "open_app": open_app,
    "set_volume": set_volume,
    "mute_volume": mute_volume,
    "collapse_win": collapse_win,
    "take_screen": take_screen
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
            'name': 'mute_volume',
            'description': 'Полностью выключает или включает звук',
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'collapse_win',
            'description': 'Сворачивает или разворачивает все окна',
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'take_screen',
            'description': 'Делает скриншот экрана и сохраняет в папку',
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
                        'description': 'если пользователь написал название на русском языке, например "дискорд", то нужно перевести это название на английский язык, "discord"'
                    }
                },
                'required': ['name_app']
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'set_volume',
            'description': 'изменяет громкость звука на нужный уровень',
            'parameters': {
                'type': 'object',
                'properties': {
                    'level': {
                        'type': 'integer',
                        'description': 'Принимает число от 1 до 100 для изменения уровня громкости'
                    }
                },
                'required': ['level']
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
