from datetime import datetime
from pathlib import Path

import pyautogui


def take_screen():
    try:
        screens_dir = Path(__file__).resolve().parent.parent / "screens"
        screens_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = screens_dir / file_name

        screen = pyautogui.screenshot()
        screen.save(file_path)

        return f"Скриншот успешно сохранен в: {screens_dir}"

    except Exception as e:
        return f"Ошибка при создании скриншота: {str(e)}"
