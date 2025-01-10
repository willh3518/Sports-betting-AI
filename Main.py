import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up undetected ChromeDriver
options = uc.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = uc.Chrome(options=options)

# Access PrizePicks website
url = 'https://app.prizepicks.com/'
driver.get(url)

# Wait for the user to solve CAPTCHA manually if it appears
input("Solve CAPTCHA manually and press Enter to continue...")

# Scroll and wait for dynamic content
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Initialize data collection list
props = []

try:
    # Locate all prop filter buttons initially
    filter_buttons = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.stat"))
    )
    print(f"Found {len(filter_buttons)} filter buttons.")

    # Track visited filters
    visited_filters = set()

    # Loop through each filter button
    for i in range(len(filter_buttons)):
        try:
            # Re-fetch filter buttons dynamically
            filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button.stat")
            button = filter_buttons[i]

            # Get the filter name
            filter_name = button.text.strip()
            if filter_name in visited_filters:
                continue  # Skip already visited filters
            visited_filters.add(filter_name)

            print(f"Scraping data for: {filter_name}")

            # Scroll the button into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)  # Allow time for scrolling

            # Click using JavaScript to avoid stale element issues
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)  # Wait for the page to load

            # Wait for the player containers to update
            player_containers = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='grid'][class*='grid-rows']"))
            )
            print(f"Found {len(player_containers)} player containers for {filter_name}.")

            # Scrape data for each player
            for container in player_containers:
                try:
                    # Extract player name
                    player_name_element = container.find_element(By.CSS_SELECTOR, "h3[id='test-player-name']")
                    player_name = player_name_element.text if player_name_element else "N/A"

                    # Extract prop value
                    prop_value_element = container.find_element(By.CSS_SELECTOR, "div[class='heading-md']")
                    prop_value = prop_value_element.text if prop_value_element else "N/A"

                    # Extract prop type
                    prop_type_element = container.find_element(By.CSS_SELECTOR, "span[class='break-words']")
                    prop_type = prop_type_element.text if prop_type_element else "N/A"

                    # Append data
                    props.append({
                        'Player': player_name,
                        'Filter': filter_name,
                        'Prop Type': prop_type,
                        'Prop Value': prop_value
                    })
                except Exception as e:
                    print(f"Error extracting data for a player in {filter_name}: {e}")

            # Wait a bit before moving to the next filter
            time.sleep(3)

        except Exception as e:
            print(f"Error handling filter button {i}: {e}")

except Exception as e:
    print(f"Error locating filter buttons: {e}")

# Save data to CSV
if props:
    df = pd.DataFrame(props)
    csv_file_path = '/Users/willhart/Downloads/prizepicks_all_props.csv'
    df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")
else:
    print("No data collected.")

# Close the browser
driver.quit()