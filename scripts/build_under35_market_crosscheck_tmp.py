import json
from pathlib import Path
import pandas as pd

CSV = Path("data/modeling/models/vsigma_under35_shadow_candidates.csv")
OUT = Path("data/modeling/models/vsigma_under35_shadow_market_crosscheck.json")

df = pd.read_csv(CSV)
df["model_under35_prob"] = pd.to_numeric(df["model_under35_prob"], errors="coerce")
df["actual_under35"] = pd.to_numeric(df["actual_under35"], errors="coerce")
df["feat_market_under25_prob"] = pd.to_numeric(df["feat_market_under25_prob"], errors="coerce")
df["feat_market_over25_prob"] = pd.to_numeric(df["feat_market_over25_prob"], errors="coerce")

blocks = []

for p_th in [0.75, 0.80, 0.85]:
    for market_u25_th in [0.45, 0.50, 0.55, 0.60]:
        m = (df["model_under35_prob"] >= p_th) & (df["feat_market_under25_prob"] >= market_u25_th)
        if int(m.sum()) == 0:
            continue
        blocks.append({
            "model_under35_threshold": p_th,
            "market_under25_threshold": market_u25_th,
            "rows": int(m.sum()),
            "actual_under35_rate": float(df.loc[m, "actual_under35"].mean()),
            "avg_model_under35_prob": float(df.loc[m, "model_under35_prob"].mean()),
            "avg_market_under25_prob": float(df.loc[m, "feat_market_under25_prob"].mean()),
            "avg_market_over25_prob": float(df.loc[m, "feat_market_over25_prob"].mean())
        })

league_blocks = []

for p_th in [0.75, 0.80, 0.85]:
    m0 = df["model_under35_prob"] >= p_th
    for league, g in df.loc[m0].groupby("league_name"):
        if len(g) < 10:
            continue
        league_blocks.append({
            "model_under35_threshold": p_th,
            "league_name": league,
            "rows": int(len(g)),
            "actual_under35_rate": float(g["actual_under35"].mean()),
            "avg_model_under35_prob": float(g["model_under35_prob"].mean()),
            "avg_market_under25_prob": float(g["feat_market_under25_prob"].mean())
        })

result = {
    "market_crosscheck": blocks,
    "league_crosscheck": league_blocks,
    "governance_read": {
        "p_under35_0_80_plus": "strong candidate gate",
        "p_under35_0_85_plus": "elite but sample smaller",
        "requires_market_check": True,
        "do_not_auto_bet": True
    }
}

OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=False))
