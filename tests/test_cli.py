from driver_development_toolkit.cli import main


def test_demo_cli_can_limit_ranked_opportunities(capsys):
    exit_code = main(["--demo", "--max-opportunities", "2"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "### 1." in output
    assert "### 2." in output
    assert "### 3." not in output


def test_demo_cli_can_exclude_consistency_opportunities(capsys):
    exit_code = main(["--demo", "--no-consistency"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "consistency across valid laps" not in output


def test_cli_can_analyze_synthetic_json_fixture(capsys):
    fixture_path = "tests/fixtures/synthetic_late_model_session.json"

    exit_code = main([fixture_path, "--max-opportunities", "1"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Source type: synthetic_json" in output
    assert "## Analysis Provenance" in output
    assert "Real iRacing .ibt ingestion remains blocked" in output
