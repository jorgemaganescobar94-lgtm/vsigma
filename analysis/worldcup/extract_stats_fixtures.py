"""
PASO B - bounded extraction of /fixtures/statistics for World Cup teams (ISOLATED).

Real match stats only (corners, cards, shots, SOT, fouls, possession) for recent
international matches involving the 48 WC-2026 teams. NO market/odds. NOT production.

Design:
  * Candidate set = international_results.csv rows with date >= SINCE and at least one
    WC team, most-recent first.
  * HARD CAP: attempts at most MAX_FIXTURES fresh fixtures; also STOPS if the API quota
    rises past QUOTA_STOP (keeps headroom) — reports and exits cleanly either way.
  * RESUME: skips fixtures already in worldcup_stats_raw.csv (re-runs are ~free: the API
    client caches /fixtures/statistics for 30 days, so cached hits don't burn quota).
  * RETRIES: a few attempts per fixture on transient errors, then skip.
  * INCREMENTAL SAVE: flushes to CSV every FLUSH fixtures, so a stop never loses progress.

Output (one row per team per fixture): worldcup_stats_raw.csv
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from api_football_client import APIFootballClient, APIFootballError  # noqa: E402
from worldcup_learning_loop import CONF_BY_TEAM  # noqa: E402  (48-team WC set)

OUT_DIR = Path(__file__).resolve().parent
RESULTS = OUT_DIR / "international_results.csv"
RAW = OUT_DIR / "worldcup_stats_raw.csv"
REPORT = OUT_DIR / "worldcup_stats_extract_report.txt"

WC_TEAMS = set(CONF_BY_TEAM)
COLS = ["fixture_id", "date", "season", "league_tag", "neutral",
        "team", "team_id", "opp", "opp_id", "is_home",
        "corners", "yellow", "red", "shots", "sot", "fouls", "possession"]

# /fixtures/statistics 'type' -> our column
TYPE_MAP = {
    "Corner Kicks": "corners", "Yellow Cards": "yellow", "Red Cards": "red",
    "Total Shots": "shots", "Shots on Goal": "sot", "Fouls": "fouls",
    "Ball Possession": "possession",
}


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


def parse_stats(resp):
    """resp = /fixtures/statistics response. -> {team_id: {name, stats dict}}."""
    out = {}
    for t in resp:
        tm = t.get("team") or {}
        tid = tm.get("id")
        if tid is None:
            continue
        d = {"name": tm.get("name")}
        for s in t.get("statistics", []) or []:
            col = TYPE_MAP.get(s.get("type"))
            if col:
                d[col] = _num(s.get("value"))
        out[int(tid)] = d
    return out


def main(since, max_fixtures, quota_stop, flush, retries):
    c = APIFootballClient()

    def quota():
        try:
            return ((c.request("/status", None, ttl_hours=0, force_refresh=True)
                     .get("response", {}) or {}).get("requests") or {}).get("current")
        except Exception:
            return None

    df = pd.read_csv(RESULTS)
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce")
    df = df.dropna(subset=["date", "fixture_id"])
    cand = df[(df["date"] >= pd.Timestamp(since, tz="UTC"))
              & (df["home"].isin(WC_TEAMS) | df["away"].isin(WC_TEAMS))]
    cand = cand.sort_values("date", ascending=False)

    done = set()
    rows = []
    if RAW.exists():
        prev = pd.read_csv(RAW)
        rows = prev.to_dict("records")
        done = set(prev["fixture_id"].astype(int))

    report = []

    def log(s):
        print(s)
        report.append(s)

    q0 = quota()
    log(f"PASO B stats extraction | candidates={len(cand)} (since {since}, >=1 WC team) | "
        f"already saved={len(done)} fixtures | start quota={q0}/7500")
    log(f"caps: max_fixtures={max_fixtures} fresh-attempts | quota_stop={quota_stop} | flush={flush}")

    attempted = with_stats = 0
    stop_reason = "completed candidate list"
    for _, r in cand.iterrows():
        fid = int(r["fixture_id"])
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
        stats = parse_stats(resp)
        hid, aid = int(r["home_id"]), int(r["away_id"])
        if hid not in stats and aid not in stats:
            continue
        with_stats += 1
        for tid, oid, is_home, tname, oname in [(hid, aid, 1, r["home"], r["away"]),
                                                (aid, hid, 0, r["away"], r["home"])]:
            st = stats.get(tid)
            if not st:
                continue
            rows.append({
                "fixture_id": fid, "date": str(r["date"])[:10], "season": r.get("season"),
                "league_tag": r.get("league_tag"), "neutral": int(r.get("neutral") or 0),
                "team": tname, "team_id": tid, "opp": oname, "opp_id": oid, "is_home": is_home,
                "corners": st.get("corners"), "yellow": st.get("yellow"), "red": st.get("red"),
                "shots": st.get("shots"), "sot": st.get("sot"), "fouls": st.get("fouls"),
                "possession": st.get("possession"),
            })

        if attempted % flush == 0:
            pd.DataFrame(rows)[COLS].to_csv(RAW, index=False)
            print(f"  ... attempted {attempted}, with-stats {with_stats}, rows {len(rows)} (flushed)")

    pd.DataFrame(rows)[COLS].to_csv(RAW, index=False)
    q1 = quota()
    spend = (q1 - q0) if (q0 is not None and q1 is not None) else "n/a"

    # coverage report
    out_df = pd.DataFrame(rows)
    fix_with = out_df["fixture_id"].nunique() if len(out_df) else 0
    teams_cov = out_df["team"].nunique() if len(out_df) else 0
    wc_cov = sorted(WC_TEAMS & set(out_df["team"])) if len(out_df) else []
    log("")
    log(f"STOP: {stop_reason}")
    log(f"fresh attempts this run={attempted} | with-stats={with_stats} | API spend(delta)={spend} | quota now={q1}")
    log(f"TOTAL coverage: fixtures with stats={fix_with} | team-rows={len(out_df)} | distinct teams={teams_cov}")
    log(f"WC teams covered: {len(wc_cov)}/48")
    missing = sorted(WC_TEAMS - set(wc_cov))
    if missing:
        log(f"WC teams with NO stats yet: {missing}")
    if len(out_df):
        per = out_df.groupby("team").size().reindex(sorted(WC_TEAMS), fill_value=0)
        thin = per[per < 5]
        if len(thin):
            log(f"WC teams with <5 stat-matches (thin): {dict(thin[thin>0])} ; zero: {list(per[per==0].index)}")
        for col in ["corners", "yellow", "shots", "sot"]:
            nn = out_df[col].notna().sum()
            log(f"  field '{col}': {nn}/{len(out_df)} rows non-null ({nn/max(len(out_df),1)*100:.0f}%)")
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"\nWritten: {RAW}\nWritten: {REPORT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2022-08-01", help="earliest match date (UTC)")
    ap.add_argument("--max-fixtures", type=int, default=1500, help="HARD CAP on fresh fixtures attempted")
    ap.add_argument("--quota-stop", type=int, default=7200, help="stop if API quota current >= this")
    ap.add_argument("--flush", type=int, default=25)
    ap.add_argument("--retries", type=int, default=3)
    a = ap.parse_args()
    main(a.since, a.max_fixtures, a.quota_stop, a.flush, a.retries)
