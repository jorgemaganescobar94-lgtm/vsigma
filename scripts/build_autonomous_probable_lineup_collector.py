from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
OUT_FIELDS = [
    "target_date","generated_at","fixture_id","league","country","home_team","away_team","team_side",
    "source_name","source_url","probable_xi","discovery_status","extract_status","notes","auto_apply","production_change",
]
REPORT_FIELDS = [
    "target_date","generated_at","fixtures_reviewed","search_provider","urls_discovered","rows_extracted",
    "status_counts","source_counts","auto_apply","production_change",
]
DOMAINS = {
    "sportsmole.co.uk":"sportsmole",
    "whoscored.com":"whoscored",
    "rotowire.com":"rotowire",
    "sportsgambler.com":"sports_gambler",
    "sports-gambler.com":"sports_gambler",
    "theguardian.com":"guardian_predicted",
    "sportskeeda.com":"sportskeeda",
    "90min.com":"ninetymin",
    "footballtransfers.com":"footballtransfers",
    "lequipe.fr":"lequipe",
    "maxifoot.fr":"maxifoot",
    "madeinfoot.com":"madeinfoot",
    "getfootballnewsfrance.com":"gffn",
    "standard.co.uk":"standard_sport",
}
SOURCE_QUERY_PLANS = [
    ("generic", "{home} vs {away} {year} probable lineups predicted XI team news"),
    ("sportsmole", "site:sportsmole.co.uk {home} vs {away} {year} possible starting lineup"),
    ("whoscored", "site:whoscored.com {home} {away} {year} preview probable lineups"),
    ("sports_gambler", "site:sportsgambler.com {home} {away} {year} predicted lineups"),
    ("rotowire", "site:rotowire.com soccer {home} {away} {year} expected lineups"),
    ("guardian_predicted", "site:theguardian.com football {home} {away} {year} team news predicted lineup"),
    ("sportskeeda", "site:sportskeeda.com {home} vs {away} {year} prediction team news lineups"),
    ("ninetymin", "site:90min.com {home} {away} {year} predicted lineup team news"),
    ("footballtransfers", "site:footballtransfers.com {home} {away} {year} predicted lineup"),
    ("lequipe", "site:lequipe.fr {home} {away} {year} composition probable"),
    ("maxifoot", "site:maxifoot.fr {home} {away} {year} composition probable"),
    ("madeinfoot", "site:madeinfoot.com {home} {away} {year} composition probable"),
    ("gffn", "site:getfootballnewsfrance.com {home} {away} {year} team news lineup"),
    ("standard_sport", "site:standard.co.uk sport football {home} {away} {year} predicted lineup team news"),
]
NARRATIVE_TOKENS = {
    "suggesting", "hosts", "host", "visitors", "win", "draw", "prediction", "preview", "betting",
    "odds", "team news", "sports mole", "article", "subscribe", "will", "should", "could", "match",
    "lineup", "line-up", "confirmed", "probable", "possible", "starting", "formation", "manager", "coach",
}
STOP_SECTION_RE = re.compile(
    r"(?:substitutes|bench|manager|coach|injured|doubtful|unavailable|sports mole|prediction|betting|odds|"
    r"team news|preview|match preview|how you voted|data analysis|latest|remplacants|absents|entraîneur)",
    re.I,
)


def s(x): return "" if x is None else str(x).strip()
def read(p: Path):
    if not p.exists(): return []
    with p.open("r",encoding="utf-8-sig",newline="") as f: return [dict(r) for r in csv.DictReader(f)]
def write(p: Path, rows, fields):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def d(day,name): return P/"today"/day/name

def fixtures(day):
    for name in ["matches_vsigma_scored_v3.csv","vsigma_daily_execution_board.csv","matches_league_filtered.csv"]:
        rows=read(d(day,name))
        if rows: return rows
    return []

def allowed_sources(day):
    regs=read(d(day,"vsigma_probable_lineup_source_registry.csv")) or read(P/"governance"/"vsigma_probable_lineup_source_registry.csv")
    return {s(r.get("source_name")):r for r in regs if s(r.get("enabled")).upper()=="YES" and s(r.get("status")).upper()=="ACTIVE"}

def source_for_url(url):
    host=urllib.parse.urlparse(url).netloc.lower().replace("www.","")
    for domain, name in DOMAINS.items():
        if host.endswith(domain): return name
    return ""

def norm_url(url):
    parsed=urllib.parse.urlparse(url)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc.lower(), parsed.path.rstrip("/"), "", parsed.query, ""))

def fixture_dt(fx):
    raw=s(fx.get("fixture_datetime_utc") or fx.get("date"))
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except Exception:
        try:
            return datetime.fromisoformat(raw[:10])
        except Exception:
            return None

def fixture_year(fx):
    dt=fixture_dt(fx)
    if dt:
        return str(dt.year)
    raw=s(fx.get("date"))
    return raw[:4] if len(raw)>=4 and raw[:4].isdigit() else ""

def fixture_date_markers(fx):
    dt=fixture_dt(fx)
    if not dt:
        return []
    month=dt.strftime("%B")
    short=dt.strftime("%b")
    day=str(dt.day)
    year=str(dt.year)
    return [
        f"{month} {day}, {year}",
        f"{short} {day}, {year}",
        f"{day} {month} {year}",
        f"{day} {short} {year}",
        f"{month} {day}",
        f"{short} {day}",
    ]

def team_token_match(text, team):
    t=team.lower().replace(".", "")
    txt=text.lower().replace(".", "")
    if t in txt:
        return True
    parts=[p for p in re.split(r"\s+|-", t) if len(p) >= 4]
    return bool(parts and any(p in txt for p in parts))

def page_relevance(fx, structured, source):
    txt=structured.lower()
    home=s(fx.get("home_team")); away=s(fx.get("away_team"))
    if home and not team_token_match(txt, home):
        return False, "HOME_TEAM_NOT_FOUND"
    if away and not team_token_match(txt, away):
        return False, "AWAY_TEAM_NOT_FOUND"
    year=fixture_year(fx)
    markers=[m.lower() for m in fixture_date_markers(fx)]
    if source == "sportsmole" and markers:
        if not any(m in txt for m in markers[:4]):
            return False, "FIXTURE_DATE_NOT_FOUND"
    elif year and year not in txt:
        return False, "FIXTURE_YEAR_NOT_FOUND"
    return True, "RELEVANT_FIXTURE_PAGE"

def http_json(url, headers=None):
    req=urllib.request.Request(url,headers=headers or {"User-Agent":"vSIGMA/1.0"})
    with urllib.request.urlopen(req,timeout=12) as r:
        return json.loads(r.read().decode("utf-8","replace"))

def http_text(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 vSIGMA probable-lineup research"})
    with urllib.request.urlopen(req,timeout=12) as r:
        return r.read().decode("utf-8","replace")

def search_web(query):
    serp=os.environ.get("SERPAPI_KEY")
    bing=os.environ.get("BING_SEARCH_API_KEY") or os.environ.get("AZURE_BING_SEARCH_KEY")
    if serp:
        try:
            url="https://serpapi.com/search.json?"+urllib.parse.urlencode({"engine":"google","q":query,"api_key":serp,"num":"5"})
            data=http_json(url)
            if data.get("error"):
                return "SERPAPI_ERROR", []
            return "SERPAPI", [(x.get("title",""),x.get("link",""),x.get("snippet","")) for x in data.get("organic_results",[])[:5]]
        except Exception:
            return "SERPAPI_SEARCH_FAILED", []
    if bing:
        try:
            url="https://api.bing.microsoft.com/v7.0/search?"+urllib.parse.urlencode({"q":query,"count":"5"})
            data=http_json(url,{"Ocp-Apim-Subscription-Key":bing,"User-Agent":"vSIGMA/1.0"})
            return "BING", [(x.get("name",""),x.get("url",""),x.get("snippet","")) for x in data.get("webPages",{}).get("value",[])[:5]]
        except Exception:
            return "BING_SEARCH_FAILED", []
    return "NO_SEARCH_KEY", []

def clean_text(page):
    page=re.sub(r"<script[\s\S]*?</script>"," ",page,flags=re.I)
    page=re.sub(r"<style[\s\S]*?</style>"," ",page,flags=re.I)
    text=re.sub(r"<[^>]+>"," ",page)
    text=html.unescape(text)
    return re.sub(r"\s+"," ",text)

def structured_text(page):
    page=re.sub(r"<script[\s\S]*?</script>"," ",page,flags=re.I)
    page=re.sub(r"<style[\s\S]*?</style>"," ",page,flags=re.I)
    page=re.sub(r"<br\s*/?>", "; ", page, flags=re.I)
    page=re.sub(r"</(?:p|div|li|h1|h2|h3|h4|strong|b|section|article)>", "\n", page, flags=re.I)
    page=re.sub(r"<[^>]+>", " ", page)
    page=html.unescape(page)
    lines=[]
    for line in page.splitlines():
        line=re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)

def clean_candidate_name(name):
    name=re.sub(r"\([^)]*\)", " ", s(name))
    name=re.sub(r"\s+", " ", name).strip(" -–—:;,.()[]")
    return name

def split_candidate_players(raw):
    raw=s(raw)
    raw=STOP_SECTION_RE.split(raw)[0]
    if raw.count(";") + raw.count(",") < 7:
        return []
    parts=[clean_candidate_name(p) for p in re.split(r"[;,|]", raw)]
    out=[]
    for p in parts:
        lp=p.lower()
        if not p or len(p) < 3 or len(p) > 45:
            continue
        if len(p.split()) >= 6:
            return []
        if any(tok in lp for tok in NARRATIVE_TOKENS):
            return []
        if p not in out:
            out.append(p)
    return out[:11] if len(out) >= 8 else []

def candidate_after_marker(line, markers):
    lower=line.lower()
    for marker in markers:
        idx=lower.find(marker)
        if idx >= 0:
            return line[idx + len(marker):].strip(" :-–—")
    return ""

def extract_section_xi(structured, team, source):
    team_l=team.lower()
    lines=structured.splitlines()
    markers=["possible starting lineup", "predicted lineup", "possible xi", "predicted xi", "composition probable"]
    for i,line in enumerate(lines):
        lower=line.lower()
        if team_l not in lower:
            continue
        if not any(marker in lower for marker in markers):
            continue
        chunk=candidate_after_marker(line, markers)
        for nxt in lines[i+1:i+4]:
            if any(marker in nxt.lower() for marker in markers) and team_l not in nxt.lower():
                break
            if STOP_SECTION_RE.search(nxt):
                break
            chunk += "; " + nxt
            players=split_candidate_players(chunk)
            if players:
                return "; ".join(players), f"{source}_structured_section"
        players=split_candidate_players(chunk)
        if players:
            return "; ".join(players), f"{source}_heading_line"
    return "", "NO_SECTION_XI"

def extract_generic_xi(text, team):
    team_re=re.escape(team)
    patterns=[
        rf"{team_re}.{{0,250}}possible starting lineup:?\s*([^\.]+)",
        rf"possible {team_re} starting lineup:?\s*([^\.]+)",
        rf"{team_re}.{{0,250}}predicted lineup:?\s*([^\.]+)",
        rf"{team_re}.{{0,250}}possible xi:?\s*([^\.]+)",
        rf"predicted {team_re} xi:?\s*([^\.]+)",
        rf"{team_re}.{{0,250}}composition probable:?\s*([^\.]+)",
        rf"composition probable {team_re}:?\s*([^\.]+)",
    ]
    for pat in patterns:
        try:
            m=re.search(pat,text,flags=re.I)
        except re.error:
            continue
        if not m:
            continue
        players=split_candidate_players(m.group(1))
        if players:
            return "; ".join(players), "generic_regex"
    return "", "NO_REGEX_XI"

def extract_xi_by_source(raw_page, text, structured, team, source):
    if source == "sportsmole":
        xi, method = extract_section_xi(structured, team, "sportsmole")
        return (xi, method) if xi else ("", method)
    xi, method = extract_section_xi(structured, team, source)
    if xi:
        return xi, method
    return extract_generic_xi(text, team)

def build_queries(fx, allowed):
    home=s(fx.get("home_team")); away=s(fx.get("away_team")); year=fixture_year(fx)
    max_q=int(os.environ.get("VSIGMA_MAX_PROBABLE_LINEUP_SEARCH_QUERIES", "8"))
    plans=[]
    for expected, template in SOURCE_QUERY_PLANS:
        if expected != "generic" and expected not in allowed:
            continue
        plans.append((expected, template.format(home=home, away=away, year=year)))
    return plans[:max_q]

def candidate_urls(fx, allowed):
    discovered=[]; seen=set(); providers=[]
    for expected, query in build_queries(fx, allowed):
        provider, results=search_web(query)
        providers.append(provider)
        if provider in {"NO_SEARCH_KEY","SERPAPI_ERROR","SERPAPI_SEARCH_FAILED","BING_SEARCH_FAILED"}:
            continue
        for title,url,snippet in results:
            src=source_for_url(url)
            if not src or src not in allowed:
                continue
            if expected != "generic" and src != expected:
                continue
            key=norm_url(url)
            if key in seen:
                continue
            seen.add(key)
            discovered.append((provider,src,url,title,snippet,expected))
    provider_summary=";".join(dict.fromkeys(providers)) if providers else "NO_SEARCH_KEY"
    return provider_summary, discovered

def build(day,tz):
    ts=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"); allowed=allowed_sources(day); out=[]; urls_seen=0
    provider="NO_SEARCH_KEY"
    for fx in fixtures(day):
        fid=s(fx.get("fixture_id")); home=s(fx.get("home_team")); away=s(fx.get("away_team"))
        try:
            provider, urls=candidate_urls(fx, allowed)
        except Exception as e:
            provider, urls = "SEARCH_EXCEPTION", []
            out.append({"target_date":day,"generated_at":ts,"fixture_id":fid,"league":s(fx.get("league")),"country":s(fx.get("country")),"home_team":home,"away_team":away,"team_side":"","source_name":"","source_url":"","probable_xi":"","discovery_status":"SEARCH_EXCEPTION","extract_status":"NO_DATA","notes":str(e)[:160],"auto_apply":"NO","production_change":"NO"})
        urls_seen += len(urls)
        if not urls:
            out.append({"target_date":day,"generated_at":ts,"fixture_id":fid,"league":s(fx.get("league")),"country":s(fx.get("country")),"home_team":home,"away_team":away,"team_side":"","source_name":"","source_url":"","probable_xi":"","discovery_status":provider if any(x in provider for x in ["NO_SEARCH_KEY","ERROR","FAILED","EXCEPTION"]) else "NO_APPROVED_URLS_FOUND","extract_status":"NO_DATA","notes":"No approved source URL discovered or search failed.","auto_apply":"NO","production_change":"NO"})
            continue
        for prov,src,url,title,snippet,expected in urls[:10]:
            try:
                raw_page=http_text(url)
                text=clean_text(raw_page)
                structured=structured_text(raw_page)
            except Exception as e:
                out.append({"target_date":day,"generated_at":ts,"fixture_id":fid,"league":s(fx.get("league")),"country":s(fx.get("country")),"home_team":home,"away_team":away,"team_side":"","source_name":src,"source_url":url,"probable_xi":"","discovery_status":"URL_DISCOVERED","extract_status":"FETCH_FAILED","notes":str(e)[:160],"auto_apply":"NO","production_change":"NO"})
                continue
            relevant, relevance_reason=page_relevance(fx, structured, src)
            if not relevant:
                out.append({"target_date":day,"generated_at":ts,"fixture_id":fid,"league":s(fx.get("league")),"country":s(fx.get("country")),"home_team":home,"away_team":away,"team_side":"","source_name":src,"source_url":url,"probable_xi":"","discovery_status":f"URL_DISCOVERED:{expected}","extract_status":"IRRELEVANT_FIXTURE_PAGE","notes":f"{title[:100]} | relevance={relevance_reason}","auto_apply":"NO","production_change":"NO"})
                continue
            for side,team in [("home",home),("away",away)]:
                xi, method=extract_xi_by_source(raw_page, text, structured, team, src)
                note=(title[:100] + f" | relevance={relevance_reason} | method={method}").strip()
                out.append({"target_date":day,"generated_at":ts,"fixture_id":fid,"league":s(fx.get("league")),"country":s(fx.get("country")),"home_team":home,"away_team":away,"team_side":side,"source_name":src,"source_url":url,"probable_xi":xi,"discovery_status":f"URL_DISCOVERED:{expected}","extract_status":"EXTRACTED" if xi else "NO_XI_PATTERN","notes":note,"auto_apply":"NO","production_change":"NO"})
    return out, provider, urls_seen

def md(day, rows, provider, urls_seen):
    sc=Counter(r["source_name"] for r in rows if r.get("source_name")); st=Counter(r["extract_status"] for r in rows)
    lines=[f"# vSIGMA Autonomous Probable Lineup Collector - {day}","","## Summary",f"- search_provider: {provider}",f"- rows_seen: {len(rows)}",f"- urls_discovered: {urls_seen}",f"- rows_extracted: {sum(1 for r in rows if r.get('extract_status')=='EXTRACTED')}","- status_counts: "+("; ".join(f"{k}={v}" for k,v in st.items()) if st else "none"),"- source_counts: "+("; ".join(f"{k}={v}" for k,v in sc.items()) if sc else "none"),"- max_search_queries_per_fixture: "+os.environ.get("VSIGMA_MAX_PROBABLE_LINEUP_SEARCH_QUERIES", "8"),"- auto_apply: NO","- production_change: NO","","## Guardrails","- Uses only search API keys if configured; no search-page scraping.","- Searches approved probable-XI domains separately and deduplicates URLs.","- Fixture-date relevance filter blocks historical or related articles before extraction.","- SportsMole uses section-aware parsing and does not fall back to narrative regex.","- Source expansion is weighted by registry; new sources are supporting only, never official.","- Search/API/fetch failures degrade to report rows instead of failing workflow.","- Fetches public source URLs only; does not bypass paywalls, logins, or blocks.","- Conservative extraction: blank if pattern confidence is insufficient.","- Output still passes through quarantine and registry-weighted consensus."]
    return "\n".join(lines)+"\n"
def run(day,tz):
    day=date.fromisoformat(day).isoformat(); rows,provider,urls_seen=build(day,tz)
    imported=[r for r in rows if r.get("extract_status")=="EXTRACTED"]
    report=[{"target_date":day,"generated_at":datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"),"fixtures_reviewed":len(fixtures(day)),"search_provider":provider,"urls_discovered":urls_seen,"rows_extracted":len(imported),"status_counts":"; ".join(f"{k}={v}" for k,v in Counter(r['extract_status'] for r in rows).items()),"source_counts":"; ".join(f"{k}={v}" for k,v in Counter(r['source_name'] for r in rows if r.get('source_name')).items()),"auto_apply":"NO","production_change":"NO"}]
    for base in [P/"today"/day, P/"governance"]:
        write(base/"probable_lineup_sources_autonomous.csv", imported, OUT_FIELDS); write(base/"vsigma_autonomous_probable_lineup_collector_report.csv", report, REPORT_FIELDS); (base/"vsigma_autonomous_probable_lineup_collector_report.md").write_text(md(day,rows,provider,urls_seen),encoding="utf-8")
    print("=== VSIGMA AUTONOMOUS PROBABLE LINEUP COLLECTOR ==="); print(f"search_provider={provider}"); print(f"rows_extracted={len(imported)}"); print("auto_apply=NO"); print("production_change=NO")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--date",required=True); p.add_argument("--timezone",default="Atlantic/Canary"); a=p.parse_args(); run(a.date,a.timezone)
if __name__=="__main__": main()
