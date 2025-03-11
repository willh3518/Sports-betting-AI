import aiohttp
import asyncio
import random
import logging
import os
import unicodedata
from bs4 import BeautifulSoup

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ✅ Fix: Use absolute path to locate `working_proxies.txt`
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level
PROXY_FILE = os.path.join(BASE_DIR, "working_proxies.txt")  # Locate file in main directory
SCRAPE_TIMEOUT = 8
semaphore = asyncio.Semaphore(40)  # Controls concurrency

async def load_proxies():
    """Loads proxies from file asynchronously."""
    try:
        with open(PROXY_FILE, "r") as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        if not proxies:
            logging.error("🚨 No proxies found in the file!")
        return proxies
    except FileNotFoundError:
        logging.error(f"🚨 Proxy file '{PROXY_FILE}' not found!")
        return []

PROXIES = asyncio.run(load_proxies())  # Load proxies at startup

async def get_proxy():
    """Rotates proxies dynamically."""
    global PROXIES
    while True:
        if not PROXIES:
            logging.warning("🔄 Reloading proxies...")
            PROXIES = await load_proxies()
        yield random.choice(PROXIES)

async def fetch_html(url, max_retries=5):
    """Fetches HTML from a given URL using rotating proxies and skips if 'no results' message is detected."""
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
            proxy_url = f"http://{proxy}"  # Adjust for HTTPS if needed

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=headers, timeout=SCRAPE_TIMEOUT, proxy=proxy_url) as response:
                        if response.status == 200:
                            html = await response.text()

                            # ✅ Parse HTML with BeautifulSoup
                            soup = BeautifulSoup(html, "html.parser")
                            no_results_element = soup.find("span", class_="my-[1em] [&>a]:underline [&>a]:text-team-secondary whitespace-pre-wrap text-pretty")
                            # ✅ Check if the no results message exists
                            if no_results_element and "I understood your question, but there were no results." in no_results_element.text:
                                logging.error(f"❌ No results found at {url}. Skipping further attempts immediately.")
                                return None  # Auto-skip remaining attempts

                            return html  # Return valid HTML if no "no results" message detected

                        elif response.status in [403, 429]:  # Rate Limited or Forbidden
                            logging.warning(f"⚠️ Rate limited ({response.status}) on {proxy}. Retrying...")
                            await asyncio.sleep((2 ** attempt) + random.uniform(0.5, 2.0))

                except Exception as e:
                    logging.warning(f"❌ Proxy {proxy} failed: {e}")

        logging.error(f"❌ Max retries reached for {url}. Skipping...")
        return None

def clean_player_name(name):
    """Cleans player names by removing accents, periods, and ensuring proper capitalization.
    Skips combo players that contain a '+' symbol.
    """
    if "+" in name:
        return None  # Skip combo players

    name = name.replace(".", "")
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8")
    return name.title()