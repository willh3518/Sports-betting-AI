import os
import subprocess
import time

# ───── CONFIG ─────
SCRIPT_DIR = "../MLB_Data_Extraction"
EXTENSION = ".py"

# Scripts with special order
PRIZEPICKS_SCRIPT = "mlb_prizepicks.py"
MERGE_SCRIPTS = {"hitter_stats_merge.py", "pitcher_stats_merge.py"}
EXCLUDE_SCRIPTS = {
    "Overall_MLB_Stats.py",
    "MLB_Main.py",  # <-- this script
}

def run_script(script_path):
    print(f"🚀 Running {script_path} ...")
    subprocess.run(["python", script_path], check=True)

if __name__ == "__main__":
    start_time = time.time()

    # Step 1: Run mlb_prizepicks.py
    run_script(os.path.join(SCRIPT_DIR, PRIZEPICKS_SCRIPT))

    # Step 2: Run all other scripts (excluding special/merge/excluded)
    all_scripts = sorted([
        f for f in os.listdir(SCRIPT_DIR)
        if (
            f.endswith(EXTENSION)
            and f not in EXCLUDE_SCRIPTS
            and f != PRIZEPICKS_SCRIPT
            and f not in MERGE_SCRIPTS
        )
    ])

    for script in all_scripts:
        run_script(os.path.join(SCRIPT_DIR, script))

    # Step 3: Run merge scripts last
    for script in sorted(MERGE_SCRIPTS):
        run_script(os.path.join(SCRIPT_DIR, script))

    print("✅ All scripts executed (with proper order).")
    print(f"⏱️ Total time: {time.time() - start_time:.2f} seconds.")
