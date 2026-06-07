import pytest
import pandas as pd
import numpy as np
from driver_development_toolkit.parser import SyntheticTelemetryGenerator, Lap
from driver_development_toolkit.analyzer import OvalSectorer, TelemetryComparer

def test_oval_sectorer_dynamic_detection():
    # Generate mock session
    generator = SyntheticTelemetryGenerator(track_length=1000.0, dt=1/60.0)
    session = generator.generate_session()
    ref_lap = session.laps[0]
    
    sectorer = OvalSectorer()
    sectors = sectorer.segment_lap(ref_lap)
    
    assert len(sectors) == 5
    assert sectors[0]['name'] == 'Frontstretch'
    assert sectors[1]['name'] == 'Turn 1-2'
    assert sectors[2]['name'] == 'Backstretch'
    assert sectors[3]['name'] == 'Turn 3-4'
    assert sectors[4]['name'] == 'Frontstretch'
    
    # Check turn boundaries
    # Turn 1-2 should be approximately 200m to 500m
    assert pytest.approx(sectors[1]['start_dist'], abs=15.0) == 200.0
    assert pytest.approx(sectors[1]['end_dist'], abs=15.0) == 500.0
    
    # Turn 3-4 should be approximately 700m to 1000m
    assert pytest.approx(sectors[3]['start_dist'], abs=15.0) == 700.0
    assert pytest.approx(sectors[3]['end_dist'], abs=15.0) == 1000.0

def test_oval_sectorer_fallback():
    # Test fallback with a very short lap data
    short_df = pd.DataFrame({
        'LapDist': [0.0, 10.0, 20.0],
        'LatAccel': [0.0, 0.0, 0.0]
    })
    dummy_lap = Lap(lap_number=1, lap_time=2.0, is_valid=True, data=short_df)
    
    sectorer = OvalSectorer()
    sectors = sectorer.segment_lap(dummy_lap)
    
    # Falling back to standard ovals proportions
    assert len(sectors) == 5
    assert sectors[1]['start_dist'] == 4.0  # 20% of 20m
    assert sectors[1]['end_dist'] == 10.0  # 50% of 20m

def test_telemetry_comparer():
    generator = SyntheticTelemetryGenerator(track_length=1000.0, dt=1/60.0)
    session = generator.generate_session()
    
    ref_lap = session.laps[0]     # Lap 1: Ref
    error_lap = session.laps[1]   # Lap 2: Entry Error (should be slower)
    
    sectorer = OvalSectorer()
    sectors = sectorer.segment_lap(ref_lap)
    
    comparer = TelemetryComparer(step_meters=1.0)
    comparison = comparer.compare_laps(error_lap, ref_lap, sectors)
    
    # Check results structure
    assert 'common_dist' in comparison
    assert 'delta_t' in comparison
    assert 'target_data' in comparison
    assert 'ref_data' in comparison
    assert 'sectors' in comparison
    
    # Lap 2 is slower than Lap 1, so delta_t at the end should be positive
    delta_t = comparison['delta_t']
    assert delta_t[-1] > 0.0
    
    # Total time difference computed from lap times
    expected_diff = error_lap.lap_time - ref_lap.lap_time
    assert pytest.approx(delta_t[-1], abs=0.2) == expected_diff
    
    # Check sector results
    sector_results = comparison['sectors']
    assert len(sector_results) == 5
    
    # The entry error lap (Lap 2) had a massive mistake in Turn 1-2 entry
    # So the time lost in Turn 1-2 should be strongly positive
    turn_1_result = next(s for s in sector_results if s['name'] == 'Turn 1-2')
    assert turn_1_result['time_lost'] > 2.0  # Large entry time loss
    
    # Lap 2 had a normal Turn 3-4 (no mistake)
    # So the time lost in Turn 3-4 should be close to 0.0
    turn_2_result = next(s for s in sector_results if s['name'] == 'Turn 3-4')
    assert pytest.approx(turn_2_result['time_lost'], abs=0.5) == 0.0
