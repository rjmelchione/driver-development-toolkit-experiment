import os
import math
import struct
import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any

# Attempt to import pyirsdk. If it fails, we will support offline synthetic mode.
try:
    import irsdk
    PYIRSDK_AVAILABLE = True
except ImportError:
    PYIRSDK_AVAILABLE = False

class Lap:
    """Represents a single completed lap with its telemetry time series."""
    def __init__(self, lap_number: int, lap_time: float, is_valid: bool, data: pd.DataFrame):
        self.lap_number = lap_number
        self.lap_time = lap_time
        self.is_valid = is_valid
        self.data = data  # Columns: Speed, Throttle, Brake, Steering, LapDist, LapDistPct, LatAccel, LongAccel, SessionTime

    def __repr__(self):
        valid_str = "Valid" if self.is_valid else "Invalid"
        return f"Lap {self.lap_number}: {self.lap_time:.3f}s ({valid_str}, {len(self.data)} samples)"

class TelemetrySession:
    """Represents a complete telemetry logging session."""
    def __init__(self, track_name: str, car_name: str, driver_name: str, laps: List[Lap]):
        self.track_name = track_name
        self.car_name = car_name
        self.driver_name = driver_name
        self.laps = laps

    @property
    def fastest_lap(self) -> Optional[Lap]:
        valid_laps = [lap for lap in self.laps if lap.is_valid]
        if not valid_laps:
            return None
        return min(valid_laps, key=lambda l: l.lap_time)

    def __repr__(self):
        return f"Session - Track: {self.track_name}, Car: {self.car_name}, Laps: {len(self.laps)}"


def parse_ibt_file(file_path: str) -> TelemetrySession:
    """Parses a physical iRacing .ibt file and returns a TelemetrySession.
    
    Raises ImportError if pyirsdk is unavailable.
    """
    if not PYIRSDK_AVAILABLE:
        raise ImportError("pyirsdk is not installed or available in this environment. Cannot parse physical .ibt files.")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Telemetry file not found: {file_path}")

    ibt = irsdk.IBT()
    try:
        ibt.open(file_path)
        
        # Read session YAML info if available
        track_name = "Unknown Track"
        car_name = "Unknown Car"
        driver_name = "Unknown Driver"
        
        if ibt._header and ibt._header.session_info_len > 0:
            try:
                start = ibt._header.session_info_offset
                end = start + ibt._header.session_info_len
                yaml_bytes = ibt._shared_mem[start:end].rstrip(b'\x00')
                translated = yaml_bytes.translate(bytes.maketrans(b'\x81\x8D\x8F\x90\x9D', b'     ')).decode('cp1252', errors='ignore')
                import yaml
                # Safe load with a custom loader that ignores custom iRacing tags
                session_info = yaml.safe_load(translated)
                
                if session_info:
                    weekend_info = session_info.get('WeekendInfo', {})
                    track_name = weekend_info.get('TrackName', track_name)
                    
                    driver_info = session_info.get('DriverInfo', {})
                    driver_car_idx = driver_info.get('DriverCarIdx', -1)
                    drivers = driver_info.get('Drivers', [])
                    if 0 <= driver_car_idx < len(drivers):
                        car_name = drivers[driver_car_idx].get('CarScreenName', car_name)
                        driver_name = drivers[driver_car_idx].get('UserName', driver_name)
            except Exception as e:
                # Log or ignore YAML parsing errors, fallback to defaults
                pass

        # Extract telemetry variables we need
        # Standard names: Speed (m/s), Throttle (0-1), Brake (0-1), SteeringWheelAngle (rad), 
        # LapDist (m), LapDistPct (0-1), Lap (int), LatAccel (m/s^2), LongAccel (m/s^2), SessionTime (s)
        available_vars = ibt.var_headers_names
        
        # Mapping required variables to what is actually available in the file
        var_mapping = {
            'Speed': 'Speed',
            'Throttle': 'Throttle',
            'Brake': 'Brake',
            'Steering': 'SteeringWheelAngle',
            'LapDist': 'LapDist',
            'LapDistPct': 'LapDistPct',
            'Lap': 'Lap',
            'LatAccel': 'LatAccel',
            'LongAccel': 'LongAccel',
            'SessionTime': 'SessionTime'
        }
        
        # Check that we have the minimum set
        for key, default_name in list(var_mapping.items()):
            if default_name not in available_vars:
                # Try case-insensitive search
                match = [v for v in available_vars if v.lower() == default_name.lower()]
                if match:
                    var_mapping[key] = match[0]
                else:
                    raise KeyError(f"Required telemetry channel '{default_name}' is missing from the file.")

        # Read arrays of data
        raw_data = {}
        for key, file_var_name in var_mapping.items():
            raw_data[key] = ibt.get_all(file_var_name)

        df = pd.DataFrame(raw_data)
        
        # Split into laps
        laps = []
        if not df.empty:
            # Group by 'Lap' number
            grouped = df.groupby('Lap')
            for lap_num, group in grouped:
                # Basic validation: Lap should have samples and cover distance
                if len(group) < 100:  # Ignore tiny lap fragments
                    continue
                
                # Check distance range. Completed laps should cross almost the full track.
                dist_min = group['LapDistPct'].min()
                dist_max = group['LapDistPct'].max()
                
                # A lap is complete if it goes from near 0 to near 1
                is_valid = (dist_min < 0.05) and (dist_max > 0.95)
                
                # Determine lap time
                # We can find the exact transition. A simpler approximation is:
                lap_time = group['SessionTime'].max() - group['SessionTime'].min()
                
                # If is_valid is True, let's keep it. Note that out-laps and in-laps will naturally
                # have invalid properties or be partial.
                # In iRacing, LapTime can also be extracted from SessionTime differences at Lap transitions
                # to get millisecond-accurate timing.
                laps.append(Lap(
                    lap_number=int(lap_num),
                    lap_time=float(lap_time),
                    is_valid=is_valid,
                    data=group.copy().reset_index(drop=True)
                ))
                
        return TelemetrySession(track_name, car_name, driver_name, laps)

    finally:
        ibt.close()


class SyntheticTelemetryGenerator:
    """Generates physically consistent synthetic telemetry for testing."""
    def __init__(self, track_length: float = 1000.0, dt: float = 1/60.0):
        self.track_length = track_length
        self.dt = dt

    def _get_steering_profile(self, dist: float) -> float:
        """Determines steering angle (in degrees) based on track distance for a 2-turn oval.
        
        Turns:
          Turn 1-2: 200m to 500m (apex 350m)
          Turn 3-4: 700m to 1000m (apex 850m)
        """
        if 200.0 <= dist < 500.0:
            return 80.0 * math.sin(math.pi * (dist - 200.0) / 300.0)
        elif 700.0 <= dist < 1000.0:
            return 80.0 * math.sin(math.pi * (dist - 700.0) / 300.0)
        return 0.0

    def _run_physics_sim(self, throttle_fn, brake_fn) -> pd.DataFrame:
        """Simulates vehicle dynamics over a single lap using a basic Euler integrator."""
        records = []
        
        # Initial conditions at start/finish line
        v = 40.0        # speed (m/s)
        dist = 0.0      # distance (m)
        time_elapsed = 0.0
        
        # Physics constants
        c_engine = 4.0   # Engine force coefficient
        c_brake = 12.0   # Braking force coefficient
        c_drag = 0.001   # Aerodynamic drag coefficient
        
        # Loop until we complete the lap (dist >= track_length)
        while dist < self.track_length:
            throttle = throttle_fn(dist)
            brake = brake_fn(dist)
            steering = self._get_steering_profile(dist)
            
            # Accelerations
            a_long = c_engine * throttle - c_brake * brake - c_drag * (v ** 2)
            
            # Lateral Gs
            # LatAccel Gs depend on speed and steering angle
            # Peak steering is 80 deg. Let's map 80 deg at 30 m/s to ~1.5 Gs (approx 15 m/s^2)
            a_lat = - (steering / 80.0) * ((v ** 2) / 200.0) * 9.81
            
            # Update states
            v = max(5.0, v + a_long * self.dt)  # Clamp speed to avoid reversing
            dist += v * self.dt
            time_elapsed += self.dt
            
            records.append({
                'SessionTime': time_elapsed,
                'Speed': v,
                'Throttle': throttle,
                'Brake': brake,
                'Steering': steering,
                'LapDist': min(dist, self.track_length),
                'LapDistPct': min(dist, self.track_length) / self.track_length,
                'LatAccel': a_lat,
                'LongAccel': a_long
            })
            
        return pd.DataFrame(records)

    def generate_reference_lap(self, lap_num: int = 1) -> Lap:
        """Generates a perfect, fast reference lap."""
        def throttle_profile(d: float) -> float:
            # Turn 1-2 braking zone
            if 170.0 <= d < 350.0:
                return 0.0
            # Turn 1-2 exit acceleration: reaches 1.0 in 50m
            elif 350.0 <= d < 400.0:
                return (d - 350.0) / 50.0
            # Turn 3-4 braking zone
            elif 670.0 <= d < 850.0:
                return 0.0
            # Turn 3-4 exit acceleration: reaches 1.0 in 50m
            elif 850.0 <= d < 900.0:
                return (d - 850.0) / 50.0
            return 1.0

        def brake_profile(d: float) -> float:
            # Turn 1 entry
            if 170.0 <= d < 320.0:
                # Decays linearly from 0.8 to 0.0
                return 0.8 * (1.0 - (d - 170.0) / 150.0)
            # Turn 3 entry
            elif 670.0 <= d < 820.0:
                return 0.8 * (1.0 - (d - 670.0) / 150.0)
            return 0.0

        df = self._run_physics_sim(throttle_profile, brake_profile)
        # Lap time is the total duration of the simulation
        lap_time = df['SessionTime'].max()
        return Lap(lap_num, lap_time, True, df)

    def generate_entry_error_lap(self, lap_num: int = 2) -> Lap:
        """Generates a lap where the driver brakes too late in Turn 1 and overshoots."""
        def throttle_profile(d: float) -> float:
            # Turn 1-2: late braking shifts throttle zone later
            if 195.0 <= d < 380.0:
                return 0.0
            elif 380.0 <= d < 430.0:
                # Delayed throttle application
                return (d - 380.0) / 50.0
            # Turn 3-4: normal entry (same as reference)
            elif 670.0 <= d < 850.0:
                return 0.0
            elif 850.0 <= d < 900.0:
                return (d - 850.0) / 50.0
            return 1.0

        def brake_profile(d: float) -> float:
            # Turn 1 entry: brakes 25 meters too late (at 195m instead of 170m)
            if 195.0 <= d < 360.0:
                # Heavy braking held longer because they overshot
                return 0.95 * (1.0 - (d - 195.0) / 165.0)
            # Turn 3 entry: normal (same as reference)
            elif 670.0 <= d < 820.0:
                return 0.8 * (1.0 - (d - 670.0) / 150.0)
            return 0.0

        df = self._run_physics_sim(throttle_profile, brake_profile)
        lap_time = df['SessionTime'].max()
        return Lap(lap_num, lap_time, True, df)

    def generate_exit_error_lap(self, lap_num: int = 3) -> Lap:
        """Generates a lap where the driver applies throttle too early, slides, and lifts."""
        def throttle_profile(d: float) -> float:
            # Turn 1-2: normal (same as reference)
            if 170.0 <= d < 350.0:
                return 0.0
            elif 350.0 <= d < 400.0:
                return (d - 350.0) / 50.0
            # Turn 3-4: applies 100% throttle too early (at 830m instead of 850m)
            elif 670.0 <= d < 830.0:
                return 0.0
            elif 830.0 <= d < 850.0:
                return 1.0
            elif 850.0 <= d < 910.0:
                return 0.1
            elif 910.0 <= d < 970.0:
                return 0.1 + 0.9 * (d - 910.0) / 60.0
            return 1.0

        def brake_profile(d: float) -> float:
            # Turn 1 entry: normal
            if 170.0 <= d < 320.0:
                return 0.8 * (1.0 - (d - 170.0) / 150.0)
            # Turn 3 entry: normal
            elif 670.0 <= d < 820.0:
                return 0.8 * (1.0 - (d - 670.0) / 150.0)
            return 0.0

        df = self._run_physics_sim(throttle_profile, brake_profile)
        lap_time = df['SessionTime'].max()
        return Lap(lap_num, lap_time, True, df)

    def generate_session(self) -> TelemetrySession:
        """Generates a mock session with three laps."""
        laps = [
            self.generate_reference_lap(1),
            self.generate_entry_error_lap(2),
            self.generate_exit_error_lap(3)
        ]
        return TelemetrySession(
            track_name="Charlotte Motor Speedway - Oval",
            car_name="Late Model Stock",
            driver_name="AI Development Driver",
            laps=laps
        )
