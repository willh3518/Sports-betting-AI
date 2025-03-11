import os
import subprocess
import time

# ✅ List of all Python scripts to run
SCRIPTS = [
    "H2H_CurrentSeason.py",
    "Home_or_Away.py",
    "Last_5_Season.py",
    "Last_10_H2H.py",
    "Last_10_Hit_Percentage.py",
    "Last_10_Season.py",
    "Opponent_Defensive_Rating.py",
    "Season_Hit_Percentage.py",
    "Season_Stats.py",
    "Stats_Without_Injured_Starter.py",
]

# ✅ Set the script directory
SCRIPT_DIR = "../Data_Extraction"
DATA_EXTRACTION_PATH = os.path.join(SCRIPT_DIR)
MERGE_SCRIPT = "Merge_Data.py"
PRIZEPICKS_SCRAPER = "PrizePicks_Scraper.py"

def run_script(script_name):
    """Executes a Python script from the Data_Extraction folder."""
    script_path = os.path.join(DATA_EXTRACTION_PATH, script_name)
    if os.path.exists(script_path):
        print(f"🚀 Running {script_name} ...")
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"⚠️ Script {script_name} not found!")

if __name__ == "__main__":
    start_time = time.time()

    # ✅ Step 1: Run PrizePicks Scraper first
    run_script(PRIZEPICKS_SCRAPER)

    # ✅ Step 2: Run all data extraction scripts
    for script in SCRIPTS:
        run_script(script)

    # ✅ Step 3: Run merge script
    run_script(MERGE_SCRIPT)

    print("✅ All scripts executed successfully!")
    print(f"🚀 Execution completed in {time.time() - start_time:.2f} seconds.")
