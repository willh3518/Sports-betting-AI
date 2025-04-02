from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import db, User
from datetime import datetime
import pandas as pd
import os

main_routes = Blueprint('main_routes', __name__)

# ===================
# CONTEXT PROCESSOR (Year for footer)
# ===================
@main_routes.app_context_processor
def inject_year():
    return {'year': datetime.now().year}

# ===================
# PUBLIC ROUTES
# ===================

@main_routes.route('/')
def home():
    print("Accessing home page")
    return render_template('home.html')

@main_routes.route('/whyus')
def whyus():
    print("Accessing Why Us page")
    return render_template('whyus.html')

@main_routes.route('/features')
def features():
    print("Accessing Features page")
    return render_template('features.html')

@main_routes.route('/api/props', methods=['GET'])
def get_props():
    # Paths to your files
    combined_csv_path = os.path.join(os.getcwd(), 'Prop_Data_CSV', 'final_combined_data.csv')
    player_ids_csv_path = os.path.join(os.getcwd(), 'Prop_Data_CSV', 'nba_player_ids.csv')  # <- updated filename!

    try:
        # Load both CSVs into DataFrames
        df_props = pd.read_csv(combined_csv_path, encoding='latin1')
        df_ids = pd.read_csv(player_ids_csv_path, encoding='latin1')

        # Replace all NaN, pd.NA, pd.NaT with None for props
        props_data = df_props.replace({pd.NA: None, pd.NaT: None, float('nan'): None})

        # Build a dictionary from player ID CSV for quick lookup
        # Key: normalized player name, Value: PlayerID
        player_id_map = {
            str(row['PlayerName']).strip().lower(): str(int(row['PlayerID']))
            for index, row in df_ids.iterrows()
            if pd.notna(row['PlayerID'])  # Make sure PlayerID isn't NaN
        }

        # Merge the PlayerID & HeadshotURL into each player record
        props_list = []

        for index, row in props_data.iterrows():
            player_name = str(row['Player']).strip().lower()

            nba_id = player_id_map.get(player_name)

            # Optional: fallback for unmatched names
            if not nba_id:
                nba_id = None
                headshot_url = None
            else:
                headshot_url = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{nba_id}.png'

            # Add the new fields to the player data
            player_record = row.to_dict()
            player_record['NBAID'] = nba_id
            player_record['HeadshotURL'] = headshot_url

            props_list.append(player_record)

        # ✅ NEW: Get unique teams playing today from the props data
        teams_playing = sorted(
            set(team for team in props_data['Team'].dropna().unique())
        )


        # Debug: Show one of the records
        print(props_list[0])

        return jsonify({
            'props': props_list,
            'teams': teams_playing
        })

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

