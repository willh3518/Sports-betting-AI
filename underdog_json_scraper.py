import os
import time
import requests
import json
import pandas as pd

# -------------------------------
# Discord Notification Settings
# -------------------------------
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1354156047329394818/mCuwO45D3fv1a19YYXXAC1PDZdoEpnjq4UTBJQ-AVLOVDfIuaaPPeWg0sY51WX30gof5"
ALERT_DELAY = 0.5  # seconds between alerts


def send_discord_alert(message, webhook_url=DISCORD_WEBHOOK_URL, max_sleep=60):
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", 1)
        try:
            sleep_time = float(retry_after)
        except ValueError:
            sleep_time = 1
        if sleep_time > max_sleep:
            print(
                f"Rate limited. Retry-After is {sleep_time} seconds, which exceeds max sleep threshold of {max_sleep} seconds. Skipping alert: {message}")
            return
        else:
            print(f"Rate limited. Sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)
            response = requests.post(webhook_url, json=data)
            if response.status_code not in [200, 204]:
                print(f"Failed to send discord alert after retry. Status code: {response.status_code}")
            else:
                print("Discord alert sent after retry:", message)
                time.sleep(ALERT_DELAY)
    elif response.status_code not in [200, 204]:
        print(f"Failed to send discord alert. Status code: {response.status_code}")
    else:
        print("Discord alert sent:", message)
        time.sleep(ALERT_DELAY)

# -------------------------------
# Underdog Fantasy API Settings
# -------------------------------
headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'YOUR_AUTHORIZATION_TOKEN_HERE',  # Replace with your token
    'client-device-id': '9ce12086-f84f-4903-9bc8-bf41270cd465',
    'client-request-id': '31d1c2b3-bdb2-4bc6-baa3-85a453112fe8',
    'client-type': 'web',
    'client-version': '20250319204340',
    'dnt': '1',
    'origin': 'https://underdogfantasy.com',
    'priority': 'u=1, i',
    'referring-link': '',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'user-latitude': '38.4342722',
    'user-longitude': '-78.883452',
}
params = {
    'sport_id': 'NBA',
}
url = "https://api.underdogfantasy.com/v2/pickem_search/search_results"

# -------------------------------
# 1) FETCH JSON DATA
# -------------------------------
response = requests.get(url, headers=headers, params=params)
data = response.json()
print("JSON data fetched from Underdog Fantasy API (in-memory).")


# -------------------------------
# PART A: TEAM & OPPONENT MAPPINGS
# -------------------------------
def build_team_mapping_from_games(data):
    team_map = {}
    games = data.get("games", [])
    for game in games:
        title = game.get("title", "")  # e.g. "LAL @ ORL"
        parts = title.split("@")
        if len(parts) == 2:
            away_abbr = parts[0].strip()  # e.g. "LAL"
            home_abbr = parts[1].strip()  # e.g. "ORL"
            away_team_id = game.get("away_team_id")
            home_team_id = game.get("home_team_id")
            if away_team_id:
                team_map[away_team_id] = away_abbr
            if home_team_id:
                team_map[home_team_id] = home_abbr
    return team_map

def build_opponent_mapping(data, team_map):
    opponent_map = {}
    games = data.get("games", [])
    for game in games:
        home_id = game.get("home_team_id")
        away_id = game.get("away_team_id")
        if home_id and away_id:
            home_abbr = team_map.get(home_id, home_id)
            away_abbr = team_map.get(away_id, away_id)
            opponent_map[home_id] = away_abbr
            opponent_map[away_id] = home_abbr
    return opponent_map

# -------------------------------
# PART B: PLAYER & APPEARANCE MAPPINGS
# -------------------------------
def build_player_map(data, team_map, opponent_map):
    pmap = {}
    players = data.get("players", [])
    for p in players:
        pid = p["id"]
        first_name = p.get("first_name", "")
        last_name = p.get("last_name", "")
        full_name = (f"{first_name} {last_name}").strip() or "Unknown"
        position = p.get("position_display_name", "Unknown")
        team_id = p.get("team_id")
        team_abbr = team_map.get(team_id, "Unknown") if team_id else "Unknown"
        opp_abbr = opponent_map.get(team_id, "Unknown") if team_id else "Unknown"
        pmap[pid] = {
            "name": full_name,
            "position": position,
            "team": team_abbr,
            "opponent": opp_abbr
        }
    return pmap

def build_appearance_map(data):
    amap = {}
    appearances = data.get("appearances", [])
    for app in appearances:
        appearance_id = app["id"]
        player_id = app.get("player_id")
        team_id = app.get("team_id")
        match_id = app.get("match_id")
        amap[appearance_id] = {
            "player_id": player_id,
            "team_id": team_id,
            "match_id": match_id
        }
    return amap

# -------------------------------
# PART C: EXTRACT PROPS (over_under_lines)
# -------------------------------
def extract_props(data, player_map, appearance_map):
    lines = data.get("over_under_lines", [])
    rows = []
    for line_obj in lines:
        over_under = line_obj.get("over_under", {})
        appearance_stat = over_under.get("appearance_stat", {})
        appearance_id = appearance_stat.get("appearance_id")
        display_stat = appearance_stat.get("display_stat", "Unknown")  # e.g. "Points"
        stat_value = line_obj.get("stat_value", "N/A")  # e.g. "28.5"
        app_info = appearance_map.get(appearance_id, {})
        player_id = app_info.get("player_id")
        pinfo = player_map.get(player_id, {})
        player_name = pinfo.get("name", "Unknown")
        position = pinfo.get("position", "Unknown")
        team_abbr = pinfo.get("team", "Unknown")
        opp_abbr = pinfo.get("opponent", "Unknown")
        row = {
            "Player": player_name,
            "Position": position,
            "Team": team_abbr,
            "Opponent": opp_abbr,
            "Prop Type": display_stat,
            "Prop Value": stat_value
        }
        rows.append(row)
    return rows

# -------------------------------
# MAIN PROCESS
# -------------------------------
def main():
    # PART A: Build team & opponent mappings
    team_map = build_team_mapping_from_games(data)
    opponent_map = build_opponent_mapping(data, team_map)

    # PART B: Build player and appearance mappings
    player_map = build_player_map(data, team_map, opponent_map)
    appearance_map = build_appearance_map(data)

    # PART C: Extract props
    rows = extract_props(data, player_map, appearance_map)

    # Create DataFrame, remove duplicates, and sort by Player
    df = pd.DataFrame(rows)
    df.drop_duplicates(inplace=True)
    if "Player" in df.columns:
        df.sort_values(by="Player", inplace=True)

    csv_filename = "underdog_props.csv"

    # Compare with old CSV (if it exists) to detect changes
    if os.path.exists(csv_filename):
        old_df = pd.read_csv(csv_filename)
        old_df.drop_duplicates(inplace=True)
        # Composite key: (Player, Prop Type)
        new_df_indexed = df.set_index(["Player", "Prop Type"])
        old_df_indexed = old_df.set_index(["Player", "Prop Type"])
        for idx, new_row in new_df_indexed.iterrows():
            if idx in old_df_indexed.index:
                old_value = old_df_indexed.loc[idx, "Prop Value"]
                new_value = new_row["Prop Value"]
                if str(old_value) != str(new_value):
                    player, prop_type = idx
                    message = f"🚨 {player} {prop_type} moved from {old_value} ➡️ {new_value}!"
                    send_discord_alert(message)
    else:
        print("No previous CSV file found, skipping change detection.")

    # Save the final CSV for future comparisons
    df.to_csv(csv_filename, index=False, encoding="utf-8")
    print(f"Extracted Underdog props have been saved to {csv_filename}")

if __name__ == "__main__":
    main()
