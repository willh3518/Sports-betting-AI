import csv
import unicodedata
from nba_api.stats.static import players

# Function to normalize names: removes accents and punctuation
def normalize_name(name):
    # Normalize unicode (removes accents)
    nfkd_form = unicodedata.normalize('NFKD', name)
    # Encode to ASCII bytes and decode back to string, ignoring non-ascii characters
    ascii_str = nfkd_form.encode('ASCII', 'ignore').decode('ASCII')
    # Remove periods, extra spaces, etc.
    cleaned_name = ascii_str.replace('.', '').strip()
    return cleaned_name

# Get the current NBA players
nba_players = players.get_players()

# Specify the filename for the CSV
output_csv = '../Prop_Data_CSV/nba_player_ids.csv'

# Define headers for the CSV
headers = ['PlayerName', 'PlayerID']

# Sort function:
def sort_key(player):
    has_id = player['id'] is not None
    normalized = normalize_name(player['full_name']).lower()
    return (not has_id, normalized)

# Sort the list
sorted_players = sorted(nba_players, key=sort_key)

# Write the sorted data to a CSV file
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for player in sorted_players:
        player_name = normalize_name(player['full_name'])  # normalized name
        player_id = player['id'] if player['id'] is not None else ''
        writer.writerow([player_name, player_id])

print(f"✅ Successfully saved {len(sorted_players)} normalized players to {output_csv}")
