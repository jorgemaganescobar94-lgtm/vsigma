"""
BOUNDED PROBE (ISOLATED, analysis/worldcup/) — does API-Football carry expected_goals (xG)
for OLD international national-team fixtures, especially PRE-2024?

Samples a few FT fixtures per (competition, year) from the already-cached
international_results.csv (0 API for the lists) and calls /fixtures/statistics on the
sample only, checking whether expected_goals is PRESENT & non-null. NO backfill, NO
production change. Hard call cap + quota stop. /fixtures/statistics is cached 30d so
re-runs are free.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from api_football_client import APIFootballClient, APIFootballError  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
IR = OUT_DIR / "international_results.csv"
REPORT = OUT_DIR / "xg_coverage_probe_report.txt"
CSV = OUT_DIR / "xg_coverage_probe.csv"

SAMPLE_PER_BUCKET = 5
HARD_CALL_CAP = 100          # max fresh /fixtures/statistics attempts
QUOTA_STOP = 300             # stop if daily quota current >= this (well under 7500)

# Fan across years/competitions, PRE-2024 prioritised (the gap that sank the last test).
FAN = [
    ("WC", 2018), ("WC", 2022),
    ("Euro", 2021), ("Euro", 2024),
    ("CopaAmerica", 2019), ("CopaAmerica", 2021), ("CopaAmerica", 2024),
    ("UNL", 2018), ("UNL", 2020), ("UNL", 2022), ("UNL", 2024),
    ("WCQ_Europe", 2021),
    ("AFCON", 2019), ("AFCON", 2022),
    ("AsianCup", 2019),
    ("Friendlies", 2018), ("Friendlies", 2021), ("Friendlies", 2023), ("Friendlies", 2024),
]


def _has_xg(resp):
    """resp = /fixtures/statistics response -> (n_team_rows, n_with_expected_goals)."""
    n = got = 0
    for t in resp or []:
        n += 1
        for s in t.get("statistics", []) or []:
            if s.get("type") == "expected_goals" and s.get("value") not in (None, ""):
                got += 1
                break
    return n, got


def sample_fixtures(df, tag, year, k):
    sub = df[(df["league_tag"] == tag) & (df["y"] == year)].copy()
    if not len(sub):
        return []
    sub = sub.sort_values("date")
    idx = np.linspace(0, len(sub) - 1, min(k, len(sub))).round().astype(int)
    idx = sorted(set(idx.tolist()))
    return sub.iloc[idx]["fixture_id"].astype(int).tolist()


def main():
    c = APIFootballClient()

    def quota():
        try:
            return ((c.request("/status", None, ttl_hours=0, force_refresh=True)
                     .get("response", {}) or {}).get("requests") or {}).get("current")
        except Exception:
            return None

    df = pd.read_csv(IR)
    df["y"] = pd.to_datetime(df["date"], utc=True, errors="coerce").dt.year

    report = []

    def out(s=""):
        print(s); report.append(s)

    q0 = quota()
    out("=" * 92)
    out("XG COVERAGE PROBE — expected_goals availability for international fixtures (sampled)")
    out("=" * 92)
    out(f"sample/bucket={SAMPLE_PER_BUCKET} | hard cap={HARD_CALL_CAP} stat calls | "
        f"quota_stop={QUOTA_STOP} | start quota={q0}/7500")
    out("")
    out(f"  {'competition':14} {'year':>5} {'sampled':>8} {'with_xg':>8} {'cov%':>6}  note")
    out("-" * 92)

    calls = 0
    rows = []
    stop = "complete"
    for tag, year in FAN:
        if calls >= HARD_CALL_CAP:
            stop = "HARD_CALL_CAP"
            break
        qn = quota()
        if qn is not None and qn >= QUOTA_STOP:
            stop = f"QUOTA_STOP ({qn})"
            break
        fids = sample_fixtures(df, tag, year, SAMPLE_PER_BUCKET)
        if not fids:
            out(f"  {tag:14} {year:>5} {'-':>8} {'-':>8} {'-':>6}  (no fixtures in dataset)")
            continue
        sampled = with_xg = 0
        for fid in fids:
            if calls >= HARD_CALL_CAP:
                stop = "HARD_CALL_CAP"
                break
            try:
                resp = c.fixture_statistics(fid).get("response", []) or []
            except APIFootballError as e:
                if getattr(e, "is_plan_limit", False):
                    stop = f"PLAN_LIMIT: {e}"
                    rows.append({"tag": tag, "year": year, "fixture_id": fid, "n_rows": None, "n_xg": None})
                    break
                resp = []
            except Exception:
                resp = []
            calls += 1
            n_rows, n_xg = _has_xg(resp)
            sampled += 1
            if n_xg > 0:
                with_xg += 1
            rows.append({"tag": tag, "year": year, "fixture_id": fid, "n_rows": n_rows, "n_xg": n_xg})
        cov = (100.0 * with_xg / sampled) if sampled else 0.0
        era = "PRE-2024" if year < 2024 else "2024+"
        out(f"  {tag:14} {year:>5} {sampled:>8} {with_xg:>8} {cov:>5.0f}%  {era}")
        if stop != "complete":
            break

    out("-" * 92)
    rdf = pd.DataFrame(rows)
    pre = rdf[(rdf["year"] < 2024) & rdf["n_xg"].notna()]
    post = rdf[(rdf["year"] >= 2024) & rdf["n_xg"].notna()]

    def agg(sub):
        if not len(sub):
            return (0, 0, 0.0)
        s = len(sub); w = int((sub["n_xg"] > 0).sum())
        return s, w, (100.0 * w / s if s else 0.0)

    ps, pw, pc = agg(pre)
    qs, qw, qc = agg(post)
    out("SUMMARY")
    out(f"  PRE-2024 sampled fixtures: {ps} | with xG: {pw} ({pc:.0f}%)")
    out(f"  2024+    sampled fixtures: {qs} | with xG: {qw} ({qc:.0f}%)")
    out("")
    q1 = quota()
    spend = (q1 - q0) if (q0 is not None and q1 is not None) else "n/a"
    out(f"STOP: {stop}")
    out(f"fresh stat attempts this run: {calls} | API spend (status delta): {spend} | quota now: {q1}/7500")

    rdf.to_csv(CSV, index=False)
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"\nWritten: {REPORT}")
    print(f"Written: {CSV}")


if __name__ == "__main__":
    main()
