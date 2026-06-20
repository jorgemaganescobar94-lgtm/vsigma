"""
FEATURE STUDY - bounded xG extraction from /fixtures/statistics (ISOLATED).

Re-reads the SAME fixtures already in worldcup_stats_raw.csv (the API client caches
/fixtures/statistics for 30 days, so this is ~free: cached hits don't burn quota).
Parses the 'expected_goals' stat per team. NO market/odds. NOT production.

HARD CAP on fresh attempts + QUOTA_STOP, resumable (skips fixtures already saved).
Output (one row per team per fixture): worldcup_xg_raw.csv
  fixture_id, team_id, opp_id, is_home, xg
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from api_football_client import APIFootballClient, APIFootballError  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
RAW = OUT_DIR / "worldcup_stats_raw.csv"          # source list of fixtures (already fetched)
XG = OUT_DIR / "worldcup_xg_raw.csv"
REPORT = OUT_DIR / "worldcup_xg_extract_report.txt"
COLS = ["fixture_id", "team_id", "opp_id", "is_home", "xg"]


def _num(v):
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip().rstrip("%")
        if v == "":
            return None
    try:
        return float(v)
    except Exception:
        return None


def parse_xg(resp):
    """resp = /fixtures/statistics response -> {team_id: xg or None}."""
    out = {}
    for t in resp:
        tm = t.get("team") or {}
        tid = tm.get("id")
        if tid is None:
            continue
        xg = None
        for s in t.get("statistics", []) or []:
            if s.get("type") == "expected_goals":
                xg = _num(s.get("value"))
        out[int(tid)] = xg
    return out


def main(max_fixtures, quota_stop, flush, retries):
    c = APIFootballClient()

    def quota():
        try:
            return ((c.request("/status", None, ttl_hours=0, force_refresh=True)
                     .get("response", {}) or {}).get("requests") or {}).get("current")
        except Exception:
            return None

    src = pd.read_csv(RAW)
    # one (fixture, team) per row already in the stats raw; reuse its team/opp/home layout
    fixtures = src[["fixture_id", "team_id", "opp_id", "is_home"]].drop_duplicates()
    fids = list(dict.fromkeys(src["fixture_id"].astype(int).tolist()))

    done = set()
    rows = []
    if XG.exists():
        prev = pd.read_csv(XG)
        rows = prev.to_dict("records")
        done = set(prev["fixture_id"].astype(int))

    report = []

    def log(s):
        print(s)
        report.append(s)

    q0 = quota()
    log(f"xG extraction | source fixtures={len(fids)} | already saved={len(done)} | start quota={q0}/7500")
    log(f"caps: max_fixtures={max_fixtures} | quota_stop={quota_stop}")

    attempted = with_xg = 0
    stop_reason = "completed fixture list"
    for fid in fids:
        if fid in done:
            continue
        if attempted >= max_fixtures:
            stop_reason = f"HARD CAP reached ({max_fixtures} fresh attempts)"
            break
        qn = quota()
        if qn is not None and qn >= quota_stop:
            stop_reason = f"QUOTA_STOP reached (quota {qn} >= {quota_stop})"
            break

        resp = None
        for attempt in range(retries):
            try:
                resp = c.fixture_statistics(fid).get("response", []) or []
                break
            except APIFootballError as e:
                if getattr(e, "is_plan_limit", False):
                    stop_reason = f"PLAN/LIMIT error: {e}"
                    resp = "ABORT"
                    break
                time.sleep(0.8 * (attempt + 1))
            except Exception:
                time.sleep(0.8 * (attempt + 1))
        if resp == "ABORT":
            break
        attempted += 1
        done.add(fid)
        if not resp:
            continue
        xgmap = parse_xg(resp)
        sub = fixtures[fixtures["fixture_id"] == fid]
        got = False
        for _, r in sub.iterrows():
            tid = int(r["team_id"])
            xg = xgmap.get(tid)
            if xg is not None:
                got = True
            rows.append({"fixture_id": fid, "team_id": tid, "opp_id": int(r["opp_id"]),
                         "is_home": int(r["is_home"]), "xg": xg})
        if got:
            with_xg += 1
        if attempted % flush == 0:
            pd.DataFrame(rows)[COLS].to_csv(XG, index=False)
            print(f"  ... attempted {attempted}, with-xg {with_xg}, rows {len(rows)} (flushed)")

    pd.DataFrame(rows)[COLS].to_csv(XG, index=False)
    q1 = quota()
    spend = (q1 - q0) if (q0 is not None and q1 is not None) else "n/a"
    out_df = pd.DataFrame(rows)
    nn = int(out_df["xg"].notna().sum()) if len(out_df) else 0
    fix_with_xg = out_df[out_df["xg"].notna()]["fixture_id"].nunique() if len(out_df) else 0
    log("")
    log(f"STOP: {stop_reason}")
    log(f"fresh attempts={attempted} | fixtures with >=1 xg={with_xg} | API spend(delta)={spend} | quota now={q1}")
    log(f"TOTAL rows={len(out_df)} | xg non-null={nn} ({nn/max(len(out_df),1)*100:.0f}%) | "
        f"fixtures with xg={fix_with_xg}/{len(fids)} ({fix_with_xg/max(len(fids),1)*100:.0f}%)")
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"\nWritten: {XG}\nWritten: {REPORT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-fixtures", type=int, default=1400, help="HARD CAP on fresh attempts")
    ap.add_argument("--quota-stop", type=int, default=7200)
    ap.add_argument("--flush", type=int, default=50)
    ap.add_argument("--retries", type=int, default=3)
    a = ap.parse_args()
    main(a.max_fixtures, a.quota_stop, a.flush, a.retries)
