"""iRacing .ibt telemetry file reader.

Wraps pyirsdk to read an .ibt file and produce a Session object.

pyirsdk is isolated to this module. All other layers receive only
driver_toolkit.models types, not pyirsdk objects.

Validation status: Not yet tested against a real .ibt file.
See docs/Requirements.md A-001 and docs/Decision_Log.md DEC-002.
"""

from pathlib import Path
from typing import Optional

from driver_toolkit.models import Session, TelemetryPoint
from driver_toolkit.parsing.lap_segmenter import segment_laps

# pyirsdk is an optional runtime dependency — raise a clear error if missing
try:
    import irsdk  # type: ignore
    _IRSDK_AVAILABLE = True
except ImportError:
    _IRSDK_AVAILABLE = False


CHANNEL_DEFAULTS: dict[str, float] = {
    "Speed": 0.0,
    "Throttle": 0.0,
    "Brake": 0.0,
    "Gear": 1,
    "RPM": 0.0,
    "LapDistPct": 0.0,
    "LapCurrentLapTime": 0.0,
    "SessionTime": 0.0,
}


def load_ibt(file_path: str | Path) -> Session:
    """Load an iRacing .ibt telemetry file and return a structured Session.

    Args:
        file_path: Path to the .ibt file.

    Returns:
        Session with all laps parsed and segmented.

    Raises:
        ImportError: If pyirsdk is not installed.
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be opened as a valid .ibt file.
    """
    if not _IRSDK_AVAILABLE:
        raise ImportError(
            "pyirsdk is required to load .ibt files. "
            "Install it with: uv add pyirsdk"
        )

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Telemetry file not found: {path}")

    ir = irsdk.IRSDK()
    if not ir.startup(test_file=str(path)):
        raise ValueError(f"Could not open file as iRacing telemetry: {path}")

    car = _safe_session_str(ir, "DriverInfo", "Drivers", 0, "CarScreenName")
    track = _safe_session_str(ir, "WeekendInfo", "TrackDisplayName")

    all_points = _read_all_ticks(ir)
    laps = segment_laps(all_points)

    ir.shutdown()

    session = Session(car=car, track=track, laps=laps, source_file=str(path))
    return session


def _read_all_ticks(ir: "irsdk.IRSDK") -> list[TelemetryPoint]:
    """Iterate through all ticks in the .ibt file and collect TelemetryPoints."""
    points = []

    while ir.get_session_info() is not None or True:
        # pyirsdk advances by calling ir.freeze_var_buffer_latest()
        # then reading channels. We iterate until freeze returns False.
        if not ir.freeze_var_buffer_latest():
            break

        pt = TelemetryPoint(
            session_time=_read(ir, "SessionTime"),
            lap_dist_pct=_read(ir, "LapDistPct"),
            speed=_read(ir, "Speed"),
            throttle=_read(ir, "Throttle"),
            brake=_read(ir, "Brake"),
            gear=int(_read(ir, "Gear")),
            rpm=_read(ir, "RPM"),
            lap_current_lap_time=_read(ir, "LapCurrentLapTime"),
        )
        points.append(pt)

    return points


def _read(ir: "irsdk.IRSDK", channel: str) -> float:
    """Read a channel value with a safe default if the channel is absent."""
    value = ir[channel]
    if value is None:
        return CHANNEL_DEFAULTS.get(channel, 0.0)
    return float(value)


def _safe_session_str(ir: "irsdk.IRSDK", *keys: str) -> str:
    """Safely navigate nested session info dict. Returns empty string on miss."""
    try:
        node = ir.session_info
        for key in keys[:-1]:
            if isinstance(node, list):
                node = node[int(keys[keys.index(key) + 1])]  # type: ignore
            else:
                node = node[key]
        return str(node.get(keys[-1], "")) if isinstance(node, dict) else ""
    except (KeyError, IndexError, TypeError, AttributeError):
        return ""
