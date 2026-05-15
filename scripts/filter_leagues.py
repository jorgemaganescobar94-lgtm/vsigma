from __future__ import annotations

from pathlib import Path
import re
import unicodedata
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = ROOT / "data" / "raw" / "matches.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_FILTERED = OUTPUT_DIR / "matches_league_filtered.csv"
OUTPUT_REJECTED = OUTPUT_DIR / "matches_league_rejected.csv"
OUTPUT_REPORT = OUTPUT_DIR / "league_filter_report.csv"


COUNTRY_COLUMN_CANDIDATES = [
    "country",
    "league_country",
    "country_name",
    "league_country_name",
]

LEAGUE_COLUMN = "league"


def normalize_text(value: str) -> str:
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))

    # Quitamos guiones para que South-Africa sea south africa
    value = re.sub(r"[^a-z0-9\s\.]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def detect_country_column(df: pd.DataFrame) -> str | None:
    for col in COUNTRY_COLUMN_CANDIDATES:
        if col in df.columns:
            return col
    return None


HARD_REJECT_PATTERNS = [
    # Juveniles / reservas
    r"\bu17\b",
    r"\bu18\b",
    r"\bu19\b",
    r"\bu20\b",
    r"\bu21\b",
    r"\bu23\b",
    r"\byouth\b",
    r"\bjunior\b",
    r"\breserve\b",
    r"\breserves\b",

    # Femenino, de momento fuera
    r"\bwomen\b",
    r"\bfemenino\b",
    r"\bfemenina\b",
    r"\bkvindeliga\b",

    # Amistosos
    r"\bfriendly\b",
    r"\bfriendlies\b",
    r"\bamistoso\b",
    r"\bamistosos\b",
    r"\bclub friendlies\b",

    # Virtual / simulado
    r"\besoccer\b",
    r"\be soccer\b",
    r"\bvirtual\b",
    r"\bsimulated\b",

    # Regional / amateur
    r"\bregional\b",
    r"\bamateur\b",
    r"\bcounty\b",
    r"\bdistrict\b",
    r"\blandesliga\b",
    r"\boberliga\b",
    r"\bregionalliga\b",
    r"\b4\. liga\b",
    r"\b3\. snl\b",

    # Desarrollo
    r"\bmls next pro\b",
    r"\bnext pro\b",
]


EUROPE_TOP_COMPETITIONS = {
    "uefa champions league",
    "champions league",
    "uefa europa league",
    "europa league",
    "uefa conference league",
    "conference league",
    "uefa europa conference league",
}


COUNTRY_LEAGUE_RULES = {
    # Inglaterra
    ("england", "premier league"): ("TIER_1", 1, "england_premier_league"),
    ("england", "championship"): ("TIER_1", 1, "england_championship"),
    ("england", "league one"): ("TIER_2", 2, "england_league_one"),
    ("england", "league two"): ("TIER_2", 2, "england_league_two"),

    # España
    ("spain", "la liga"): ("TIER_1", 1, "spain_la_liga"),
    ("spain", "laliga"): ("TIER_1", 1, "spain_la_liga"),
    ("spain", "segunda division"): ("TIER_1", 1, "spain_segunda"),
    ("spain", "la liga 2"): ("TIER_1", 1, "spain_segunda"),
    ("spain", "laliga2"): ("TIER_1", 1, "spain_segunda"),

    # Italia
    ("italy", "serie a"): ("TIER_1", 1, "italy_serie_a"),
    ("italy", "serie b"): ("TIER_1", 1, "italy_serie_b"),
    ("italy", "serie c"): ("TIER_3", 3, "italy_serie_c_noisy"),

    # Alemania
    ("germany", "bundesliga"): ("TIER_1", 1, "germany_bundesliga"),
    ("germany", "2. bundesliga"): ("TIER_1", 1, "germany_2_bundesliga"),
    ("germany", "3. liga"): ("TIER_3", 3, "germany_3_liga_noisy"),

    # Francia
    ("france", "ligue 1"): ("TIER_1", 1, "france_ligue_1"),
    ("france", "ligue 2"): ("TIER_1", 1, "france_ligue_2"),

    # Países Bajos
    ("netherlands", "eredivisie"): ("TIER_1", 1, "netherlands_eredivisie"),
    ("netherlands", "eerste divisie"): ("TIER_2", 2, "netherlands_eerste_divisie"),

    # Portugal
    ("portugal", "primeira liga"): ("TIER_1", 1, "portugal_primeira_liga"),
    ("portugal", "liga portugal"): ("TIER_1", 1, "portugal_primeira_liga"),
    ("portugal", "liga portugal 2"): ("TIER_2", 2, "portugal_liga_2"),

    # Bélgica
    ("belgium", "jupiler pro league"): ("TIER_1", 1, "belgium_jupiler"),
    ("belgium", "pro league"): ("TIER_1", 1, "belgium_jupiler"),
    ("belgium", "challenger pro league"): ("TIER_3", 3, "belgium_challenger_noisy"),

    # Escocia
    ("scotland", "premiership"): ("TIER_2", 2, "scotland_premiership"),
    ("scotland", "championship"): ("TIER_3", 3, "scotland_championship_noisy"),
    ("scotland", "league one"): ("TIER_3", 3, "scotland_league_one_noisy"),

    # Turquía
    ("turkey", "super lig"): ("TIER_2", 2, "turkey_super_lig"),
    ("turkey", "1. lig"): ("TIER_3", 3, "turkey_1_lig_noisy"),
    ("turkey", "tff 1. lig"): ("TIER_3", 3, "turkey_1_lig_noisy"),

    # Europa media
    ("switzerland", "super league"): ("TIER_2", 2, "switzerland_super_league"),
    ("austria", "bundesliga"): ("TIER_2", 2, "austria_bundesliga"),
    ("denmark", "superliga"): ("TIER_2", 2, "denmark_superliga"),
    ("sweden", "allsvenskan"): ("TIER_2", 2, "sweden_allsvenskan"),
    ("norway", "eliteserien"): ("TIER_2", 2, "norway_eliteserien"),

    # América / Asia razonables
    ("usa", "major league soccer"): ("TIER_2", 2, "usa_mls"),
    ("usa", "mls"): ("TIER_2", 2, "usa_mls"),
    ("united states", "major league soccer"): ("TIER_2", 2, "usa_mls"),
    ("united states", "mls"): ("TIER_2", 2, "usa_mls"),

    ("brazil", "serie a"): ("TIER_2", 2, "brazil_serie_a"),
    ("brazil", "serie b"): ("TIER_3", 3, "brazil_serie_b_noisy"),
    ("brazil", "serie c"): ("TIER_3", 3, "brazil_serie_c_noisy"),

    ("argentina", "primera division"): ("TIER_2", 2, "argentina_primera"),
    ("japan", "j1 league"): ("TIER_2", 2, "japan_j1"),
    ("south korea", "k league 1"): ("TIER_2", 2, "korea_k1"),
    ("korea republic", "k league 1"): ("TIER_2", 2, "korea_k1"),

    # Competiciones continentales
    ("world", "conmebol libertadores"): ("TIER_1", 1, "conmebol_libertadores"),
    ("world", "conmebol sudamericana"): ("TIER_2", 2, "conmebol_sudamericana"),
    ("world", "uefa europa conference league"): ("TIER_2", 2, "uefa_europa_conference_league"),
    ("world", "afc champions league"): ("TIER_2", 2, "afc_champions_league"),
    ("world", "afc champions league two"): ("TIER_3", 3, "afc_champions_league_two_noisy"),
    ("world", "caf champions league"): ("TIER_3", 3, "caf_champions_league_noisy"),

    # Ligas medias aceptables, pero con castigo fuerte
    ("south africa", "premier soccer league"): ("TIER_3", 3, "south_africa_psl_noisy"),
    ("united arab emirates", "pro league"): ("TIER_3", 3, "uae_pro_league_noisy"),
    ("egypt", "premier league"): ("TIER_3", 3, "egypt_premier_league_noisy"),
    ("israel", "liga leumit"): ("TIER_3", 3, "israel_liga_leumit_noisy"),
    ("lithuania", "a lyga"): ("TIER_3", 3, "lithuania_a_lyga_noisy"),
    ("slovakia", "super liga"): ("TIER_3", 3, "slovakia_super_liga_noisy"),
    ("finland", "veikkausliiga"): ("TIER_3", 3, "finland_veikkausliiga_noisy"),

    # Copas nacionales: contexto, no premium directo
    ("canada", "canadian championship"): ("TIER_3", 3, "canada_cup_noisy"),
    ("ecuador", "copa ecuador"): ("TIER_4", 4, "ecuador_cup_context_only"),
}


UNIQUE_LEAGUE_RULES_WITHOUT_COUNTRY = {
    "eredivisie": ("TIER_1", 1, "unique_eredivisie"),
    "uefa champions league": ("TIER_1", 1, "unique_uefa_champions_league"),
    "champions league": ("TIER_1", 1, "unique_champions_league"),
    "uefa europa league": ("TIER_1", 1, "unique_uefa_europa_league"),
    "europa league": ("TIER_1", 1, "unique_europa_league"),
    "uefa conference league": ("TIER_1", 1, "unique_uefa_conference_league"),
    "conference league": ("TIER_1", 1, "unique_conference_league"),
    "j1 league": ("TIER_2", 2, "unique_j1"),
    "k league 1": ("TIER_2", 2, "unique_k1"),
    "allsvenskan": ("TIER_2", 2, "unique_allsvenskan"),
    "eliteserien": ("TIER_2", 2, "unique_eliteserien"),
    "canadian championship": ("TIER_3", 3, "unique_canadian_championship_noisy"),
}


def has_hard_reject_signal(league_norm: str) -> bool:
    return any(re.search(pattern, league_norm) for pattern in HARD_REJECT_PATTERNS)


def classify_league(league: str, country: str | None = None) -> tuple[str, int, str]:
    league_norm = normalize_text(league)
    country_norm = normalize_text(country) if country is not None else ""

    if not league_norm:
        return "REJECT", 99, "league_empty"

    if has_hard_reject_signal(league_norm):
        return "REJECT", 99, "hard_reject_noise_league"

    if league_norm in EUROPE_TOP_COMPETITIONS:
        return "TIER_1", 1, "uefa_top_competition"

    if country_norm:
        key = (country_norm, league_norm)

        if key in COUNTRY_LEAGUE_RULES:
            return COUNTRY_LEAGUE_RULES[key]

        return "REJECT", 99, "country_league_not_allowlisted"

    if league_norm in UNIQUE_LEAGUE_RULES_WITHOUT_COUNTRY:
        return UNIQUE_LEAGUE_RULES_WITHOUT_COUNTRY[league_norm]

    return "REJECT", 99, "generic_or_unknown_league_without_country"


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"No existe el archivo: {INPUT_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    required_columns = {"date", "league", "fixture_id", "home_team", "away_team", "status"}
    missing = required_columns - set(df.columns)

    if missing:
        print("\nColumnas encontradas en matches.csv:")
        print(list(df.columns))
        raise ValueError(f"Faltan columnas obligatorias en matches.csv: {sorted(missing)}")

    country_col = detect_country_column(df)

    if country_col:
        print(f"\nColumna de país detectada: {country_col}")
        classifications = df.apply(
            lambda row: classify_league(row[LEAGUE_COLUMN], row[country_col]),
            axis=1,
        )
    else:
        print("\nAviso: no se detectó columna de país. Se usará filtro ultraestricto por nombre único.")
        classifications = df[LEAGUE_COLUMN].apply(lambda league: classify_league(league, None))

    df["league_tier"] = classifications.apply(lambda x: x[0])
    df["league_tier_rank"] = classifications.apply(lambda x: x[1])
    df["league_filter_reason"] = classifications.apply(lambda x: x[2])

    filtered = df[df["league_tier"] != "REJECT"].copy()
    rejected = df[df["league_tier"] == "REJECT"].copy()

    filtered = filtered.sort_values(
        by=["league_tier_rank", "league", "date", "home_team"],
        ascending=[True, True, True, True],
    )

    rejected = rejected.sort_values(
        by=["league_filter_reason", "league", "date", "home_team"],
        ascending=[True, True, True, True],
    )

    group_cols = ["league", "league_tier", "league_filter_reason"]
    if country_col:
        group_cols = [country_col] + group_cols

    report = (
        df.groupby(group_cols)
        .size()
        .reset_index(name="matches")
        .sort_values(["league_tier", "matches"], ascending=[True, False])
    )

    filtered.to_csv(OUTPUT_FILTERED, index=False)
    rejected.to_csv(OUTPUT_REJECTED, index=False)
    report.to_csv(OUTPUT_REPORT, index=False)

    print("\n=== FILTRO DE LIGAS v3 COMPLETADO ===")
    print(f"Partidos de entrada: {len(df)}")
    print(f"Partidos aceptados: {len(filtered)}")
    print(f"Partidos rechazados: {len(rejected)}")

    print("\nAceptados por tier:")
    if not filtered.empty:
        print(filtered["league_tier"].value_counts().sort_index().to_string())
    else:
        print("Ninguno")

    print("\nRechazados por motivo:")
    if not rejected.empty:
        print(rejected["league_filter_reason"].value_counts().to_string())
    else:
        print("Ninguno")

    print("\nArchivos generados:")
    print(f"- {OUTPUT_FILTERED}")
    print(f"- {OUTPUT_REJECTED}")
    print(f"- {OUTPUT_REPORT}")

    print("\nPrimeros partidos aceptados:")
    if not filtered.empty:
        columns_to_show = [
            "date",
            "country",
            "league",
            "league_tier",
            "fixture_id",
            "home_team",
            "away_team",
            "status",
        ]
        existing_columns = [col for col in columns_to_show if col in filtered.columns]
        print(filtered[existing_columns].head(40).to_string(index=False))
    else:
        print("No hay partidos aceptados.")

    print("\nLigas rechazadas más frecuentes:")
    rejected_summary_cols = ["country", "league", "league_filter_reason"]
    existing_rejected_cols = [col for col in rejected_summary_cols if col in rejected.columns]

    if not rejected.empty:
        rejected_summary = (
            rejected.groupby(existing_rejected_cols)
            .size()
            .reset_index(name="matches")
            .sort_values("matches", ascending=False)
            .head(40)
        )
        print(rejected_summary.to_string(index=False))
    else:
        print("Ninguna")


if __name__ == "__main__":
    main()
