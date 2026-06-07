import os
import pytest
import pandas as pd
from unittest import mock
from driver_development_toolkit.parser import (
    Lap,
    TelemetrySession,
    SyntheticTelemetryGenerator,
    parse_ibt_file
)

def test_lap_properties():
    # Create dummy DataFrame
    df = pd.DataFrame({
        'SessionTime': [0.0, 1.0],
        'Speed': [30.0, 31.0],
        'Throttle': [1.0, 1.0],
        'Brake': [0.0, 0.0],
        'Steering': [0.0, 0.0],
        'LapDist': [0.0, 30.0],
        'LapDistPct': [0.0, 0.03],
        'LatAccel': [0.0, 0.0],
        'LongAccel': [1.0, 1.0]
    })
    
    lap = Lap(lap_number=1, lap_time=1.0, is_valid=True, data=df)
    assert lap.lap_number == 1
    assert lap.lap_time == 1.0
    assert lap.is_valid is True
    assert len(lap.data) == 2
    assert "Lap 1" in repr(lap)
    assert "Valid" in repr(lap)

def test_telemetry_session():
    # Create two laps
    df1 = pd.DataFrame({'SessionTime': [0.0, 1.0], 'Speed': [30.0, 31.0]})
    lap1 = Lap(lap_number=1, lap_time=23.5, is_valid=True, data=df1)
    
    df2 = pd.DataFrame({'SessionTime': [0.0, 1.0], 'Speed': [30.0, 31.0]})
    lap2 = Lap(lap_number=2, lap_time=24.2, is_valid=True, data=df2)
    
    df3 = pd.DataFrame({'SessionTime': [0.0, 1.0], 'Speed': [30.0, 31.0]})
    lap3 = Lap(lap_number=3, lap_time=20.0, is_valid=False, data=df3) # Slower but invalid
    
    session = TelemetrySession("Test Track", "Test Car", "Test Driver", [lap1, lap2, lap3])
    
    assert session.track_name == "Test Track"
    assert session.car_name == "Test Car"
    assert session.driver_name == "Test Driver"
    assert len(session.laps) == 3
    
    # Fastest lap should be lap 1 (23.5s), since lap 3 (20.0s) is invalid
    assert session.fastest_lap == lap1
    assert "Session - Track: Test Track" in repr(session)

def test_synthetic_telemetry_generation():
    generator = SyntheticTelemetryGenerator(track_length=1000.0, dt=1/60.0)
    session = generator.generate_session()
    
    assert session.track_name == "Charlotte Motor Speedway - Oval"
    assert session.car_name == "Late Model Stock"
    assert session.driver_name == "AI Development Driver"
    assert len(session.laps) == 3
    
    # Verify lap objects
    for i, lap in enumerate(session.laps):
        assert lap.lap_number == i + 1
        assert lap.is_valid is True
        assert not lap.data.empty
        
        # Verify required columns exist
        required_cols = {'SessionTime', 'Speed', 'Throttle', 'Brake', 'Steering', 'LapDist', 'LapDistPct', 'LatAccel', 'LongAccel'}
        assert required_cols.issubset(lap.data.columns)
        
        # Verify physics bounds
        assert lap.data['Throttle'].min() >= 0.0
        assert lap.data['Throttle'].max() <= 1.0
        assert lap.data['Brake'].min() >= 0.0
        assert lap.data['Brake'].max() <= 1.0
        assert lap.data['LapDistPct'].min() >= 0.0
        assert lap.data['LapDistPct'].max() <= 1.0
        assert lap.data['LapDist'].max() == 1000.0
        
    # Check that Reference lap (Lap 1) is the fastest
    assert session.fastest_lap.lap_number == 1
    # Check that Lap 2 (Entry error) is slower than reference
    assert session.laps[1].lap_time > session.laps[0].lap_time
    # Check that Lap 3 (Exit error) is slower than reference
    assert session.laps[2].lap_time > session.laps[0].lap_time

def test_parse_ibt_file_no_pyirsdk():
    with mock.patch('driver_development_toolkit.parser.PYIRSDK_AVAILABLE', False):
        with pytest.raises(ImportError) as exc_info:
            parse_ibt_file("dummy.ibt")
        assert "pyirsdk is not installed" in str(exc_info.value)

def test_parse_ibt_file_missing_file():
    with mock.patch('driver_development_toolkit.parser.PYIRSDK_AVAILABLE', True):
        with pytest.raises(FileNotFoundError) as exc_info:
            parse_ibt_file("nonexistent_file_xyz.ibt")
        assert "Telemetry file not found" in str(exc_info.value)
