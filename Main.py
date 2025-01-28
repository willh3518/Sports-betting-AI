import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import logging

# Setup logging for debugging and error reporting
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def process_filter(driver, filter_buttons, index):
    try:
        # Refresh buttons to avoid stale element issues
        filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button.stat")
        button = filter_buttons[index]

        # Get the filter name
        filter_name = button.text.strip()

        # Scroll the button into view and click
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(5)  # Wait for content to load
        return filter_name
    except Exception as e:
        logging.error(f"Error processing filter at index {index}: {e}")
        return None

def scrape_props(driver):
    all_props = []
    filter_buttons = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.stat"))
    )
    visited_filters = set()

    for i in range(len(filter_buttons)):
        filter_name = process_filter(driver, filter_buttons, i)
        if not filter_name or filter_name in visited_filters:
            continue
        visited_filters.add(filter_name)

        player_containers = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[class*='grid']"))
        )

        for container in player_containers:
            try:
                player_name = container.find_element(By.CSS_SELECTOR, "h3[id='test-player-name']").text
                prop_value = float(container.find_element(By.CSS_SELECTOR, "div[class='heading-md']").text)
                prop_type = container.find_element(By.CSS_SELECTOR, "span[class='break-words']").text

                # Extract the Opposing Team abbreviation
                raw_text = container.find_element(By.CSS_SELECTOR, "time.text-soClean-140.body-sm").text.strip()
                if "vs" in raw_text:
                    opposing_team = raw_text.split("vs")[1].strip().split()[0]
                else:
                    opposing_team = None

                # Collect and append prop data
                all_props.append({
                    'Player': player_name,
                    'Prop Type': prop_type,
                    'Prop Value': prop_value,
                    'Opposing Team': opposing_team,
                })

            except Exception as e:
                logging.error(f"Error processing player container: {e}")
                continue

    return pd.DataFrame(all_props)

def main():
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 1  # 2 = Block location, 1 = Allow
    })
    driver = uc.Chrome(options=options)

    url = 'https://app.prizepicks.com/'
    driver.get(url)
    input("Solve CAPTCHA manually and press Enter to continue...")

    props_df = scrape_props(driver)

    if not props_df.empty:
        props_df = props_df.sort_values(by='Player', ascending=True)
        props_df.to_csv('prizepicks_data.csv', index=False)
        print("Data saved to 'prizepicks_data.csv'.")
    else:
        print("No data collected.")

    driver.quit()

if __name__ == "__main__":
    main()
