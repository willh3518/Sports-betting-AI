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
    # Wait for player containers to load
    player_containers = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='grid'][class*='grid-rows']"))
    )
    print(f"Found {len(player_containers)} player containers.")

    for container in player_containers:
        try:
            # Extract player name
            try:
                player_name_element = container.find_element(By.CSS_SELECTOR, "h3[id='test-player-name']")
                player_name = player_name_element.text if player_name_element else "N/A"
            except Exception as e:
                player_name = "N/A"
                print(f"Player Name not found: {e}")

            # Extract prop value
            try:
                prop_value_element = container.find_element(By.CSS_SELECTOR, "div[class='heading-md']")
                prop_value = prop_value_element.text if prop_value_element else "N/A"
            except Exception as e:
                prop_value = "N/A"
                print(f"Prop Value not found for {player_name}: {e}")

            # Extract prop type
            try:
                prop_type_element = container.find_element(By.CSS_SELECTOR, "span[class='break-words']")
                prop_type = prop_type_element.text if prop_type_element else "N/A"
            except Exception as e:
                prop_type = "N/A"
                print(f"Prop Type not found for {player_name}: {e}")

            # Append to data collection
            props.append({
                'Player': player_name,
                'Prop Type': prop_type,
                'Prop Value': prop_value
            })
        except Exception as e:
            print(f"Error extracting data for a player: {e}")

except Exception as e:
    print(f"Error locating player containers: {e}")

# Save data to CSV
if props:
    df = pd.DataFrame(props)
    csv_file_path = '/Users/willhart/Downloads/prizepicks_props.csv'
    df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")
else:
    print("No data collected.")

# Close the browser
driver.quit()


# Handle pop-ups if present
try:
    close_button = driver.find_element(By.CLASS_NAME, 'popup-close')
    close_button.click()
    time.sleep(1)
except Exception as e:
    print(f"No pop-up found: {e}")

'''
# Wait for a specific element to load
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "sport-category-button"))
)
'''


# Collect props data
props = []

# Find sports categories
sports_buttons = driver.find_elements(By.CLASS_NAME, 'league-icon-old selected-old')  # Update based on HTML structure

# Loop through each sport category
for sport_button in sports_buttons:
    sport_button.click()
    time.sleep(2)

    players = driver.find_elements(By.CLASS_NAME, 'h-16')  # Update based on HTML structure
    for player in players:
        player_name = player.find_element(By.CLASS_NAME, 'heading-xs pb-1 text-white').text
        prop_type = player.find_element(By.CLASS_NAME, 'break-words').text
        prop_value = player.find_element(By.CLASS_NAME, 'heading-md').text

        props.append({'Player': player_name, 'Prop Type': prop_type, 'Prop Value': prop_value})
print (props)
# Convert to DataFrame and export to CSV
df = pd.DataFrame(props)
csv_file_path = '/Users/willhart/Downloads/prizepicks_props.csv'
df.to_csv(csv_file_path, index=False)

# Close browser
driver.quit()
