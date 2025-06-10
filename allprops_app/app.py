import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from access_config import DAILY_ACCESS_CODE
import unicodedata  # Make sure this is at the top

# --- Alias Map ---
PLAYER_NAME_ALIASES = {
    "alex sarr": "alexandre sarr"
}

# --- Helper Functions ---
def normalize_name(name):
    nfkd_form = unicodedata.normalize('NFKD', name)
    ascii_str = nfkd_form.encode('ASCII', 'ignore').decode('ASCII')
    return ascii_str.replace('.', '').strip().lower()

def apply_alias(name):
    return PLAYER_NAME_ALIASES.get(name, name)

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Replace with a random secure key in production

@app.route('/', methods=['GET', 'POST'])
def enter_code():
    if request.method == 'POST':
        code = request.form.get('access_code')
        if code == DAILY_ACCESS_CODE:
            session['access_granted'] = True
            return redirect(url_for('all_props'))
        else:
            return render_template('enter_code.html', error='Invalid code. Try again.')
    return render_template('enter_code.html')

@app.route('/allprops')
def all_props():
    # Check if user has entered the correct code
    if not session.get('access_granted'):
        return redirect(url_for('enter_code'))
    return render_template('allprops.html')

@app.route('/api/props', methods=['GET'])
def get_props():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    combined_csv_path = os.path.join(project_root, 'Prop_Data_CSV', 'final_combined_data.csv')
    player_ids_csv_path = os.path.join(project_root, 'Prop_Data_CSV', 'nba_player_ids.csv')
    projected_minutes_path = os.path.join(project_root, 'lineups_projected_minutes.csv')

    prizepicks_path = os.path.join(project_root, 'test_prizepicks_props.csv')
    underdog_path = os.path.join(project_root, 'underdog_props.csv')

    try:
        df_props = pd.read_csv(combined_csv_path, encoding='latin1')
        df_ids = pd.read_csv(player_ids_csv_path, encoding='latin1')
        df_minutes = pd.read_csv(projected_minutes_path, encoding='latin1')
        df_pp = pd.read_csv(prizepicks_path, encoding='latin1')
        df_ud = pd.read_csv(underdog_path, encoding='latin1')

        props_data = df_props.replace({pd.NA: None, pd.NaT: None, float('nan'): None})
        df_minutes = df_minutes.replace({pd.NA: None, pd.NaT: None, float('nan'): None})
        df_pp = df_pp.replace({pd.NA: None, pd.NaT: None, float('nan'): None})
        df_ud = df_ud.replace({pd.NA: None, pd.NaT: None, float('nan'): None})

        # Maps
        player_id_map = {
            apply_alias(normalize_name(row['PlayerName'])): str(int(row['PlayerID']))
            for _, row in df_ids.iterrows()
            if pd.notna(row['PlayerID'])
        }

        projected_minutes_map = {
            apply_alias(normalize_name(row['player_name'])): row['projected_minutes']
            for _, row in df_minutes.iterrows()
            if pd.notna(row['projected_minutes'])
        }

        # --- Build full prop list ---
        props_list = []
        for _, row in props_data.iterrows():
            raw_name = str(row['Player'])
            normalized_name = apply_alias(normalize_name(raw_name))
            prop_type = str(row['Prop Type']).strip().lower()

            nba_id = player_id_map.get(normalized_name)
            headshot_url = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{nba_id}.png' if nba_id else None
            projected_minutes = projected_minutes_map.get(normalized_name)

            # Get PrizePicks lines for that prop
            pp_lines = df_pp[df_pp['Player'].str.lower().apply(lambda x: apply_alias(normalize_name(x)) == normalized_name)]
            pp_matches = pp_lines[pp_lines['Prop Type'].str.lower().str.replace(" ", "") == prop_type.replace(" ", "")]
            prizepicks_lines = [
                {
                    'line': row['Prop Value'],
                    'label': row.get('Demon/Goblin', 'base')
                } for _, row in pp_matches.iterrows()
            ]

            # Get Underdog line for that prop
            ud_lines = df_ud[df_ud['Player'].str.lower().apply(lambda x: apply_alias(normalize_name(x)) == normalized_name)]
            ud_matches = ud_lines[ud_lines['Prop Type'].str.lower().str.replace(" ", "") == prop_type.replace(" ", "")]
            underdog_lines = [
                {
                    'line': row['Prop Value'],
                    'label': 'underdog'
                } for _, row in ud_matches.iterrows()
            ]

            player_record = row.to_dict()
            player_record['NBAID'] = nba_id
            player_record['HeadshotURL'] = headshot_url
            player_record['ProjectedMinutes'] = projected_minutes
            player_record['PrizePicksLines'] = prizepicks_lines
            player_record['UnderdogLines'] = underdog_lines

            props_list.append(player_record)

        teams_playing = sorted(set(team for team in props_data['Team'].dropna().unique()))
        return jsonify({'props': props_list, 'teams': teams_playing})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
