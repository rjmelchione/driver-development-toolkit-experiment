from pathlib import Path

import pytest

from driver_development_toolkit.ingestion import IbtTelemetryReader, reader_for_path


def test_reader_for_path_selects_synthetic_json_reader():
    reader = reader_for_path(Path("session.json"))

    assert reader.__class__.__name__ == "SyntheticTelemetryReader"


def test_ibt_reader_reports_validation_boundary():
    with pytest.raises((RuntimeError, NotImplementedError)) as error:
        IbtTelemetryReader().read(Path("session.ibt"))

    assert "representative Late Model" in str(error.value) or "not enabled yet" in str(error.value)
