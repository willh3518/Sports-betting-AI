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
    "mlb_hitter_advanced_stats.py",
    "mlb_pitcher_advanced_stats.py"
    "Overall_MLB_Stats.py",
    "MLB_Main.py",
    "Config.py",
    "mlb_utils.py",
    "create_training_data.py",
    "prepare_mlb_predictions.py"
}

# Track errors
error_log = []

def run_script(script_path):
    print(f" Running {script_path} ...")
    try:
        subprocess.run(["python", script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        error_message = f"Error in {script_path}: {str(e)}"
        print(f"ERROR: {error_message}")
        error_log.append(error_message)
        return False

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

    # Print error summary
    if error_log:
        print("\n" + "=" * 50)
        print(f" ERROR SUMMARY: {len(error_log)} script(s) failed")
        print("=" * 50)
        for i, error in enumerate(error_log, 1):
            print(f" {i}. {error}")
        print("\nPlease run these scripts individually to fix the issues.")
    else:
        print("\n All scripts completed successfully with no errors!")