import pandas as pd
import os, json
from src.shared.schemas import MarketSummary

DATA_DIR = "data"
REPORT_DIR = "reports"

def summarize(role: str, location: str) -> MarketSummary:
    df = pd.read_csv(os.path.join(DATA_DIR, "synthetic_market.csv"))
    df = df[(df["role"] == role) & (df["location"] == location)]
    if df.empty:
        raise SystemExit(f"No market data for role={role} location={location}")
    median = float(df["salary"].median())
    p25 = float(df["salary"].quantile(0.25))
    p75 = float(df["salary"].quantile(0.75))
    channels = df["channel"].value_counts().index.tolist()[:3]
    return MarketSummary(role=role, location=location, median=median, p25=p25, p75=p75, recommended_channels=channels)

def run(role: str, location: str):
    os.makedirs(REPORT_DIR, exist_ok=True)
    ms = summarize(role, location)
    out = os.path.join(REPORT_DIR, f"Market_{role.replace(' ','_')}_{location}.json")
    with open(out, "w", encoding="utf-8") as f:
        f.write(ms.model_dump_json(indent=2))
    print(f"Generated: {out}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", required=True)
    ap.add_argument("--location", required=True)
    args = ap.parse_args()
    run(args.role, args.location)
