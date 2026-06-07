"""iRacing .ibt telemetry file reader.

Wraps pyirsdk's IBT class to read an .ibt file and produce a Session object.

pyirsdk is isolated to this module. All other layers receive only
driver_toolkit.models types, not pyirsdk objects.

API note: .ibt files require the irsdk.IBT class, not irsdk.IRSDK.
irsdk.IRSDK uses freeze_var_buffer_latest() for live shared-memory telemetry.
irsdk.IBT provides direct indexed access to recorded file ticks via:
  ibt.open(path)
  ibt.get(tick_index, channel_name)   # single tick, single channel
  ibt.get_all(channel_name)            # all ticks for one channel (preferred)
  ibt.close()

Source: pyirsdk tutorial 02, confirmed from library source.
See docs/Decision_Log.md DEC-002 and docs/Requirements.md A-001.

Validation status: Not yet tested against a real .ibt file.
Session info (car, track) access from the IBT class is unconfirmed —
the IBT class may expose session_info differently from the live IRSDK class.
"""

from pathlib import Path

from driver_toolkit.models import Session, TelemetryPoint
from driver_toolkit.parsing.lap_segmenter import segment_laps

try:
    import irsdk  # type: ignore
    _IRSDK_AVAILABLE = True
except ImportError:
    _IRSDK_AVAILABLE = False

REQUIRED_CHANNELS = [
    "SessionTime",
    "LapDistPct",
    "Speed",
    "Throttle",
    "Brake",
    "Gear",
    "RPM",
    "LapCurrentLapTime",
]

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

    Uses irsdk.IBT for file access — this is the correct class for .ibt files.
    irsdk.IRSDK is the live SDK class and should NOT be used here.

    Args:
        file_path: Path to the .ibt file.

    Returns:
        Session with all laps parsed and segmented.

    Raises:
        ImportError: If pyirsdk is not installed.
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be opened or has no telemetry ticks.
    """
    if not _IRSDK_AVAILABLE:
        raise ImportError(
            "pyirsdk is required to load .ibt files. "
            "Install it with: uv add pyirsdk"
        )

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Telemetry file not found: {path}")

    ibt = irsdk.IBT()
    ibt.open(str(path))

    try:
        all_points = _read_all_ticks(ibt)
        if not all_points:
            raise ValueError(
                f"No telemetry ticks found in file: {path}. "
                "The file may be empty or in an unsupported format."
            )

        car, track = _read_session_info(ibt)
        laps = segment_laps(all_points)

    finally:
        ibt.close()

    return Session(car=car, track=track, laps=laps, source_file=str(path))


def _read_all_ticks(ibt: "irsdk.IBT") -> list[TelemetryPoint]:
    """Read all telemetry ticks from the IBT file using bulk channel reads.

    Uses get_all() to fetch each channel as a complete list, then zips
    channels into TelemetryPoints. This is more efficient than per-tick reads
    and is the pattern demonstrated in pyirsdk documentation.
    """
    channel_data: dict[str, list] = {}
    for channel in REQUIRED_CHANNELS:
        values = ibt.get_all(channel)
        channel_data[channel] = values if values is not None else []

    tick_count = max((len(v) for v in channel_data.values()), default=0)
    if tick_count == 0:
        return []

    def safe(channel: str, i: int) -> float:
        values = channel_data[channel]
        if i < len(values) and values[i] is not None:
            return float(values[i])
        return CHANNEL_DEFAULTS.get(channel, 0.0)

    return [
        TelemetryPoint(
            session_time=safe("SessionTime", i),
            lap_dist_pct=safe("LapDistPct", i),
            speed=safe("Speed", i),
            throttle=safe("Throttle", i),
            brake=safe("Brake", i),
            gear=int(safe("Gear", i)),
            rpm=safe("RPM", i),
            lap_current_lap_time=safe("LapCurrentLapTime", i),
        )
        for i in range(tick_count)
    ]


def _read_session_info(ibt: "irsdk.IBT") -> tuple[str, str]:
    """Attempt to read car and track name from session info.

    Session info access from the IBT class is not fully confirmed from
    documentation. This function attempts common patterns and returns
    empty strings on failure rather than raising.

    Validation required against a real .ibt file (see Requirements A-001).
    """
    car = ""
    track = ""

    try:
        session_info = getattr(ibt, "session_info", None)
        if isinstance(session_info, dict):
            drivers = session_info.get("DriverInfo", {}).get("Drivers", [])
            if drivers:
                car = str(drivers[0].get("CarScreenName", ""))
            track = str(session_info.get("WeekendInfo", {}).get("TrackDisplayName", ""))
    except (AttributeError, KeyError, IndexError, TypeError):
        pass

    return car, track
