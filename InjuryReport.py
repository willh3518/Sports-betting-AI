import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def fetch_injury_data_selenium():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    service = Service("/Users/willhart/Downloads/chromedriver-mac-arm64/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.espn.com/nba/injuries")
    time.sleep(5)  # Allow the page to load fully

    injuries = []
    rows = driver.find_elements(By.XPATH, '//table[@class="Table"]/tbody/tr')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if cells and len(cells) > 3:
            player_name = cells[0].text.strip()
            status = cells[3].text.strip()
            injuries.append((player_name, status))
    driver.quit()
    return injuries

def create_starting_lineup_dataframe():
    data = {
        'Team': ['Celtics', 'Nets', 'Knicks', '76ers', 'Raptors', 'Bulls', 'Cavaliers', 'Pistons', 'Pacers', 'Bucks',
                 'Hawks', 'Hornets', 'Heat', 'Magic', 'Wizards', 'Nuggets', 'Timberwolves', 'Thunder', 'Trail Blazers',
                 'Jazz', 'Warriors', 'Clippers', 'Lakers', 'Suns', 'Kings', 'Mavericks', 'Rockets', 'Grizzlies',
                 'Pelicans', 'Spurs'],
        'PG': ['Jrue Holiday', "D'Angelo Russell", 'Jalen Brunson', 'Tyrese Maxey', 'Immanuel Quickley', 'Josh Giddey',
               'Darius Garland', 'Cade Cunningham', 'Tyrese Haliburton', 'Damian Lillard', 'Trae Young', 'LaMelo Ball',
               'Tyler Herro', 'Jalen Suggs', 'Jordan Poole', 'Jamal Murray', 'Anthony Edwards',
               'Shai Gilgeous-Alexander', 'Anfernee Simons', 'Keyonte George', 'Stephen Curry', 'James Harden',
               'Austin Reaves', 'Tyus Jones', "De'Aaron Fox", 'Kyrie Irving', 'Fred VanVleet', 'Ja Morant',
               'Dejounte Murray', 'Chris Paul'],
        'SG': ['Jaylen Brown', 'Cam Thomas', 'Mikal Bridges', 'Kelly Oubre Jr.', 'Grady Dick', 'Coby White',
               'Donovan Mitchell', 'Jaden Ivey', 'Andrew Nembhard', 'Andre Jackson', 'Dyson Daniels', 'Brandon Miller',
               'Duncan Robinson', 'Kentavious Caldwell-Pope', 'Bub Carrington', 'Russell Westbrook', 'Donte Divencenzo',
               'Cason Wallace', 'Deni Avdija', 'Collin Sexton', 'Dennis Schroder', 'Norman Powell', 'Max Christie',
               'Devin Booker', 'Malik Monk', 'Klay Thompson', 'Jalen Green', 'Desmond Bane', 'CJ McCollum',
               'Stephon Castle'],
        'SF': ['Jayson Tatum', 'Cam Johnson', 'Josh Hart', 'Eric Gordon', 'RJ Barrett', 'Zach LaVine', 'Dean Wade',
               'Tim Hardaway Jr.', 'Benedict Marthurin', 'Khris Middleton', 'Zaccharie Risacher', 'Josh Green',
               'Jimmy Butler', 'Franz Wagner', 'Bilal Coulibaly', 'Christian Braun', 'Jaden McDaniels', 'Lu Dort',
               'Toumani Camara', 'Lauri Markkanen', 'Andrew Wiggins', 'Kawhi Leonard', 'LeBron James', 'Bradley Beal',
               'DeMar DeRozan', 'Luka Doncic', 'Dillon Brooks', 'Jaylen Wells', 'Trey Murphy III', 'Devin Vassell'],
        'PF': ['Derrick White', 'Noah Clowney', 'OG Anunoby', 'Paul George', 'Scottie Barnes', 'Patrick Williams',
               'Evan Mobley', 'Tobias Harris', 'Pascal Siakam', 'Giannis Antetokounmpo', 'Jalen Johnson',
               'Miles Bridges', "Kel'el Ware", 'Paolo Banchero', 'Alexandre Sarr', 'Michael Porter Jr.',
               'Julius Randle', 'Jalen Williams', 'Jerami Grant', 'John Collins', 'Draymond Green', 'Derrick Jones Jr.',
               'Rui Hachimura', 'Kevin Durant', 'Keegan Murray', 'PJ Washington', 'Amen Thompson', 'Jaren Jackson Jr.',
               'Zion WIlliamson', 'Jeremy Sochan'],
        'C': ['Kristaps Porzingis', 'Nic Claxton', 'Karl-Anthony Towns', 'Joel Embiid', 'Jakob Poeltl',
              'Nikola Vucevic', 'Jarrett Allen', 'Jalen Duren', 'Myles Turner', 'Brook Lopez', 'Clint Capela',
              'Mark Williams', 'Bam Adebayo', 'Wendell Carter Jr.', 'Jonas Valanciunas', 'Nikola Jokic', 'Rudy Gobert',
              'Isaiah Hartenstein', 'Deandre Ayton', 'Walker Kessler', 'Trayce Jackson-Davis', 'Ivica Zubac',
              'Anthony Davis', 'Jusuf Nurkic', 'Domantas Sabonis', 'Derick Lively Jr.', 'Alperen Sengun', 'Zach Edey',
              'Yves Missi', 'Victor Wembanyama']
    }
    return pd.DataFrame(data)

def filter_starters(starting_lineups, injured_players):
    injured_player_names = {player for player, _ in injured_players}  # Set of injured player names
    injured_starters = []
    non_injured_starters = []

    for index, row in starting_lineups.iterrows():
        team = row['Team']
        for position in ['PG', 'SG', 'SF', 'PF', 'C']:
            player = row[position]
            if player in injured_player_names:
                injured_starters.append(
                    {'Team': team, 'Position': position, 'Player': player, 'Injury Status': 'Injured'})
            else:
                non_injured_starters.append(
                    {'Team': team, 'Position': position, 'Player': player, 'Injury Status': 'Healthy'})

    return injured_starters, non_injured_starters

def create_combined_csv(injured_starters, non_injured_starters, file_name):
    combined_data = injured_starters + non_injured_starters  # Combine data with injured players first
    df = pd.DataFrame(combined_data)
    df = df.sort_values(by=['Team', 'Injury Status'], ascending=[True, False])  # Sort by Team, then Injury Status
    df.to_csv(file_name, index=False)
    print(f"Combined CSV file '{file_name}' has been created.")

def main():
    # Fetch injury data
    injured_players = fetch_injury_data_selenium()

    # Create the starting lineups DataFrame
    starting_lineups = create_starting_lineup_dataframe()

    # Separate injured and non-injured starters
    injured_starters, non_injured_starters = filter_starters(starting_lineups, injured_players)

    # Create a combined CSV file
    create_combined_csv(injured_starters, non_injured_starters, 'combined_starters.csv')

if __name__ == '__main__':
    main()
