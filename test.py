import requests

API_KEY = "BE2697BEF0D4225FBA69B7C373A57C2D"
STEAM_ID = "76561199540051807"

url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
params = {
    'key': API_KEY,
    'steamid': STEAM_ID,
    'format': 'json',
    'include_appinfo': True,
    'include_played_free_games': True
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    games = data.get('response', {}).get('games', [])

    if not games:
        print("API всё ещё возвращает пустой список. Проверь, совпадает ли SteamID64!")
    else:
        parsed_games = {}
        for game in games:
            name = game.get('name', '').strip().lower()
            app_id = str(game.get('appid'))

            # Пропускаем инструмент/бета-версии без названий
            if name:
                parsed_games[name] = app_id

        print(f"Собрано игр: {len(parsed_games)}\n")
        print("STEAM_GAMES = {")
        for name, app_id in sorted(parsed_games.items()):
            # Экранируем кавычки в названиях игр, если они есть
            clean_name = name.replace('"', '\\"')
            print(f'    "{clean_name}": "{app_id}",')
        print("}")
else:
    print(f"Ошибка запроса: {response.status_code}")
