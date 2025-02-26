import aiohttp, asyncio, csv, os, time, re, random, logging
import unicodedata
from bs4 import BeautifulSoup
import pandas as pd
from selectolax.parser import HTMLParser

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),  # Save logs to file
        logging.StreamHandler()  # Also print logs to console
    ]
)

# 📌 Input & Output Files
INPUT_CSV = "prizepicks_data.csv"
OUTPUT_CSV = "player_stats_with_props.csv"

# 📌 Timeout & Throttling Settings
SCRAPE_TIMEOUT = 8  # Max request time (seconds)
CONCURRENT_REQUESTS = 20  # Limit concurrent HTTP requests
semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS*2)


# 📌 Base URLs for StatMuse Queries
STATMUSE_URL_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-2024-25-season-stats"
STATMUSE_H2H_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-vs-{team}-in-the-2024-25-season"
STATMUSE_HIT_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-games-with-more-than-{value}-{prop}-this-season"
STATMUSE_LAST_10_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-vs-{team}-in-last-10-matchups"

# 📌 Team Name Mapping for StatMuse Compatibility
TEAM_NAME_MAPPING = {
    "ATL": "atlanta", "BOS": "boston", "BKN": "brooklyn", "CHA": "charlotte",
    "CHI": "chicago", "CLE": "cleveland", "DAL": "dallas", "DEN": "denver",
    "DET": "detroit", "GSW": "golden-state", "HOU": "houston", "IND": "indiana",
    "LAC": "la-clippers", "LAL": "la-lakers", "MEM": "memphis", "MIA": "miami",
    "MIL": "milwaukee", "MIN": "minnesota", "NOP": "new-orleans", "NYK": "new-york",
    "OKC": "oklahoma-city", "ORL": "orlando", "PHI": "philadelphia", "PHX": "phoenix",
    "POR": "portland", "SAC": "sacramento", "SAS": "san-antonio", "TOR": "toronto",
    "UTA": "utah", "WAS": "washington"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

CACHE = {}  # Stores previously fetched HTML responses to prevent duplicate requests

# Load Proxies & Setup Rotation
async def load_proxies():
    with open("working_proxies.txt", "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

PROXIES = asyncio.run(load_proxies())  # Load proxies synchronously at startup  # Load proxies asynchronously

async def get_proxy():
    global PROXIES
    """Rotates proxies dynamically."""
    while True:
        if not PROXIES:
            logging.error("🚨 No working proxies left! Reloading proxies...")

            PROXIES = await load_proxies()
        yield random.choice(PROXIES)

def clean_player_name(name):
    """Removes periods, accents, and ensures proper capitalization."""
    name = name.replace(".", "")  # Remove periods
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8")  # Remove accents
    return name.title()  # Capitalize properly

async def fetch_html(session, url, max_retries=5):
    if url in CACHE:
        logging.info(f"🔄 Using cached response for: {url}")
        return CACHE[url]

    headers = {
        "User-Agent": random.choice(USER_AGENTS),  # Rotate headers
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }

    async with semaphore:
        for attempt in range(max_retries):
            proxy = await get_proxy().__anext__()
            proxy_url = f"http://{proxy}"

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=headers, timeout=SCRAPE_TIMEOUT, proxy=proxy_url) as response:
                        if response.status == 200:
                            html = await response.text()
                            CACHE[url] = html  # ✅ Cache result
                            return html
                        elif response.status in [403, 429]:
                            logging.warning(f"⚠️ Rate limited on {proxy}. Retrying...")
                            await asyncio.sleep((2 ** attempt) + random.uniform(0.5, 2.0))
                except Exception as e:
                    logging.warning(f"❌ Proxy {proxy} failed: {e}")

        logging.error(f"❌ Max retries reached for {url}. Skipping...")
        return None

async def batch_scrape(urls, scrape_function):
    """Efficiently process multiple URLs in parallel."""
    tasks = [scrape_function(url) for url in urls]
    return await asyncio.gather(*tasks)

def extract_stats(html):
    """Parses HTML and extracts player stats from the first table."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("table")  # Faster than find()
    if not table:
        return {}

    headers = [th.get_text(strip=True) for th in table.select("th")]
    values = [td.get_text(strip=True) for td in table.select("td")]

    valid_stats = ["GP", "PPG", "RPG", "APG", "SPG", "BPG", "FGM", "FGA", "3PM", "3PA", "FTM", "FTA", "OREB", "DREB",
                   "TPG"]

    return {headers[i]: values[i] for i in range(len(headers)) if headers[i] in valid_stats}

async def extract_prop_hit_percentage(html):
    """Extracts prop hit percentage from StatMuse results."""
    soup = BeautifulSoup(html, "lxml")
    stat_text = soup.find("h1")
    if not stat_text:
        return 0

    text = stat_text.text
    match = re.search(r"(\d+) games", text)
    return int(match.group(1)) if match else 0

def extract_h2h_stats(html):
    """Parses H2H stats using selectolax, extracts 'Games Played' and opponent name."""
    tree = HTMLParser(html)

    # ✅ Extract the full header text
    header_element = tree.css_first("h1")
    header_text = header_element.text(strip=True) if header_element else ""

    # ✅ Extract Opponent Name from Header
    opponent_match = re.search(r"vs (.*?) in", header_text, re.IGNORECASE)
    opponent_name = opponent_match.group(1) if opponent_match else "Unknown"

    # ✅ Extract "Games Played" from the Header
    games_played_match = re.search(r"in (\d+) game", header_text)
    games_played = games_played_match.group(1) if games_played_match else "N/A"

    # ✅ Extract table stats
    table = tree.css_first("table")
    if not table:
        return {"GP": games_played, "Opponent": opponent_name}  # Store Opponent Name in Output

    headers = [th.text(strip=True) for th in table.css("th")]

    # ✅ Handling multi-game case (Average row exists)
    rows = table.css("tr")
    if len(rows) > 2:
        last_row = rows[-2].css("td")
    else:
        last_row = rows[1].css("td")

    values = [td.text(strip=True) for td in last_row]

    # ✅ Map stats correctly
    stat_mapping = {"PTS": "PPG", "REB": "RPG", "AST": "APG", "STL": "SPG", "BLK": "BPG", "TOV": "TPG"}
    stats = {stat_mapping.get(headers[i], headers[i]): values[i] for i in range(len(headers))}

    # ✅ Add Opponent Name and "Games Played" to Stats
    stats["GP"] = games_played
    stats["Opponent"] = opponent_name  # Ensure Opponent is Stored

    return stats

async def scrape_player_stats(player_name, session):
    """Scrapes season stats for a single player."""
    url = STATMUSE_URL_TEMPLATE.format(player=player_name.replace(" ", "-").lower())
    html = await fetch_html(session, url)
    return extract_stats(html) if html else {}

async def scrape_h2h_stats(player_name, opposing_team, session):
    if not opposing_team:
        return {}

    formatted_player = player_name.replace(" ", "-").lower()
    formatted_team = TEAM_NAME_MAPPING.get(opposing_team, opposing_team).replace(" ", "-").lower()
    url = STATMUSE_H2H_TEMPLATE.format(player=formatted_player, team=formatted_team)

    if url in CACHE:
        logging.info(f"🔄 Using cached H2H stats for {player_name} vs {opposing_team}")
        return extract_h2h_stats(CACHE[url])

    html = await fetch_html(session, url)
    return extract_h2h_stats(html) if html else {}

async def scrape_last_10_stats(player_name, opposing_team, session):
    """Scrapes Last 10 Matchups stats for a player vs an opponent (individual game logs)."""
    if not opposing_team:
        return [], {}

    formatted_player = player_name.replace(" ", "-").lower()
    formatted_team = TEAM_NAME_MAPPING.get(opposing_team, opposing_team).replace(" ", "-").lower()
    url = STATMUSE_LAST_10_TEMPLATE.format(player=formatted_player, team=formatted_team)

    html = await fetch_html(session, url)
    if not html:
        return [], {}

    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("table")
    if not table:
        return [], {}

    rows = table.select("tr")
    if len(rows) < 2:
        return [], {}

    headers = [th.get_text(strip=True) for th in table.select("th")]

    # ✅ Extract all game logs, excluding the last row
    stats_list = []
    for row in rows[1:-1]:  # Exclude the last row (average stats)
        values = [td.get_text(strip=True) for td in row.select("td")]
        stats = {headers[i]: values[i] for i in range(len(headers))}
        stats_list.append(stats)

    # ✅ Extract the last row separately as the **average row**
    avg_values = [td.get_text(strip=True) for td in rows[-1].select("td")]
    avg_stats = {headers[i]: avg_values[i] for i in range(len(headers))}

    return stats_list, avg_stats  # ✅ Return both game logs & the average stats

def calculate_last_10_hit_percentage(game_logs, prop_type, threshold):
    """Calculates the percentage of games where a player hit the given prop threshold."""
    prop_mapping = {
        "points": "PTS", "assists": "AST", "rebounds": "REB",
        "steals": "STL", "blocks": "BLK", "fg made": "FGM",
        "fg attempted": "FGA", "3-pt made": "3PM", "3-pt attempted": "3PA",
        "turnovers": "TOV", "offensive rebounds": "OREB", "defensive rebounds": "DREB",
        "pts+asts": ["PTS", "AST"], "pts+rebs": ["PTS", "REB"],
        "pts+rebs+asts": ["PTS", "REB", "AST"], "rebs+asts": ["REB", "AST"],
        "blks+stls": ["BLK", "STL"]
    }

    stat_key = prop_mapping.get(prop_type.lower())
    if not stat_key:
        return 0  # Skip unsupported props

    hit_count = 0
    total_games = len(game_logs)

    for game in game_logs:
        if isinstance(stat_key, list):
            stat_value = sum(float(game.get(k, 0)) for k in stat_key)
        else:
            stat_value = float(game.get(stat_key, 0))

        if stat_value >= threshold:
            hit_count += 1

    return round((hit_count / total_games) * 100, 1) if total_games else 0

async def scrape_prop_hit_percentage(player_name, prop, value, session):
    formatted_player = player_name.replace(" ", "-").lower()
    formatted_prop = prop.replace(" ", "-").lower()
    url = STATMUSE_HIT_TEMPLATE.format(player=formatted_player, value=value, prop=formatted_prop)

    if url in CACHE:
        logging.info(f"🔄 Using cached prop hit percentage for {player_name}: {prop} {value}")
        return await extract_prop_hit_percentage(CACHE[url])

    html = await fetch_html(session, url)
    return await extract_prop_hit_percentage(html) if html else 0

async def process_unique_players(unique_players, player_team_mapping):
    """Processes season stats, H2H, and last 10 matchups for unique players."""
    results = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=10)) as session:
        tasks = [
            asyncio.gather(
                scrape_player_stats(player, session),
                scrape_h2h_stats(player, player_team_mapping.get(player, ""), session),
                scrape_last_10_stats(player, player_team_mapping.get(player, ""), session)
            )
            for player in unique_players
        ]
        responses = await asyncio.gather(*tasks)

    for player, (season_stats, h2h_stats, last_10_stats) in zip(unique_players, responses):
        results.append((player, season_stats, h2h_stats, last_10_stats))

    return results

async def process_player_props(player_prop_combinations, season_stats_mapping):
    """Processes prop hit percentages for player-prop combinations."""
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [
            scrape_prop_hit_percentage(player, prop, value, session)
            for player, prop, value in player_prop_combinations
        ]
        games_hit_list = await asyncio.gather(*tasks)

    for (player, prop, value), games_hit in zip(player_prop_combinations, games_hit_list):
        total_games_played = int(season_stats_mapping.get(player, {}).get("GP", 0))
        hit_percentage = round((games_hit / total_games_played) * 100, 1) if games_hit and total_games_played else 0

        results.append({
            "Player": player,
            "Prop": f"{prop.capitalize()} {value}",
            "Games Hit": games_hit,
            "Hit Percentage": f"{hit_percentage}%",
            "Games Played": total_games_played,
        })

    return results

async def process_last_10_hit_percentage(unique_players, player_prop_combinations, player_team_mapping):
    """Scrapes last 10 game logs and computes hit percentage for props."""
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [
            scrape_last_10_stats(player, player_team_mapping.get(player, ""), session)
            for player in unique_players
        ]
        game_logs_list = await asyncio.gather(*tasks)

    game_logs_mapping = {player: logs for player, logs in zip(unique_players, game_logs_list)}

    for player, prop, value in player_prop_combinations:
        game_logs = game_logs_mapping.get(player, [])
        last_10_hit_percentage = calculate_last_10_hit_percentage(game_logs, prop, value)
        results.append({
            "Player": player,
            "Prop": f"{prop.capitalize()} {value}",
            "Last 10 Matchup Hit %": f"{last_10_hit_percentage}%"
        })

    return results

async def save_to_csv(season_stats, prop_results, player_team_mapping):
    """Saves processed player stats and prop data to CSV efficiently using Pandas, including H2H Prop Hit Value."""
    logging.info(f"📄 Writing results to {OUTPUT_CSV}...")

    output_data = []

    # ✅ Sort season_stats alphabetically by player name
    sorted_season_stats = sorted(season_stats, key=lambda x: x[0])

    for player, season_data, h2h_data, last_10_data, avg_stats in sorted_season_stats:
        opponent_name = player_team_mapping.get(player, "Unknown")  # Use team mapping

        # ✅ Season Stats Row
        output_data.append([
            player, "Season Stats", "", "", "", "", season_data.get("GP", "N/A"), season_data.get("PPG", "N/A"),
            season_data.get("RPG", "N/A"), season_data.get("APG", "N/A"), season_data.get("SPG", "N/A"),
            season_data.get("BPG", "N/A"), season_data.get("FGM", "N/A"), season_data.get("FGA", "N/A"),
            season_data.get("3PM", "N/A"), season_data.get("3PA", "N/A"), season_data.get("FTM", "N/A"),
            season_data.get("FTA", "N/A"), season_data.get("OREB", "N/A"), season_data.get("DREB", "N/A"),
            season_data.get("TPG", "N/A")
        ])

        # ✅ H2H Stats Row
        if h2h_data.get("GP") != "N/A":
            output_data.append([
                "", f"H2H vs {opponent_name}", "", "", "", "", h2h_data.get("GP", "N/A"),
                h2h_data.get("PPG", "N/A"), h2h_data.get("RPG", "N/A"), h2h_data.get("APG", "N/A"),
                h2h_data.get("SPG", "N/A"), h2h_data.get("BPG", "N/A"), h2h_data.get("FGM", "N/A"),
                h2h_data.get("FGA", "N/A"), h2h_data.get("3PM", "N/A"), h2h_data.get("3PA", "N/A"),
                h2h_data.get("FTM", "N/A"), h2h_data.get("FTA", "N/A"), h2h_data.get("OREB", "N/A"),
                h2h_data.get("DREB", "N/A"), h2h_data.get("TPG", "N/A")
            ])

        # ✅ Handle last 10 matchups correctly
        games_played = len(last_10_data)-1 if isinstance(last_10_data, list) else 0

        # Extract the dictionary where NAME == 'Average'
        average_row = next((entry for entry in last_10_data if entry.get('NAME') == 'Average'), None)

        if games_played > 0:
            output_data.append([
                "", f"Last {len(last_10_data)-1} vs {player_team_mapping.get(player, 'Unknown')}", "", "", "", "",
                len(last_10_data)-1,
                average_row.get("PTS", "N/A"), average_row.get("REB", "N/A"),
                average_row.get("AST", "N/A"), average_row.get("STL", "N/A"),
                average_row.get("BLK", "N/A"), average_row.get("FGM", "N/A"),
                average_row.get("FGA", "N/A"), average_row.get("3PM", "N/A"),
                average_row.get("3PA", "N/A"), average_row.get("FTM", "N/A"),
                average_row.get("FTA", "N/A"), average_row.get("OREB", "N/A"),
                average_row.get("DREB", "N/A"), average_row.get("TOV", "N/A")
            ])

        # ✅ Prop Results Rows with H2H Prop Hit Value
        sorted_prop_results = sorted(prop_results, key=lambda x: x["Player"])
        for prop_data in sorted_prop_results:
            if prop_data["Player"] == player:
                prop_value = float(re.search(r"(\d+\.?\d*)$", prop_data["Prop"]).group(1))  # Extract prop value
                prop_type = prop_data["Prop"].split()[0].lower()  # Extract prop type

                # ✅ Find H2H stats for this player and opponent
                h2h_stat = 0
                if h2h_data and opponent_name != "Unknown":
                    if prop_type == "points":
                        h2h_stat = float(h2h_data.get("PPG", 0))
                    elif prop_type == "assists":
                        h2h_stat = float(h2h_data.get("APG", 0))
                    elif prop_type == "rebounds":
                        h2h_stat = float(h2h_data.get("RPG", 0))
                    elif prop_type == "steals":
                        h2h_stat = float(h2h_data.get("SPG", 0))
                    elif prop_type == "blocks":
                        h2h_stat = float(h2h_data.get("BPG", 0))
                    elif prop_type == "fg made":
                        h2h_stat = float(h2h_data.get("FGM", 0))
                    elif prop_type == "fg attempted":
                        h2h_stat = float(h2h_data.get("FGA", 0))
                    elif prop_type == "3-pt made":
                        h2h_stat = float(h2h_data.get("3PM", 0))
                    elif prop_type == "3-pt attempted":
                        h2h_stat = float(h2h_data.get("3PA", 0))
                    elif prop_type == "turnovers":
                        h2h_stat = float(h2h_data.get("TPG", 0))
                    elif prop_type == "offensive rebounds":
                        h2h_stat = float(h2h_data.get("OREB", 0))
                    elif prop_type == "defensive rebounds":
                        h2h_stat = float(h2h_data.get("DREB", 0))
                    elif prop_type == "pts+asts":
                        h2h_stat = float(h2h_data.get("PPG", 0)) + float(h2h_data.get("APG", 0))
                    elif prop_type == "pts+rebs":
                        h2h_stat = float(h2h_data.get("PPG", 0)) + float(h2h_data.get("RPG", 0))
                    elif prop_type == "pts+rebs+asts":
                        h2h_stat = float(h2h_data.get("PPG", 0)) + float(h2h_data.get("RPG", 0)) + float(h2h_data.get("APG", 0))
                    elif prop_type == "rebs+asts":
                        h2h_stat = float(h2h_data.get("RPG", 0)) + float(h2h_data.get("APG", 0))
                    elif prop_type == "blks+stls":
                        h2h_stat = float(h2h_data.get("BPG", 0)) + float(h2h_data.get("SPG", 0))

                # ✅ Compare and set "H2H Prop Hit Value"
                h2h_hit_value = "Yes" if h2h_stat >= prop_value else "No"

                output_data.append([
                    "", prop_data["Prop"], prop_data["Games Hit"], prop_data["Hit Percentage"],
                    h2h_hit_value, prop_data["Last 10 Matchup Hit %"], "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                ])


    # ✅ Convert list to Pandas DataFrame
    df_output = pd.DataFrame(output_data, columns=[
        "Player", "Prop", "Games Hit", "Hit Percentage", "H2H Prop Hit Value", f"Last {games_played} Matchup Hit %",
        "Games Played", "PPG", "RPG", "APG", "SPG", "BPG", "FGM", "FGA", "3PM", "3PA", "FTM", "FTA",
        "OREB", "DREB", "TPG"
    ])

    # ✅ Save to CSV
    df_output.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    logging.info(f"✅ CSV successfully saved to {OUTPUT_CSV}.")

async def scrape_and_process(unique_players, player_team_mapping, player_prop_combinations):
    season_stats = []
    prop_results = []
    last_10_hit_results = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=10)) as session:
        player_tasks = [
            asyncio.gather(
                scrape_player_stats(player, session),
                scrape_h2h_stats(player, player_team_mapping.get(player, ""), session),
                scrape_last_10_stats(player, player_team_mapping.get(player, ""), session)  # OLD LINE TO FIX
            )
            for player in unique_players
        ]

        prop_tasks = [
            scrape_prop_hit_percentage(player, prop, value, session)
            for player, prop, value in player_prop_combinations
        ]

        last_10_tasks = [
            scrape_last_10_stats(player, player_team_mapping.get(player, ""), session)  # OLD LINE TO FIX
            for player in unique_players
        ]

        # Run all tasks concurrently
        player_results, prop_results_raw, last_10_logs_list = await asyncio.gather(
            asyncio.gather(*player_tasks),
            asyncio.gather(*prop_tasks),
            asyncio.gather(*last_10_tasks)
        )

        # Process player results
        for player, (season_data, h2h_data, last_10_result) in zip(unique_players, player_results):
            last_10_data, avg_stats = last_10_result  # ✅ FIXED: Store the avg stats separately
            season_stats.append((player, season_data, h2h_data, last_10_data, avg_stats))  # ✅ Added avg_stats

        # ✅ FIX: Create season_stats_mapping before using it
        season_stats_mapping = {player: stats for player, stats, _, _, _ in season_stats}

        # ✅ Corrected dictionary comprehension
        game_logs_mapping = {player: (logs, avg_stats) for player, (logs, avg_stats) in
                             zip(unique_players, last_10_logs_list)}

        for (player, prop, value) in player_prop_combinations:
            logs, _ = game_logs_mapping.get(player, ([], {}))  # ✅ Extract only logs, ignore avg_stats
            last_10_hit_percentage = calculate_last_10_hit_percentage(logs, prop, value)
            last_10_hit_results.append({
                "Player": player,
                "Prop": f"{prop} {value}",
                "Last 10 Matchup Hit %": f"{last_10_hit_percentage}%"
            })

        # Process prop results
        for (player, prop, value), games_hit in zip(player_prop_combinations, prop_results_raw):
            total_games = int(season_stats_mapping.get(player, {}).get("GP", 1))
            hit_percentage = round((games_hit / total_games) * 100, 1) if total_games > 0 else 0
            last_10_hit_percentage = next((x["Last 10 Matchup Hit %"] for x in last_10_hit_results if
                                           x["Player"] == player and x["Prop"] == f"{prop} {value}"), "N/A")

            prop_results.append({
                "Player": player,
                "Prop": f"{prop} {value}",
                "Games Hit": games_hit,
                "Hit Percentage": f"{hit_percentage}%",
                "Games Played": total_games,
                "H2H Prop Hit Value": "Yes" if hit_percentage > 50 else "No",  # Keeping H2H logic intact
                "Last 10 Matchup Hit %": last_10_hit_percentage
            })
    return season_stats, prop_results

async def scrape_all_players():
    start_time = time.time()
    if not os.path.exists(INPUT_CSV):
        logging.error(f"🚨 Input CSV '{INPUT_CSV}' not found!")
        return
    logging.info(f"🔍 Reading player data from {INPUT_CSV}...")
    unique_players = set()
    player_prop_combinations = []
    player_team_mapping = {}
    df = pd.read_csv(INPUT_CSV, dtype={"Prop Value": str})  # Ensures numeric values are read as strings
    for _, row in df.iterrows():
        player_name = clean_player_name(row.get("Player", "").strip())
        if "+" in player_name:
            continue
        prop_type = row.get("Prop Type", "").strip()
        prop_value = str(row.get("Prop Value", "")).strip()
        opposing_team = row.get("Opposing Team", "").strip()
        if player_name:
            unique_players.add(player_name)
            player_team_mapping[player_name] = TEAM_NAME_MAPPING.get(opposing_team, opposing_team)
            # ✅ Skip unsupported props to improve speed
            unsupported_props = {"dunks", "blocked shots", "fantasy score"}
            if prop_type.lower() not in unsupported_props and prop_value.replace('.', '', 1).isdigit():
                player_prop_combinations.append((player_name, prop_type, float(prop_value)))
    if not unique_players:
        logging.warning("⚠️ No valid player names found in CSV.")
        return
    season_stats, prop_results = await scrape_and_process(unique_players, player_team_mapping, player_prop_combinations)
    await save_to_csv(season_stats, prop_results, player_team_mapping)
    logging.info(f"✅ Scraping complete! Stats saved to '{OUTPUT_CSV}'.")
    logging.info(f"🚀 Execution completed in {time.time() - start_time:.2f} seconds.")

async def worker(queue, session, results):
    """Processes player requests in batches with independent task execution."""
    while not queue.empty():
        player, opponent = await queue.get()

        # Create independent tasks for each scraping function
        season_task = asyncio.create_task(scrape_player_stats(player, session))
        h2h_task = asyncio.create_task(scrape_h2h_stats(player, opponent, session))
        last_10_task = asyncio.create_task(scrape_last_10_stats(player, opponent, session))

        # Collect results as they finish
        season_stats = await season_task
        h2h_stats = await h2h_task
        last_10_stats = await last_10_task

        results.append((player, (season_stats, h2h_stats, last_10_stats)))

        await asyncio.sleep(random.uniform(0.2, 0.8))  # ✅ Keep small delay for safety

if __name__ == "__main__":
    asyncio.run(scrape_all_players())
