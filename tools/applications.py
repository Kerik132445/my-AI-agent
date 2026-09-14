import os
import glob
import difflib


APP_ALIASES = {
    "телеграм": "telegram",
    "тг": "telegram",
    "дискорд": "discord",
    "дс": "discord",
    "блокнот": "notepad",
    "браузер": "chrome",
    "калькулятор": "calc",
}


user_start = os.path.expandvars(
    r"%APPDATA%\Microsoft\Windows\Start Menu"
)

common_start = os.path.expandvars(
    r"%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu"
)

search_paths = [
    user_start,
    common_start,
]


all_lnks = []

for base_path in search_paths:
    pattern = os.path.join(base_path, "**", "*.lnk")
    found_files = glob.glob(pattern, recursive=True)
    all_lnks.extend(found_files)


clear_lnks = {}

for one_app in all_lnks:
    file_name = os.path.basename(one_app)
    app_name = os.path.splitext(file_name)[0].lower()

    clear_lnks[app_name] = one_app


def open_app(name_app: str):
    clean_input = name_app.strip().lower()

    search_query = APP_ALIASES.get(
        clean_input,
        clean_input
    )

    target_path = None

    for app_name, app_path in clear_lnks.items():
        if search_query in app_name:
            target_path = app_path
            break

    if not target_path:
        matches = difflib.get_close_matches(
            search_query,
            clear_lnks.keys(),
            n=1,
            cutoff=0.5
        )

        if matches:
            matched_key = matches[0]
            target_path = clear_lnks[matched_key]

    if not target_path:
        return f"Приложение '{name_app}' не найдено на ПК."

    try:
        os.startfile(target_path)

        return f"Приложение '{name_app}' успешно запущено."

    except Exception as e:
        return f"Не удалось запустить '{name_app}'. Ошибка: {str(e)}"
