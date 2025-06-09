import os
import requests
import pandas as pd
from datetime import datetime

# ======= CONFIG =======
API_URL = "https://api.prizepicks.com/projections"
CSV_FILENAME = os.path.join("..", "Prop_Data_CSV", "prizepicks_data.csv")

# ======= 1) CONFIGURE REQUEST =======
cookies = {
    'rl_page_init_referrer': '%22%24direct%22',
    '_pxvid': '3758602b-276a-11ef-9fd0-200749dffc2e',
    'intercom-device-id-qmdeaj0t': 'c1d71880-764c-4cbd-a9f1-e867426b45fa',
    '__pxvid': '385d6be2-276a-11ef-a698-0242ac120004',
    '_sp_id.9177': '0bb52ba9-6dbf-4c3c-94df-61bd8bc57c3e.1718052263.3.1718635800.1718539042.101cd900-f834-4704-9fb7-859507be3702',
    'ajs_anonymous_id': '31e2bf14-53cb-42aa-b28b-8ef373863f36',
    'ajs_user_id': '7c614406-798b-4b3c-95d9-12e1c0cccc17',
    'rl_anonymous_id': '%22e87094a3-3f7b-4464-b2b2-652ffc230540%22',
    'intercom-id-qmdeaj0t': '8b6bc254-1257-4d66-92e9-a263b2f2f76c',
    'rl_user_id': '%228d53cd68-8574-45d1-811f-67c072846e1d%22',
    'pxcts': '251a1106-fea9-11ef-aa2c-5d7775896faa',
    '_pxhd': '6d70a2b6f78b1cfd2110e137d19cfa4d06ebdd1d6688314ec21c9d85b8a4d293:d02fc780-65bc-11e9-b971-bb43e5539738',
    'rl_trait': '%7B%22id%22%3A%228d53cd68-8574-45d1-811f-67c072846e1d%22%2C%22address%22%3A%221900%20North%20Kenilworth%20Street%22%2C%22allow_tailed_entries%22%3Atrue%2C%22amount_won%22%3A3382.74%2C%22bonus%22%3Anull%2C%22city%22%3A%22Arlington%22%2C%22cohort_tag%22%3A%22shark%22%2C%22confirmed_at%22%3A%222023-03-04T16%3A26%3A59-05%3A00%22%2C%22country_code%22%3A%22US%22%2C%22created_at%22%3A%222023-03-04T16%3A18%3A50-05%3A00%22%2C%22credit%22%3A28.25%2C%22date_of_birth%22%3A%222005-02-27T00%3A00%3A00-05%3A00%22%2C%22default_entry_amount%22%3Anull%2C%22default_entry_type%22%3Anull%2C%22deposited_amount%22%3A280%2C%22device_vibration%22%3Atrue%2C%22email%22%3A%22willboneshart%40gmail.com%22%2C%22entries_won%22%3A130%2C%22first_name%22%3A%22Will%22%2C%22ftd_promo_type%22%3Anull%2C%22full_name%22%3A%22Will%20Hart%22%2C%22has_confirmed_phone_number%22%3Anull%2C%22idology_validation_state%22%3A%22pending%22%2C%22internal_validation_state%22%3A%22pending%22%2C%22invite_code%22%3A%22PR-692NWPA%22%2C%22is_rotogrinders%22%3Anull%2C%22last_agreed_to_terms_at%22%3A%222023-02-06T02%3A22%3A39-05%3A00%22%2C%22last_entry_created_at%22%3A%222023-03-10T19%3A35%3A19Z%22%2C%22last_name%22%3A%22Hart%22%2C%22last_sign_in_state%22%3A%22VA%22%2C%22needs_tid%22%3Afalse%2C%22notifications%22%3Afalse%2C%22number_of_entries%22%3A303%2C%22otp_status%22%3A%22withdrawal_only%22%2C%22payment_service%22%3A%22nuvei%22%2C%22phone_number%22%3Anull%2C%22postal_code%22%3A%2222205%22%2C%22promo%22%3A0%2C%22push_notification_token%22%3A%22E7FF3E621E85DBAEC54F4C6A3A9117462C336A77AB11B24F39E2D1FD110BBAC4%22%2C%22referral_code%22%3A%22PR-NH3X28H%22%2C%22require_kyc_selfie%22%3Afalse%2C%22role%22%3Anull%2C%22show_balance%22%3Atrue%2C%22sms_opt_in%22%3Afalse%2C%22socure_validation_state%22%3A%22passed%22%2C%22state%22%3A%22VA%22%2C%22terms_accepted%22%3Atrue%2C%22tid_validation%22%3A1%2C%22updated_at%22%3A%222023-03-11T03%3A14%3A50-04%3A00%22%2C%22validation_provider%22%3A%22socure%22%2C%22validation_state%22%3A%22passed%22%2C%22verification_image%22%3Anull%2C%22verification_image_reviewed%22%3Afalse%2C%22verified%22%3Atrue%2C%22withdrawable_credit%22%3A47%2C%22bonus_offer%22%3Anull%2C%22free_entries%22%3A%5B%5D%2C%22customerDashLink%22%3A%22https%3A%2F%2Fapi.prizepicks.com%2Fadmin%2Fusers%2F8d53cd68-8574-45d1-811f-67c072846e1d%22%2C%22prize_points%22%3A1000%2C%22weekly_prize_points%22%3A1000%2C%22last_opened_game_mode%22%3A%22pickem%22%2C%22streak_rmg_treatment_notification%22%3Afalse%2C%22last_opened_state%22%3A%22VA%22%2C%22username%22%3Anull%7D'
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'dnt': '1',
    'if-modified-since': 'Mon, 24 Mar 2025 03:33:20 GMT',
    'origin': 'https://app.prizepicks.com',
    'priority': 'u=1, i',
    'referer': 'https://app.prizepicks.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'x-device-id': 'aa84b224-c1db-4b2e-91f8-0f6bab083db0',
    'x-device-info': 'name=,os=mac,osVersion=10.15.7,isSimulator=false,platform=web,appVersion=web',
}

params = {
    'league_id': '7',
    'per_page': '250',
    'single_stat': 'true',
    'in_game': 'true',
    'state_code': 'VA',
    'game_mode': 'pickem',
}

# ======= HELPERS =======
def build_player_mapping(data):
    mapping = {}
    for item in data.get("included", []):
        if item.get("type") in ["new_player", "player"]:
            pid   = item.get("id")
            attrs = item.get("attributes", {})
            # PrizePicks JSON includes 'team' or 'market' with the player's team code
            team_code = attrs.get("team") or attrs.get("market")
            name = (attrs.get("full_name") or attrs.get("display_name") or attrs.get("name")
                    or f"{attrs.get('first_name','')} {attrs.get('last_name','')}").strip()
            position = attrs.get("position", "Unknown")
            mapping[pid] = {"name": name, "position": position, "team": team_code}
    return mapping

def build_game_mapping(data):
    mapping = {}
    for item in data.get("included", []):
        if item.get("type") == "game":
            gid = item.get("id")
            teams = (item.get("attributes", {})
                        .get("metadata", {})
                        .get("game_info", {})
                        .get("teams", {}))
            mapping[gid] = {"home": teams.get("home", {}).get("abbreviation"),
                            "away": teams.get("away", {}).get("abbreviation")}
    return mapping

def extract_props(data, player_map, game_map):
    rows = []
    today_abbr = datetime.now().strftime("%a")  # e.g. "Thu"

    for proj in data.get("data", []):
        attrs = proj["attributes"]
        rel   = proj["relationships"]

        # — 1) Player —
        pid   = rel.get("new_player", {}).get("data", {}).get("id")
        info  = player_map.get(pid, {})
        pname = info.get("name", "Unknown")
        pos   = info.get("position", "Unknown")

        # — 2) Team & Opponent —
        player_team = info.get("team") or attrs.get("team", "")
        game_id     = rel.get("game", {}).get("data", {}).get("id")
        gm          = game_map.get(game_id, {"home":None,"away":None})
        home, away  = gm["home"], gm["away"]
        if player_team == home:
            opponent, home_away = away, "Home"
        elif player_team == away:
            opponent, home_away = home, "Away"
        else:
            continue  # skip any props where we can't place the team

        # — 3) Prop details & filtering —
        prop_type = attrs.get("stat_display_name", "")
        # drop Combo props
        if "(Combo)" in prop_type:
            continue

        prop_value = attrs.get("line_score")
        odds_raw   = attrs.get("odds_type", "").lower()
        if odds_raw not in ("demon","goblin"):
            odds_cat = "base"
        else:
            # skip demon/goblin
            continue

        # — 4) Start time & today filter —
        raw_time = attrs.get("start_time")
        if not raw_time:
            continue
        try:
            dt   = datetime.fromisoformat(raw_time)
            wd   = dt.strftime("%a")
            tod  = dt.strftime("%-I:%M %p")
            st   = f"{wd} {tod}"
        except ValueError:
            continue

        # only include today's games
        if not st.startswith(today_abbr):
            continue

        # — 5) Append cleaned row —
        rows.append({
            "Player":        pname,
            "Position":      pos,
            "Team":          player_team,
            "Prop Type":     prop_type,
            "Prop Value":    prop_value,
            "Opposing Team": opponent,
            "Odds Category": odds_cat,
            "Start Time":    st
        })

    return rows

def main():
    # Fetch data
    resp = requests.get(API_URL, params=params, cookies=cookies, headers=headers)
    data = resp.json()

    # Build mappings
    pmap = build_player_mapping(data)
    gmap = build_game_mapping(data)

    # Extract props
    rows = extract_props(data, pmap, gmap)

    # DataFrame
    df = pd.DataFrame(rows)

    # Filter base only
    df = df[df["Odds Category"] == "base"]

    # Filter combos and today
    today_abbr = datetime.now().strftime("%a")
    df = df[~df["Prop Type"].str.contains(r"\(Combo\)")]
    df = df[df["Start Time"].str.startswith(today_abbr)]

    # Save
    os.makedirs(os.path.dirname(CSV_FILENAME), exist_ok=True)
    df.to_csv(CSV_FILENAME, index=False, encoding="utf-8")
    print(f"Data saved to {CSV_FILENAME}")

if __name__ == "__main__":
    main()