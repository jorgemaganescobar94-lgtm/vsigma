from scripts.check_automerge_guardrails import evaluate_files


def test_allows_daily_command_center_script() -> None:
    assert evaluate_files(["scripts/build_daily_command_center.py"]) == []


def test_allows_daily_command_center_test_file() -> None:
    assert evaluate_files(["tests/test_daily_command_center.py"]) == []


def test_allows_github_workflow_changes() -> None:
    assert evaluate_files([".github/workflows/vsigma_production.yml"]) == []


def test_blocks_data_processed_changes() -> None:
    failures = evaluate_files(["data/processed/snapshot.csv"])
    assert failures
    assert "data/" in failures[0]


def test_blocks_env_file() -> None:
    failures = evaluate_files([".env"])
    assert failures
    assert ".env" in failures[0]


def test_blocks_score_script() -> None:
    failures = evaluate_files(["scripts/score_matches_v3.py"])
    assert failures
    assert "keyword" in failures[0]


def test_blocks_backtest_script() -> None:
    failures = evaluate_files(["scripts/backtest_vsigma.py"])
    assert failures
    assert "keyword" in failures[0]


def test_blocks_enrich_odds_script() -> None:
    failures = evaluate_files(["scripts/enrich_odds_context_v3.py"])
    assert failures
    assert "keyword" in failures[0]


def test_blocks_unknown_file() -> None:
    failures = evaluate_files(["misc/new_file.txt"])
    assert failures
    assert "allowlist" in failures[0]
