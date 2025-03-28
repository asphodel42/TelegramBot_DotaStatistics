import requests, json

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
                    "net_worth": player["net_worth"],
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
    try: 
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(stats, file, indent=4, ensure_ascii=False)
        print(f"Statistics saved to {filename}")
    except Exception as e:
        print(f"Error saving statistics: {e}")
    try:
        with open("last_match_id.txt", "w", encoding="utf-8") as file:
            file.write(str(stats["match_id"]))
    except Exception as e:
        print(f"Error saving last match ID: {e}")


def getHeroInfo(hero_id):
    url = "https://api.opendota.com/api/heroes"
    response = requests.get(url)

    if response.status_code == 200:
        heroes = response.json()
        for hero in heroes:
            if hero["id"] == hero_id:
                hero_name = hero["localized_name"]
                hero_image_url = f"https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/{hero['name'].replace('npc_dota_hero_', '')}.png"
                return hero_name, hero_image_url

def getRankImage(player_id):
    ranks = ["Herald", "Guardian", "Crusader", "Archon", "Legend", "Ancient", "Divine", "Immortal"]

    url = f"https://api.opendota.com/api/players/{player_id}"
    response = requests.get(url)

    if response.status_code == 200:
        player_data = response.json()
        rank_tier_medal = player_data["rank_tier"]//10
        rank_tier_star = player_data["rank_tier"]%10

    rank_tier_name = ranks[rank_tier_medal-1]
    
    url_rank = f"https://courier.spectral.gg/images/dota/ranks/rank{rank_tier_medal}.png"
    return rank_tier_name, rank_tier_star, url_rank
