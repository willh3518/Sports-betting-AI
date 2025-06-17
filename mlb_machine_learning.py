import os
import glob
import logging
import joblib
import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import GridSearchCV

# ── CONFIG ──────────────────────────────────────────────────────────────────────
MLB_DATA_DIR   = "MLB_Prop_Data_CSV"
MODEL_DIR      = "MLB_Models"
RESULTS_DIR    = "MLB_Results"
TRAINING_DIR   = os.path.join(MLB_DATA_DIR, "MLB_Training_Data")
TODAY          = datetime.datetime.now().strftime("%Y-%m-%d")
TOP_N          = 10

prop_list      = ["Hits","Runs","RBIs","Hits+Runs+RBIs","Hitter Fantasy Score"]
pitcher_list   = ["Pitcher Strikeouts","Earned Runs Allowed","Pitches Thrown","Pitching Outs","Pitcher Fantasy Score"]

for d in (MODEL_DIR, RESULTS_DIR, TRAINING_DIR):
    os.makedirs(d, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ── TRAINING DATA LOADER ─────────────────────────────────────────────────────────
def load_training_data():
    """
    Read all dated training CSVs in TRAINING_DIR and combine them.
    """
    hitter_files = sorted(glob.glob(os.path.join(TRAINING_DIR, "*hitter_training*.csv")))
    pitcher_files = sorted(glob.glob(os.path.join(TRAINING_DIR, "*pitcher_training*.csv")))

    dfs_hit = [pd.read_csv(f) for f in hitter_files]
    dfs_pit = [pd.read_csv(f) for f in pitcher_files]

    df_hit = pd.concat(dfs_hit, ignore_index=True) if dfs_hit else pd.DataFrame()
    df_pit = pd.concat(dfs_pit, ignore_index=True) if dfs_pit else pd.DataFrame()

    # drop duplicates
    df_hit = df_hit.drop_duplicates()
    df_pit = df_pit.drop_duplicates()
    logger.info(f"Loaded training: {len(df_hit)} hitter rows, {len(df_pit)} pitcher rows")
    return df_hit, df_pit

# ── FEATURE PIPELINE ─────────────────────────────────────────────────────────────
def feature_engineering(df):
    # convert percent strings to floats
    pct_cols = [c for c in df.columns if '%' in c]
    for c in pct_cols:
        df[c] = df[c].astype(str).str.rstrip('%').astype(float) / 100

    # prop-type dummies
    if 'Prop Type' in df.columns:
        df = pd.concat([df, pd.get_dummies(df['Prop Type'], prefix='prop')], axis=1)
    return df.fillna(-999)

def get_model_features(df):
    CORE = [
        'Prop Value', 'Game-Time Temp (F)', 'Game-Time Humidity (%)', 'Game-Time Wind Speed (mph)',
        'AVG_vs_rhp','OBP_vs_rhp','SLG_vs_rhp','OPS_vs_rhp',
        'AVG_vs_lhp','OBP_vs_lhp','SLG_vs_lhp','OPS_vs_lhp',
        'wOBA','xwOBA','Barrel%','Hard Hit %',
        'ERA','WHIP','K/9','BB/9','K/BB','HR/9','K%','BB%','K-BB%','LOB%'
    ]
    cols = [c for c in CORE if c in df.columns]
    cols += [c for c in df.columns if c.startswith('prop_')]
    return df[cols]

# ── TRAINING ────────────────────────────────────────────────────────────────────
def train_all():
    hit_df, pit_df = load_training_data()
    master = pd.concat([hit_df, pit_df], ignore_index=True)
    master = feature_engineering(master)

    for prop in prop_list + pitcher_list:
        subset = master[master['Prop Type'] == prop]
        if subset.empty:
            logger.warning(f"No data for {prop}, skipping.")
            continue

        X = get_model_features(subset)
        y = subset['Hit'].astype(int)

        # skip single‐class problems
        if y.nunique() < 2:
            logger.warning(f"{prop} has only one class {y.unique().tolist()}, skipping.")
            continue

        n = len(y)
        cv = 3 if n >= 4 else 2  # require at least 2 folds

        # grid‐search on full data
        rf = RandomForestClassifier(random_state=42)
        gs = GridSearchCV(
            rf,
            param_grid={
                'n_estimators':    [100, 200],
                'max_depth':       [10, 20],
                'min_samples_leaf': [1, 2],
                'max_features':    ['sqrt']
            },
            cv=cv,
            scoring='neg_log_loss',
            n_jobs=-1
        )
        gs.fit(X, y)
        logger.info(f"{prop} best params: {gs.best_params_}, log-loss={-gs.best_score_:.4f}")

        # calibrate on same data folds
        calib = CalibratedClassifierCV(gs.best_estimator_, method='isotonic', cv=cv)
        calib.fit(X, y)

        path = os.path.join(MODEL_DIR, f"{prop.replace(' ','_')}_rf.pkl")
        joblib.dump({
            'model':    calib,
            'features': X.columns.tolist()
        }, path)
        logger.info(f"Saved {prop} model to {path}")

# ── PREDICTION ──────────────────────────────────────────────────────────────────
def daily_predictions():
    df_h = pd.read_csv(os.path.join(MLB_DATA_DIR, 'master_hitter_dataset.csv'))
    df_p = pd.read_csv(os.path.join(MLB_DATA_DIR, 'master_pitcher_dataset.csv'))
    df   = pd.concat([df_h, df_p], ignore_index=True)
    df   = feature_engineering(df)

    preds = []
    for prop in prop_list + pitcher_list:
        model_file = f"{prop.replace(' ', '_')}_rf.pkl"
        model_path = os.path.join(MODEL_DIR, model_file)
        if not os.path.exists(model_path):
            logger.warning(f"Model file missing for {prop}, skipping: {model_file}")
            continue

        sub = df[df['Prop Type'] == prop]
        if sub.empty:
            continue

        X   = get_model_features(sub)
        mdl = joblib.load(model_path)
        X   = X.reindex(columns=mdl['features'], fill_value=0)
        proba = mdl['model'].predict_proba(X)[:, 1]

        tmp = sub[['Player','Prop Type','Prop Value','Start Time']].copy()
        tmp['Model_Type']    = 'hitter' if prop in prop_list else 'pitcher'
        tmp['RF_Prediction'] = (proba >= 0.5).astype(int)
        tmp['RF_Confidence'] = proba

        # empty placeholder columns
        for col in [
            'LLM_Prediction','LLM_RF_Agreement','LLM_Confidence',
            'LLM_Justification','Actual_Stat','Actual_Result','Reflection'
        ]:
            tmp[col] = ''

        # reorder
        cols = [
            'Player','Prop Type','Prop Value','Start Time','Model_Type',
            'RF_Prediction','RF_Confidence',
            'LLM_Prediction','LLM_RF_Agreement','LLM_Confidence',
            'LLM_Justification','Actual_Stat','Actual_Result','Reflection'
        ]
        preds.append(tmp[cols])

    if not preds:
        logger.warning("No predictions generated; no models found.")
        return

    # no blank rows—just concatenate
    result = pd.concat(preds, ignore_index=True)
    result.to_csv(os.path.join(RESULTS_DIR, f"{TODAY}_mlb_predictions.csv"), index=False)

    top = result.sort_values('RF_Confidence', ascending=False).head(TOP_N)
    top.to_csv(os.path.join(RESULTS_DIR, f"{TODAY}_mlb_top_picks.csv"), index=False)

    logger.info(f"Saved {len(result)} predictions, top {TOP_N} to disk")

# ── CLI MENU ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    while True:
        print("\nMLB Machine Learning Pipeline")
        print("----------------------------")
        print("1. Make Daily Predictions")
        print("2. Train Models (Weekly)")
        print("3. Exit")

        choice = input("\nWhat would you like to do? (1/2/3): ").strip()
        if choice == '1':
            logger.info("Running daily predictions...")
            daily_predictions()
            print(f"\nPredictions saved to: {RESULTS_DIR}/{TODAY}_mlb_predictions.csv")
            print(f"Top picks saved to: {RESULTS_DIR}/{TODAY}_mlb_top_picks.csv")
        elif choice == '2':
            confirm = input("\nThis should only be done weekly. Proceed? (y/n): ").strip().lower()
            if confirm == 'y':
                logger.info("Running weekly training...")
                train_all()
                print("\nTraining completed!")
        elif choice == '3':
            print("\nExiting.")
            break
        else:
            print("\nInvalid choice. Please pick 1, 2, or 3.")