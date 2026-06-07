"""Telemetry ingestion boundaries and fixture readers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from driver_development_toolkit.models import Lap, TelemetrySample, TelemetrySession


class TelemetryReader(Protocol):
    """Boundary for loading telemetry from different source formats."""

    def read(self, path: Path) -> TelemetrySession:
        """Read telemetry into the normalized session model."""


class SyntheticTelemetryReader:
    """Read normalized JSON fixtures used until real IBT files are available."""

    def read(self, path: Path) -> TelemetrySession:
        with path.open("r", encoding="utf-8") as fixture:
            payload = json.load(fixture)

        laps = []
        for lap_payload in payload["laps"]:
            samples = tuple(
                TelemetrySample(
                    distance_pct=float(sample["distance_pct"]),
                    speed_mph=float(sample["speed_mph"]),
                    throttle_pct=float(sample["throttle_pct"]),
                    brake_pct=float(sample["brake_pct"]),
                    steering_deg=float(sample.get("steering_deg", 0.0)),
                )
                for sample in lap_payload["samples"]
            )
            laps.append(
                Lap(
                    number=int(lap_payload["number"]),
                    lap_time_s=float(lap_payload["lap_time_s"]),
                    valid=bool(lap_payload.get("valid", True)),
                    samples=samples,
                )
            )

        return TelemetrySession(
            source=str(path),
            car=str(payload.get("car", "Unknown car")),
            track=str(payload.get("track", "Unknown track")),
            laps=tuple(laps),
            source_type="synthetic_json",
        )


class IbtTelemetryReader:
    """Placeholder for future real `.ibt` ingestion through `libibt`."""

    def read(self, path: Path) -> TelemetrySession:
        try:
            import libibt  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "Real .ibt ingestion is not enabled yet. The parser boundary exists, "
                "but this run is proceeding with synthetic fixtures until a "
                "representative Late Model .ibt file is available for validation."
            ) from exc

        raise NotImplementedError(
            "Real .ibt ingestion must be mapped and validated against a representative "
            "Late Model telemetry file before use."
        )


def reader_for_path(path: Path) -> TelemetryReader:
    """Select a telemetry reader for the supplied file path."""

    if path.suffix.lower() == ".json":
        return SyntheticTelemetryReader()
    if path.suffix.lower() == ".ibt":
        return IbtTelemetryReader()
    raise ValueError(f"Unsupported telemetry format: {path.suffix}")
