import glob
import os
import sys
import math
import json
from datetime import datetime
import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

MLB_RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'MLB_Results')
XGB_CSV_PATH     = os.path.join(MLB_RESULTS_DIR, "xgboost_accuracy.csv")


def _sanitize_records(records):
    """
    Replace any NaN/Inf in a list of dicts with None so JSON stays valid.
    """
    clean_list = []
    for rec in records:
        clean = {}
        for k, v in rec.items():
            if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                clean[k] = None
            else:
                clean[k] = v
        clean_list.append(clean)
    return clean_list


def calc_bankroll_history(starting_bankroll=500, start_date='2025-06-13'):
    """
    Load all *_generated_betslips.json files, compute daily P&L and running bankroll.
    """
    files = sorted(glob.glob(os.path.join(MLB_RESULTS_DIR, "*_generated_betslips.json")))
    bankroll = starting_bankroll
    history  = []

    # Day 0
    history.append({
        "date": start_date,
        "bankroll": bankroll,
        "daily_pnl": 0,
        "num_slips": 0,
        "num_won": None,
        "total_staked": 0,
        "total_returned": None,
        "net_result": None
    })

    for fpath in files:
        date = os.path.basename(fpath).split('_')[0]
        if date < start_date:
            continue

        with open(fpath) as fp:
            slips = json.load(fp)

        num_slips    = len(slips)
        day_staked   = sum(float(s.get('stake', 0)) for s in slips)
        day_returned = 0.0
        num_won      = 0

        # only count if every slip has a 'hit'
        scored = bool(slips and all('hit' in s for s in slips))
        for s in slips:
            if s.get('hit'):
                num_won += 1
                day_returned += float(s.get('stake', 0)) * float(s.get('payout_multiplier', 1))

        net = (day_returned - day_staked) if scored else None
        if net is not None:
            bankroll += net

        history.append({
            "date": date,
            "bankroll": bankroll,
            "daily_pnl": net,
            "num_slips": num_slips,
            "num_won":  num_won,
            "total_staked":   day_staked,
            "total_returned": day_returned if scored else None,
            "net_result":     net
        })

    return history


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/dashboard-data')
def dashboard_data():
    # ── Load accuracy summary ──────────────────────────
    acc_path = os.path.join(MLB_RESULTS_DIR, "MLB_Prop_Accuracy.csv")
    if not os.path.exists(acc_path):
        return jsonify(success=False, error="MLB_Prop_Accuracy.csv not found"), 500

    acc_df = pd.read_csv(acc_path).fillna(0)

    # ── 1) Historical performance ──────────────────────
    history = []
    for _, row in acc_df.iterrows():
        history.append({
            "date": row["Date"],
            "total": int(row["Total_Predictions"]),
            "rf_accuracy": float(row["RF_Accuracy"]),
            "llm_accuracy": float(row["LLM_Accuracy"]),
            "agreement_accuracy": float(row["Agreement_Accuracy"])
        })

    # ── 2) Latest overall metrics ─────────────────────
    latest   = acc_df.iloc[-1]
    latest_date = latest["Date"]
    overall = {
        "total":           int(latest["Total_Predictions"]),
        "rf_accuracy":     float(latest["RF_Accuracy"]),
        "llm_accuracy":    float(latest["LLM_Accuracy"]),
        "agreement_accuracy": float(latest["Agreement_Accuracy"]),
        "agreement_count": int(latest["Agreement_Count"])
    }

    # ── 3) Prop-Type summary ───────────────────────────
    prop_types = {}
    for col in acc_df.columns:
        if (col.endswith("_Count")
            and col not in ("Total_Predictions", "Agreement_Count")
            and not col.endswith("_Agreement_Count")):
            prop = col[:-6]  # strip _Count

            cnt = int(latest.get(f"{prop}_Count", 0))
            rf  = float(latest.get(f"{prop}_RF_Accuracy", 0.0))
            llm = float(latest.get(f"{prop}_LLM_Accuracy", 0.0))

            prop_types[prop] = {
                "count":       cnt,
                "rf_accuracy": rf,
                "llm_accuracy": llm
            }

    # ── 3B) All-Time Prop-Type Agreement-Only Accuracy ──
    alltime_prop_accuracy = []
    agr_cols = [
        c for c in acc_df.columns
        if c.endswith("_Agreement_Count") and c != "Agreement_Count"
    ]
    for agr in agr_cols:
        prop = agr[:-len("_Agreement_Count")]
        total_agreements = int(acc_df[agr].sum())
        if total_agreements == 0:
            alltime_prop_accuracy.append({
                "prop_type": prop.replace("_", " "),
                "total": 0,
                "accuracy": None
            })
            continue

        rate_col = f"{prop}_Agreement_Accuracy"
        if rate_col in acc_df.columns:
            daily_counts = acc_df[agr]
            daily_rates  = acc_df[rate_col]
            total_correct = (daily_counts * daily_rates).sum()
            acc = round(float(total_correct) / total_agreements, 4)
        else:
            acc = None

        alltime_prop_accuracy.append({
            "prop_type": prop.replace("_", " "),
            "total": total_agreements,
            "accuracy": acc
        })

    # ── 4) Recent High-Confidence picks (RF ≥ 80%) ─────────────────
    recent_predictions = []
    top_files = sorted(glob.glob(os.path.join(MLB_RESULTS_DIR, "*_mlb_top_picks.csv")))
    if top_files:
        dfs = []
        for f in top_files:
            try:
                tmp = pd.read_csv(f)
            except:
                continue
            tmp["Date"] = os.path.basename(f).split("_")[0]
            dfs.append(tmp)
        if dfs:
            tops = pd.concat(dfs, ignore_index=True)
            # drop rows without actual result
            if "Actual_Result" in tops:
                tops = tops[tops["Actual_Result"].notna()]
            # only keep RF_Confidence ≥ 0.8
            tops["RF_Confidence"] = tops["RF_Confidence"].astype(float)
            tops = tops[tops["RF_Confidence"] >= 0.8]
            # format RF_Confidence as "88.3%" strings
            tops["RF_Confidence"] = (tops["RF_Confidence"] * 100).round(1).astype(str) + '%'
            # take the 20 most‐recent
            rec = tops.sort_values("Date").tail(20)
            recent_predictions = _sanitize_records(
                rec.to_dict(orient="records")
            )

    # ── 5) Today's Betslips ─────────────────────────────
    betslips = []
    today = datetime.now().strftime("%Y-%m-%d")
    slip_file = os.path.join(MLB_RESULTS_DIR, f"{today}_generated_betslips.json")
    if os.path.exists(slip_file):
        with open(slip_file) as fp:
            betslips = json.load(fp)

    # ── 6) XGB Overall & By-Prop ────────────────────────
    xgb_metrics  = []
    xgb_by_prop  = {}
    prop_type_fields = [
        "Hits+Runs+RBIs", "Hitter_Fantasy_Score", "Hits", "Total_Bases", "Runs",
        "Walks", "Hitter_Strikeouts", "Earned_Runs_Allowed", "Pitches_Thrown",
        "Pitcher_Strikeouts", "Pitcher_Fantasy_Score", "Pitching_Outs"
    ]
    if os.path.exists(XGB_CSV_PATH):
        xgb_df = pd.read_csv(XGB_CSV_PATH)
        xgb_metrics = _sanitize_records(xgb_df.to_dict(orient="records"))

        for prop in prop_type_fields:
            safe = prop.replace(" ", "_")
            rows = []
            for _, r in xgb_df.iterrows():
                rows.append({
                    "date":         r["Date"],
                    "xgb_accuracy": r.get(f"{prop}_XGB_Accuracy", None),
                    "xgb_correct":  r.get(f"{prop}_XGB_Correct",  None),
                    "count":        r.get(f"{prop}_XGB_Total",    None),
                })
            xgb_by_prop[prop] = _sanitize_records(rows)

    # ── 7) Bankroll history ─────────────────────────────
    bankroll_history = calc_bankroll_history()

    # ── 8) Confidence-Weighted Accuracy Breakdown ───────────────────────
    band_ranges = [
        (0.50, 0.60, "50-60%"),
        (0.60, 0.70, "60-70%"),
        (0.70, 0.80, "70-80%"),
        (0.80, 0.90, "80-90%"),
        (0.90, 1.00, "90-100%")
    ]
    # init counters
    confidence_bands = {lbl: {"correct": 0, "total": 0} for *_, lbl in band_ranges}

    def parse_conf(x):
        """Convert '89.5%' or 0.895 → float between 0 and 1, else None."""
        try:
            if isinstance(x, str) and x.endswith('%'):
                return float(x.rstrip('%')) / 100
            return float(x)
        except:
            return None

    for fp in glob.glob(os.path.join(MLB_RESULTS_DIR, "*_mlb_top_picks.csv")):
        try:
            df = pd.read_csv(fp)
            # drop rows with no conf or no actual result
            df["RF_Confidence"] = df["RF_Confidence"].apply(parse_conf)
            df = df[df["RF_Confidence"].notna() & df["Actual_Result"].notna()]
            # determine correctness
            df["Correct"] = (
                    df["Prediction"].astype(int)
                    .map({1: "Over", 0: "Under"})
                    == df["Actual_Result"]
            )
            # bucket
            for _, row in df.iterrows():
                c = row["RF_Confidence"]
                for lo, hi, lbl in band_ranges:
                    if (lo <= c < hi) or (lbl == "90-100%" and abs(c - hi) < 1e-6):
                        confidence_bands[lbl]["total"] += 1
                        confidence_bands[lbl]["correct"] += int(row["Correct"])
                        break
        except Exception:
            continue

    # build an ARRAY of band objects
    confidence_accuracy = []
    for _, _, label in band_ranges:
        tot = confidence_bands[label]["total"]
        corr = confidence_bands[label]["correct"]
        acc = round(corr / tot, 3) if tot else 0
        confidence_accuracy.append({
            "band": label,
            "total": tot,
            "correct": corr,
            "accuracy": acc
        })

    # --- assemble payload ---
    data = {
        "latest_date": latest_date,
        "overall": overall,
        "prop_types": prop_types,
        "alltime_prop_accuracy": alltime_prop_accuracy,
        "historical_data": history,
        "recent_predictions": recent_predictions,
        "betslips": betslips,
        "xgb_comparison": xgb_metrics,
        "xgb_by_prop": xgb_by_prop,
        "bankroll_history": bankroll_history,
        "confidence_accuracy": confidence_accuracy
    }

    return jsonify(success=True, data=data)


@app.route('/api/mlb-insights')
def mlb_insights():
    INSIGHTS_JSON = os.path.join(MLB_RESULTS_DIR, "mlb_insights_db.json")
    try:
        with open(INSIGHTS_JSON) as fp:
            db = json.load(fp)
        return jsonify(success=True, insights=db.get("prop_types", {}))
    except Exception as e:
        app.logger.error(f"Error loading insights: {e}")
        return jsonify(success=False, error=str(e)), 500


@app.route('/api/bankroll-llm')
def bankroll_llm():
    try:
        # get full history
        history = calc_bankroll_history()  # uses default starting_bankroll & start_date
        today = datetime.now().strftime("%Y-%m-%d")
        # pick the last entry _before_ today
        past = [h for h in history if h["date"] < today]
        if past:
            last = past[-1]
            return jsonify(
                success=True,
                bankroll=last["bankroll"],
                net_result_yesterday=last["net_result"],
                yesterday_date=last["date"]
            )
        # no prior days
        return jsonify(
            success=True,
            bankroll=history[0]["bankroll"],
            net_result_yesterday=None,
            yesterday_date=None
        )
    except Exception as e:
        app.logger.error(f"bankroll-llm error: {e}")
        return jsonify(success=False, error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)