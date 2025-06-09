import aiohttp
import asyncio
import random
import logging
import os
import unidecode
from datetime import datetime, date
from bs4 import BeautifulSoup
import requests
from typing import Optional, Tuple, Dict

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROXY_FILE = os.path.join(BASE_DIR, "working_proxies.txt")
SCRAPE_TIMEOUT = 8
WEATHER_UNITS = "imperial"
OWM_API_KEY = "6db6b866a5090601c4b967df2d80d5dc"

# Concurrency Control
semaphore = asyncio.Semaphore(40)

# Team name mappings
TEAM_ABBREV_MAP = {
    "ATL": "Braves", "ARI": "Diamondbacks", "BAL": "Orioles", "BOS": "Red Sox", "CHC": "Cubs",
    "CIN": "Reds", "CLE": "Guardians", "COL": "Rockies", "CHW": "White Sox", "DET": "Tigers",
    "HOU": "Astros", "KC": "Royals", "LAA": "Angels", "LAD": "Dodgers", "MIA": "Marlins",
    "MIL": "Brewers", "MIN": "Twins", "NYM": "Mets", "NYY": "Yankees", "ATH": "Athletics",
    "PHI": "Phillies", "PIT": "Pirates", "SD": "Padres", "SEA": "Mariners", "SFG": "Giants",
    "STL": "Cardinals", "TBR": "Rays", "TEX": "Rangers", "TOR": "Blue Jays", "WSN": "Nationals"
}

# Name corrections for player names
NAME_CORRECTIONS = {
    "Dj Lemahieu": "DJ LeMahieu",
    "Jp Crawford": "JP Crawford",
    "Tj Friedl": "TJ Friedl",
    "Cj Abrams": "CJ Abrams",
    "Andrew Mccutchen": "Andrew McCutchen",
    "Matt Mclain": "Matt McLain"
}

# Proxy Management
async def load_proxies():
    """Loads proxies from file asynchronously."""
    try:
        with open(PROXY_FILE, "r") as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        if not proxies:
            logging.error("No proxies found in the file!")
        return proxies
    except FileNotFoundError:
        logging.error(f"Proxy file '{PROXY_FILE}' not found!")
        return []

PROXIES = asyncio.run(load_proxies())

async def get_proxy():
    """Rotates proxies dynamically."""
    global PROXIES
    while True:
        if not PROXIES:
            logging.warning("Reloading proxies...")
            PROXIES = await load_proxies()
        yield random.choice(PROXIES)

# Web Scraping
async def fetch_html(url: str, max_retries: int = 5) -> Optional[str]:
    """Fetches HTML from a given URL using rotating proxies."""
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]),
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
                            soup = BeautifulSoup(html, "html.parser")
                            no_results_element = soup.find("span",
                                                           class_="my-[1em] [&>a]:underline [&>a]:text-team-secondary whitespace-pre-wrap text-pretty")
                            if no_results_element and "I understood your question, but there were no results." in no_results_element.text:
                                logging.error(f"No results found at {url}. Skipping further attempts immediately.")
                                return None
                            return html
                        elif response.status in [403, 429]:
                            logging.warning(f"Rate limited ({response.status}) on {proxy}. Retrying...")
                            await asyncio.sleep((2 ** attempt) + random.uniform(0.5, 2.0))
                except Exception as e:
                    logging.warning(f"Proxy {proxy} failed: {e}")

        logging.error(f"Max retries reached for {url}. Skipping...")
        return None

# Name Normalization
def normalize_name(name: str) -> str:
    """Normalizes player names by removing accents, periods, and applying corrections."""
    name = str(name)
    name = unidecode.unidecode(name)
    name = name.replace(".", "").replace("Jr", "").replace("II", "").replace("III", "").strip()
    name = " ".join(name.split())
    name = name.title()
    return NAME_CORRECTIONS.get(name, name)

# Date Parsing
def parse_schedule_date(col_str: str) -> Optional[date]:
    """Parse a string like 'Wed 5/28' → date(TODAY.year, 5, 28)."""
    try:
        md = col_str.strip().split()[-1]
        m_str, d_str = md.split("/")
        return date(datetime.now().year, int(m_str), int(d_str))
    except Exception:
        return None

def manual_parse_time(raw_time: str, sched_date: date) -> Tuple[Optional[datetime], Optional[str]]:
    """Parse time string and return (datetime_obj, formatted_string)."""
    tokens = raw_time.split()
    if len(tokens) >= 3 and tokens[0].isalpha() and ":" in tokens[1]:
        tstr = " ".join(tokens[1:])
    else:
        tstr = raw_time.strip()
    try:
        time_part = tstr.upper()
        hour_min, ampm = time_part.split()
        hour_str, min_str = hour_min.split(":")
        hour = int(hour_str)
        minute = int(min_str)
        if ampm == "PM" and hour != 12:
            hour += 12
        if ampm == "AM" and hour == 12:
            hour = 0
        dt_obj = datetime(sched_date.year, sched_date.month, sched_date.day, hour, minute)
        game_time_str = dt_obj.strftime("%Y-%m-%d %I:%M %p")
        return dt_obj, game_time_str
    except Exception:
        return None, None

# Weather Analysis
def compute_wind_effect(orientation_deg: float, wind_deg: float) -> Tuple[str, str]:
    """Compute wind effects on pitchers and hitters based on field orientation."""
    if wind_deg is None:
        return ("Unknown (no wind data)", "Unknown (no wind data)")

    rel = (wind_deg - orientation_deg + 360) % 360
    if (rel >= 315) or (rel <= 45):
        return (
            "Headwind: balls into the air will be knocked down - helps pitchers.",
            "Headwind: balls in the air won't carry - hinders hitters."
        )
    if 135 <= rel <= 225:
        return (
            "Tailwind: fly balls may carry farther - can hurt pitchers.",
            "Tailwind: fly balls likely to carry - helps hitters."
        )
    return (
        "Crosswind: pushes balls to foul lines. Neutral-ish for pitchers.",
        "Crosswind: pushes balls to foul lines. Neutral-ish for hitters."
    )

def fetch_forecast_weather(lat: float, lon: float, target_dt: datetime) -> Optional[Dict]:
    """Fetch weather forecast from OpenWeatherMap API."""
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OWM_API_KEY,
        "units": WEATHER_UNITS
    }

    try:
        with requests.Session() as session:
            resp = session.get(base_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            forecast_list = data.get("list", [])
            if not forecast_list:
                return None

            target_unix = int(datetime.timestamp(target_dt))
            closest = min(forecast_list, key=lambda ent: abs(ent["dt"] - target_unix))

            return {
                "temp": closest["main"].get("temp"),
                "humidity": closest["main"].get("humidity"),
                "wind_speed": closest["wind"].get("speed"),
                "wind_deg": closest["wind"].get("deg")
            }
    except Exception as e:
        logging.error(f"Error fetching weather forecast: {e}")
        return None

# Baseball Statistics
def extract_pitch_frequency(zone_map_element, zone_name: str) -> Tuple[int, float]:
    """Extract pitch frequency counts and percentages from SVG zone maps."""
    selector = f"g.zone-region-pitch-frequency g.{zone_name}"
    grp = zone_map_element.find(selector, first=True)
    if not grp:
        return 0, 0.0

    all_text_nodes = grp.find("text")
    if not all_text_nodes or len(all_text_nodes) < 2:
        return 0, 0.0

    try:
        count = int(all_text_nodes[0].text.strip())
    except ValueError:
        count = 0

    try:
        pct_val = float(all_text_nodes[1].text.strip().split("%")[0])
    except Exception:
        pct_val = 0.0

    return count, pct_val