import os
import glob
import difflib
import ctypes
import pyautogui
import time
import webbrowser

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
        # VK_LWIN = 0x5B, VK_D = 0x44
        # Зажимаем Win
        ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
        # Нажимаем D
        ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)
        time.sleep(0.05)
        # Отпускаем D и Win
        ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)

        time.sleep(0.4)

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


def lounch_steam_section(section: str):
    try:
        sections = {
            "библиотека": "steam://open/games",
            "library": "steam://open/games",
            "друзья": "steam://open/friends",
            "friends": "steam://open/friends",
            "магазин": "steam://store",
            "store": "steam://store",
            "настройки": "steam://open/settings",
            "settings": "steam://open/settings"
        }

        clean_section = section.strip().lower()
        uri = sections.get(clean_section, "steam://open/main")

        webbrowser.open(uri)

        return f"Раздел Steam {section} открыт"

    except Exception as e:
        return f"Ошибка при откытии Steam: {str(e)}"


STEAM_GAMES = {
    "100% orange juice": "282800",
    "60 seconds! reatomized": "1012880",
    "911 operator": "503560",
    "american truck simulator": "270880",
    "assassin's creed origins": "582160",
    "baldi's basics classic remastered": "1712830",
    "ball-it hell": "1335940",
    "barro gt": "1990740",
    "battlefield™ 1": "1238840",
    "battlefield™ 6": "2807960",
    "battlefield™ v": "1238810",
    "ben and ed": "395200",
    "bloons td battles 2": "1276390",
    "breathedge": "738520",
    "bridge constructor portal": "684410",
    "buckshot roulette": "2835570",
    "bunny guys!": "2218460",
    "car mechanic simulator 2018": "645630",
    "castle crashers": "204360",
    "catch me!": "1741160",
    "cities: skylines": "255710",
    "clone drone in the danger zone": "597170",
    "clustertruck": "397950",
    "content warning": "2881650",
    "counter-strike 2": "730",
    "crosshair v2": "2250040",
    "cuphead": "268910",
    "cybarian: the time travelling warrior": "928840",
    "dark sector": "29900",
    "dave the diver": "1868140",
    "days gone": "1259420",
    "dayz": "221100",
    "dead in bermuda": "384310",
    "dead island riptide definitive edition": "383180",
    "death stranding director's cut": "1850570",
    "detroit: become human": "1222140",
    "distant space": "569610",
    "don't starve together": "322330",
    "doom": "379720",
    "drawful 2": "442070",
    "drift86": "1070580",
    "duckside playtest": "2887860",
    "dune: spice wars": "1605220",
    "dying light": "239140",
    "dying light 2: reloaded edition": "534380",
    "eets": "6100",
    "empire takeover": "1723790",
    "euro truck simulator 2": "227300",
    "faaast penguin": "2590150",
    "femboy futa house": "3602290",
    "forza horizon 4": "1293830",
    "freddy fazbear's pizzeria simulator": "738060",
    "frozenheim": "1134100",
    "garry's mod": "4000",
    "geometry dash": "322170",
    "getting over it with bennett foddy": "240720",
    "ghost recon breakpoint": "2231380",
    "god of war": "1593500",
    "grand theft auto iii - the definitive edition": "1546970",
    "grand theft auto v enhanced": "3240220",
    "grand theft auto v legacy": "271590",
    "grand theft auto: san andreas - the definitive edition": "1547000",
    "grand theft auto: vice city - the definitive edition": "1546990",
    "grapples galore": "2239140",
    "green hell": "815370",
    "gris": "683320",
    "guntouchables": "2543510",
    "half-life": "70",
    "half-life 2": "220",
    "half-life 2: deathmatch": "320",
    "half-life deathmatch: source": "360",
    "hello neighbor": "521890",
    "hello neighbor: hide and seek": "960420",
    "hentai girl": "878750",
    "hitman world of assassination": "1659040",
    "hitman: absolution": "203140",
    "hitman: sniper challenge": "205930",
    "hotel architect": "1602000",
    "hotline miami": "219150",
    "house flipper": "613100",
    "house flipper remastered collection playtest": "4005190",
    "human fall flat": "477160",
    "icarus": "1149460",
    "isle of jura": "1703140",
    "just cause 3": "225540",
    "kingdom come: deliverance": "379430",
    "level devil": "3242750",
    "machinika museum": "1507190",
    "mafia ii (classic)": "50130",
    "mafia ii: definitive edition": "1030830",
    "mafia: definitive edition": "1030840",
    "marvel's spider-man: miles morales": "1817190",
    "marvel’s spider-man remastered": "1817070",
    "meccha chameleon": "4704690",
    "metro 2033 redux": "286690",
    "metro exodus": "412020",
    "metro exodus enhanced edition": "1449560",
    "mindustry": "1127400",
    "mini thief": "481870",
    "minimalism": "585690",
    "mirror's edge": "17410",
    "mirror's edge™ catalyst": "1233570",
    "moonlighter": "606150",
    "motorslice demo": "3910170",
    "muck": "1625450",
    "my sexy neighbour 2 | prologue": "3814970",
    "one-armed cook": "1977530",
    "one-armed robber": "2551020",
    "otherwar": "1526870",
    "overcome your fears - caretaker": "3550490",
    "payday 2": "218620",
    "peak": "3527290",
    "people playground": "1118200",
    "pico park:classic edition": "461040",
    "plague inc: evolved": "246620",
    "planet coaster": "493340",
    "popgoes arcade": "1986840",
    "poppy playtime": "1721470",
    "portal": "400",
    "portal 2": "620",
    "postal 2": "223470",
    "prison escape simulator: dig out": "3672720",
    "project zomboid": "108600",
    "pubg: battlegrounds": "578080",
    "raft": "648800",
    "ready or not": "1144200",
    "red dead redemption 2": "1174180",
    "remothered: tormented fathers": "633360",
    "rise of the tomb raider": "391220",
    "rpg maker vx ace": "220700",
    "rpg maker xp": "235900",
    "rust": "252490",
    "rust - staging branch": "700580",
    "satisfactory": "526870",
    "schedule i": "3164500",
    "shadow of the tomb raider": "750920",
    "slime rancher": "433340",
    "smart factory tycoon": "1755300",
    "sons of the forest": "1326470",
    "space crew: legendary edition": "1176710",
    "stardew valley": "413150",
    "stickman killing zombie": "2792610",
    "stumble guys": "1677740",
    "subnautica": "264710",
    "super animal royale": "843380",
    "super meat boy": "40800",
    "superliminal": "1049410",
    "supermarket simulator": "2670630",
    "supermarket together": "2709570",
    "teardown": "1167630",
    "tell me why": "1180660",
    "terraria": "105600",
    "the binding of isaac: rebirth": "250900",
    "the escapists": "298630",
    "the escapists 2": "641990",
    "the farmer was replaced": "2060160",
    "the forest": "242760",
    "the jackbox megapicker": "2828500",
    "the last of us™ part i": "1888930",
    "the last of us™ part ii remastered": "2531310",
    "the mean greens - plastic warfare": "360940",
    "the planet crafter": "1284190",
    "the walking dead: the telltale definitive series": "1449690",
    "the witcher 2: assassins of kings enhanced edition": "20920",
    "the witcher 3: wild hunt - complete edition": "292030",
    "the witcher: enhanced edition": "20900",
    "thief simulator": "704850",
    "thief simulator 2": "1332720",
    "tom clancy's ghost recon® wildlands": "460930",
    "totally accurate battle simulator": "508440",
    "totally accurate battlegrounds": "823130",
    "toy tinker simulator": "1510580",
    "trailmakers": "585420",
    "train simulator classic": "24010",
    "ultimate custom night": "871720",
    "ultimate zombie defense": "1035510",
    "unplagued": "3062930",
    "vivaland: dream house": "2606170",
    "wallpaper alive": "2003310",
    "wallpaper engine": "431960",
    "warhammer 40,000: gladius - relics of war": "489630",
    "watch_dogs 2": "447040",
    "weapon of choice": "373600",
    "who's your daddy?!": "427730",
    "wild terra 2: new lands": "1134700",
    "world crafter td": "3098890",
    "zombie gunship survival": "1597480",
}


def launch_steam_game(game_name: str):
    try:
        clean_name = game_name.strip().lower()

        app_id = STEAM_GAMES.get(
            clean_name, clean_name if clean_name.isdigit() else None)

        if not app_id:
            return f"Игра {game_name} не была найдена в библиотеке Steam"

        webbrowser.open(f"steam://rungameid/{app_id}")
        return f"Запуск игры '{game_name}' (AppID: {app_id}) через Steam..."

    except Exception as e:
        return f"Ошибка при запуске игры Steam: {str(e)}"


available_tools = {
    "get_time": get_time,
    "get_date": get_date,
    "open_app": open_app,
    "set_volume": set_volume,
    "mute_volume": mute_volume,
    "collapse_win": collapse_win,
    "take_screen": take_screen,
    "lounch_steam_section": lounch_steam_section,
    "launch_steam_game": launch_steam_game
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
            'description': 'Сворачивает или разворачивает все открытые окна на рабочем столе (Win+D)',
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
    },
    {
        'type': 'function',
        'function': {
            'name': 'launch_steam_game',
            'description': 'Запускает игру по ее названию',
            'parameters': {
                'type': 'object',
                'properties': {
                    'level': {
                        'type': 'string',
                        'description': 'Принимает название игры которое нужно запустить'
                    }
                },
                'required': ['game_name']
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'lounch_steam_section',
            'description': 'Открывает нужную вкладку в Steam: библиотека, друзья, магазин, настройки.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'level': {
                        'type': 'string',
                        'description': 'Название раздела: "библиотека", "друзья", "магазин", "настройки"'
                    }
                },
                'required': ['section']
            },
        },
    },
]

messages = [
    {
        'role': 'system',
        'content': ("Ты — Гвен, полезный ИИ-ассистент для управления ПК."
                    "Если пользователь просит выполнить несколько действий подряд (например, 'сверни окна и открой стим'), ты ДОЛЖНА вызвать все соответствующие функции (tools) последовательно. "
                    "Отвечай кратко и по делу."
                    "КРИТИЧЕСКОЕ ПРАВИЛО: Если пользователь просит выполнить 2 и более действий "
                    "(например: 'сверни окна и открой стим'), ты ОБЯЗАНА вернуть сразу список вызовов функций.\n"
                    "Пример ответа:\n"
                    '[{"name": "collapse_win", "arguments": {}}, {"name": "open_app", "arguments": {"name_app": "steam"}}]'
                    ),
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
