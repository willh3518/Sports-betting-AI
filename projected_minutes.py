import csv
import time
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

def normalize_name(name):
    # Normalize unicode (removes accents)
    nfkd_form = unicodedata.normalize('NFKD', name)
    # Encode to ASCII bytes and decode back to string, ignoring non-ascii characters
    ascii_str = nfkd_form.encode('ASCII', 'ignore').decode('ASCII')
    # Remove periods, extra spaces, etc.
    cleaned_name = ascii_str.replace('.', '').strip()
    return cleaned_name

def scrape_lineups_data_to_csv():
    # --- Chrome Options with anti-detection flags ---
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/111.0.0.0 Safari/537.36"
    )
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    # Hide 'webdriver' to reduce headless detection
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
            """
        }
    )

    try:
        # 1. Open the page
        driver.get("https://www.lineups.com/nba/nba-player-minutes-per-game")

        # 2. Click the dropdown and select "500"
        dropdown_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='ngb-dd-items_per_page']/span"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button)
        time.sleep(1)

        try:
            driver.execute_script("arguments[0].click();", dropdown_button)
        except:
            ActionChains(driver).move_to_element(dropdown_button).click().perform()
        time.sleep(2)

        option_500 = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH,
                "(.//*[normalize-space(text()) and normalize-space(.)='Search Players'])[1]/following::div[25]"))
        )
        option_500.click()
        time.sleep(3)

        # 3. Extract player names from the first (static) table
        static_table_div = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/app-root/div/div/app-minutes-router/app-minutes/div/div/div[5]")
            )
        )
        static_tbody = static_table_div.find_element(By.XPATH, ".//tbody[@class='static-table-body']")
        static_rows = static_tbody.find_elements(By.TAG_NAME, "tr")

        player_names = []
        for row in static_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 1:
                continue
            name = cells[0].text.strip()
            if not name:
                try:
                    name = cells[0].find_element(By.CSS_SELECTOR, "a span .player-name-col-lg").text.strip()
                except:
                    name = ""
            player_names.append(name)

        # 4. Extract projected minutes from the second (stats) table
        stats_table = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.minute-item-table"))
        )
        stats_tbody = stats_table.find_element(By.TAG_NAME, "tbody")
        stats_rows = stats_tbody.find_elements(By.TAG_NAME, "tr")

        projected_minutes_list = []
        for row in stats_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 6:
                projected_minutes_list.append("")
                continue
            projected_minutes = cells[5].text.strip()
            projected_minutes_list.append(projected_minutes)

        # 5. Normalize and combine before writing to CSV
        combined_data = []
        row_count = min(len(player_names), len(projected_minutes_list))
        for i in range(row_count):
            normalized_name = normalize_name(player_names[i])
            combined_data.append({
                "player_name": normalized_name,
                "projected_minutes": projected_minutes_list[i]
            })

        csv_filename = "lineups_projected_minutes.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["player_name", "projected_minutes"])
            writer.writeheader()
            writer.writerows(combined_data)

        print(f"Data written to {csv_filename}")
        return combined_data

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_lineups_data_to_csv()
