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
