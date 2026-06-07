"""Built-in synthetic telemetry for demos and tests."""

from __future__ import annotations

from driver_development_toolkit.models import Lap, TelemetrySample, TelemetrySession


def demo_session() -> TelemetrySession:
    """Return a deterministic synthetic session with known coaching opportunities."""

    return TelemetrySession(
        source="built-in synthetic fixture",
        car="iRacing Late Model",
        track="Synthetic short oval",
        source_type="synthetic_builtin",
        laps=(
            Lap(
                number=1,
                lap_time_s=22.4,
                samples=(
                    TelemetrySample(0.05, 91, 20, 45),
                    TelemetrySample(0.15, 88, 35, 30),
                    TelemetrySample(0.30, 86, 55, 10),
                    TelemetrySample(0.40, 93, 68, 0),
                    TelemetrySample(0.55, 90, 25, 44),
                    TelemetrySample(0.65, 87, 40, 25),
                    TelemetrySample(0.80, 85, 52, 8),
                    TelemetrySample(0.90, 92, 70, 0),
                ),
            ),
            Lap(
                number=2,
                lap_time_s=22.0,
                samples=(
                    TelemetrySample(0.05, 94, 24, 38),
                    TelemetrySample(0.15, 91, 39, 24),
                    TelemetrySample(0.30, 90, 68, 4),
                    TelemetrySample(0.40, 97, 80, 0),
                    TelemetrySample(0.55, 93, 28, 39),
                    TelemetrySample(0.65, 90, 44, 20),
                    TelemetrySample(0.80, 89, 65, 3),
                    TelemetrySample(0.90, 96, 82, 0),
                ),
            ),
            Lap(
                number=3,
                lap_time_s=22.8,
                samples=(
                    TelemetrySample(0.05, 90, 18, 52),
                    TelemetrySample(0.15, 86, 30, 36),
                    TelemetrySample(0.30, 84, 50, 12),
                    TelemetrySample(0.40, 90, 62, 0),
                    TelemetrySample(0.55, 89, 20, 48),
                    TelemetrySample(0.65, 85, 35, 28),
                    TelemetrySample(0.80, 82, 48, 10),
                    TelemetrySample(0.90, 89, 66, 0),
                ),
            ),
        ),
    )
