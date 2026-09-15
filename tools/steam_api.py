import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"


def get_owned_games() -> dict[str, str]:
    """Возвращает словарь с названиями игр и их AppID."""

    if not API_KEY or not STEAM_ID:
        raise ValueError(
            "Не найдены STEAM_API_KEY или STEAM_ID в файле .env"
        )

    params = {
        "key": API_KEY,
        "steamid": STEAM_ID,
        "format": "json",
        "include_appinfo": True,
        "include_played_free_games": True,
    }

    response = requests.get(URL, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    games = data.get("response", {}).get("games", [])

    parsed_games = {}

    for game in games:
        name = game.get("name", "").strip().lower()
        app_id = str(game.get("appid"))

        if name:
            parsed_games[name] = app_id

    return parsed_games


if __name__ == "__main__":
    games = get_owned_games()

    print(f"Собрано игр: {len(games)}\n")

    for name, app_id in sorted(games.items()):
        print(f'"{name}": "{app_id}",')
