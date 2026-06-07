from pathlib import Path

import pytest

from driver_development_toolkit.ingestion import IbtTelemetryReader, reader_for_path


def test_reader_for_path_selects_synthetic_json_reader():
    reader = reader_for_path(Path("session.json"))

    assert reader.__class__.__name__ == "SyntheticTelemetryReader"


def test_synthetic_json_fixture_loads_normalized_session():
    fixture_path = Path(__file__).parent / "fixtures" / "synthetic_late_model_session.json"
    session = reader_for_path(fixture_path).read(fixture_path)

    assert session.source_type == "synthetic_json"
    assert session.car == "iRacing Late Model"
    assert len(session.laps) == 3
    assert session.laps[1].lap_time_s == 22.0


def test_ibt_reader_reports_validation_boundary():
    with pytest.raises((RuntimeError, NotImplementedError)) as error:
        IbtTelemetryReader().read(Path("session.ibt"))

    assert "representative Late Model" in str(error.value) or "not enabled yet" in str(error.value)
