import requests
import json

BASE_URL = "https://api.opendota.com/api"

def getLastMatchId(player_id):
    url = f"{BASE_URL}/players/{player_id}/recentMatches"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["match_id"]
    return None

def getMatchStats(player_id, match_id):
    url = f"{BASE_URL}/matches/{match_id}"
    response = requests.get(url)

    if response.status_code == 200:
        match_data = response.json()
        for player in match_data["players"]:
            if player.get("account_id") and player['account_id'] == player_id:
                return {
                    "match_id": match_id,
                    "player_id": player_id,
                    "team": "radiant" if player["team_number"] == 0 else "dire",
                    "win": True if match_data["radiant_win"] != player["team_number"] else False,
                    "duration": match_data["duration"],
                    "radiant_score": match_data["radiant_score"],
                    "dire_score": match_data["dire_score"],
                    "hero_id": player["hero_id"],
                    "kills": player["kills"],
                    "deaths": player["deaths"],
                    "assists": player["assists"],
                    "gold_per_min": player["gold_per_min"],
                    "xp_per_min": player["xp_per_min"],
                    "hero_damage": player["hero_damage"],
                    "hero_healing": player["hero_healing"],
                    "tower_damage": player["tower_damage"],
                }
        print("Player not found")
    return None


def saveStatsToJSON(stats, filename="game_statistics.json"):
    """Зберігає статистику у JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4, ensure_ascii=False)
    print(f"Statistics saved to {filename}")
