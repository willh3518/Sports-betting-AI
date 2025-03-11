import undetected_chromedriver as uc
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def process_filter(driver, index):
    """Click on a filter button and return the filter name, handling stale element issues."""
    try:
        # Skip index 0 since the first filter is already clicked
        if index == 0:
            return None

        # Re-fetch the filter buttons every time before clicking
        filter_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.stat"))
        )

        if index >= len(filter_buttons):  # Ensure index is within range
            return None

        button = filter_buttons[index]
        filter_name = button.text.strip()

        # Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        button.click()

        # Wait for content to update after clicking
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li[class*='grid']"))
        )

        return filter_name

    except StaleElementReferenceException:
        logging.warning(f"Stale element at index {index}, re-fetching buttons and retrying.")
        return process_filter(driver, index)  # Retry with fresh elements

    except Exception as e:
        logging.warning(f"Skipping filter index {index} due to error: {e}")
        return None

def scrape_props(driver):
    """Scrape player prop data from the website."""
    all_props = []
    visited_filters = set()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.stat"))
        )
    except Exception:
        logging.error("Filter buttons not found. Exiting...")
        return pd.DataFrame()

    filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button.stat")

    for i in range(len(filter_buttons)):
        filter_name = process_filter(driver, i)
        if not filter_name or filter_name in visited_filters:
            continue

        visited_filters.add(filter_name)

        try:
            player_containers = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[class*='grid']"))
            )
        except Exception:
            logging.warning(f"No player data found for filter: {filter_name}")
            continue

        for container in player_containers:
            try:
                # Check if both 'More' and 'Less' buttons are present
                more_button = container.find_element(By.CSS_SELECTOR, "button#test-more")
                less_button = container.find_element(By.CSS_SELECTOR, "button#test-less")

                if more_button is None or less_button is None:
                    logging.info(f"Skipping prop for player as it doesn't have both 'More' and 'Less' options.")
                    continue

                player_name = container.find_element(By.CSS_SELECTOR, "h3[id='test-player-name']").text.strip()
                prop_value = container.find_element(By.CSS_SELECTOR, "div[class='heading-md']").text.strip()

                # Convert prop_value safely
                try:
                    prop_value = float(prop_value)
                except ValueError:
                    logging.warning(f"Skipping invalid prop value: {prop_value}")
                    continue

                prop_type = container.find_element(By.CSS_SELECTOR, "span[class='break-words']").text.strip()

                # Extract the opposing team abbreviation
                raw_text = container.find_element(By.CSS_SELECTOR, "time.text-soClean-140.body-sm").text.strip()
                opposing_team = raw_text.split("vs")[1].strip().split()[0] if "vs" in raw_text else None

                team_position_text = container.find_element(By.CSS_SELECTOR,
                                                            "div[id='test-team-position']").text.strip()
                team = team_position_text.split('-')[0].strip() if '-' in team_position_text else None

                # ✅ Skip any prop that contains "dunk" (case-insensitive)
                if "dunk" in prop_type.lower() or "fantasy score" in prop_type.lower():
                    logging.info(
                        f"Skipping prop '{prop_type}' for player '{player_name}' (unwanted prop type detected).")
                    continue

                # ✅ Skip any player that contains '+' (indicating a combo player)
                if "+" in player_name:
                    logging.info(f"Skipping combo player '{player_name}'.")
                    continue

                all_props.append({
                    'Player': player_name,
                    'Team': team,
                    'Prop Type': prop_type,
                    'Prop Value': prop_value,
                    'Opposing Team': opposing_team,
                })

            except Exception as e:
                logging.warning(f"Error processing player container: {e}")
                continue

    return pd.DataFrame(all_props)

def main():
    """Main execution function."""
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})

    driver = uc.Chrome(options=options, version_main=133)

    try:
        url = 'https://app.prizepicks.com/'
        driver.get(url)
        input("Solve CAPTCHA manually and press Enter to continue...")

        props_df = scrape_props(driver)

        if not props_df.empty:
            props_df = props_df.sort_values(by='Player', ascending=True)
            props_df.to_csv('../Prop_Data_CSV/prizepicks_data.csv', index=False)
            logging.info("Data saved to 'prizepicks_data.csv'.")
        else:
            logging.info("No data collected.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
