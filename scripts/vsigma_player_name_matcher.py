from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher

STOP_TOKENS = {
    "de", "del", "de la", "da", "das", "do", "dos", "van", "von", "jr", "junior", "ii", "iii",
}


def strip_accents(text: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(ch)
    )


def normalize_player_name(name: str) -> str:
    text = strip_accents(str(name or "").lower())
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"[._/]+", " ", text)
    text = re.sub(r"[-’'`]+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def name_tokens(name: str) -> list[str]:
    norm = normalize_player_name(name)
    tokens = [t for t in norm.split() if t and t not in STOP_TOKENS]
    return tokens


def strong_tokens(name: str) -> set[str]:
    return {t for t in name_tokens(name) if len(t) >= 4}


def last_token(name: str) -> str:
    tokens = name_tokens(name)
    return tokens[-1] if tokens else ""


def player_match_score(probable: str, official: str) -> float:
    p = normalize_player_name(probable)
    o = normalize_player_name(official)
    if not p or not o:
        return 0.0
    if p == o:
        return 1.0

    pt = name_tokens(probable)
    ot = name_tokens(official)
    if not pt or not ot:
        return 0.0

    pset, oset = set(pt), set(ot)
    p_last, o_last = pt[-1], ot[-1]

    # Single-token projected XI names often use surnames only.
    if len(pt) == 1:
        token = pt[0]
        if token == o_last and len(token) >= 3:
            return 0.96
        if token in oset and len(token) >= 4:
            return 0.88

    # Direct surname match.
    if p_last == o_last and len(p_last) >= 3:
        return 0.94

    shared_strong = strong_tokens(probable) & strong_tokens(official)
    if shared_strong:
        # Higher if all probable strong tokens appear in official name.
        if strong_tokens(probable).issubset(strong_tokens(official)):
            return 0.90
        return 0.82

    # Token subset match, useful for compound names where one part is omitted.
    if pset and pset.issubset(oset):
        return 0.86
    if oset and oset.issubset(pset):
        return 0.80

    # Conservative fuzzy fallback for typos/diacritics.
    ratio = SequenceMatcher(None, p, o).ratio()
    if ratio >= 0.90:
        return 0.78
    return 0.0


def match_players(probable_players: list[str], official_players: list[str], threshold: float = 0.78):
    """Greedy one-to-one match between probable and official player names.

    Returns (matches, missing_official, wrong_probable), where matches are dicts with
    probable, official, and score. This is intentionally conservative: one official
    player can only be matched once.
    """
    probable = [p for p in probable_players if str(p or "").strip()]
    official = [o for o in official_players if str(o or "").strip()]

    pairs = []
    for pi, p in enumerate(probable):
        for oi, o in enumerate(official):
            score = player_match_score(p, o)
            if score >= threshold:
                pairs.append((score, pi, oi, p, o))
    pairs.sort(reverse=True, key=lambda x: x[0])

    used_p = set()
    used_o = set()
    matches = []
    for score, pi, oi, p, o in pairs:
        if pi in used_p or oi in used_o:
            continue
        used_p.add(pi)
        used_o.add(oi)
        matches.append({"probable": p, "official": o, "score": f"{score:.2f}"})

    missing_official = [o for i, o in enumerate(official) if i not in used_o]
    wrong_probable = [p for i, p in enumerate(probable) if i not in used_p]
    return matches, missing_official, wrong_probable


def match_count(probable_players: list[str], official_players: list[str], threshold: float = 0.78) -> int:
    matches, _, _ = match_players(probable_players, official_players, threshold=threshold)
    return len(matches)
