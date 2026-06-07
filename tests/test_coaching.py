import pytest
from driver_development_toolkit.parser import SyntheticTelemetryGenerator
from driver_development_toolkit.analyzer import OvalSectorer, TelemetryComparer
from driver_development_toolkit.coaching import CoachingEngine

def test_coaching_late_braking():
    # Setup
    generator = SyntheticTelemetryGenerator(track_length=1000.0, dt=1/60.0)
    session = generator.generate_session()
    
    ref_lap = session.laps[0]      # Lap 1: Ref
    target_lap = session.laps[1]   # Lap 2: Entry Error in Turn 1-2
    
    sectorer = OvalSectorer()
    sectors = sectorer.segment_lap(ref_lap)
    
    comparer = TelemetryComparer(step_meters=1.0)
    comparison = comparer.compare_laps(target_lap, ref_lap, sectors)
    
    # Run Coaching Engine
    engine = CoachingEngine(time_loss_threshold=0.15)
    opportunities = engine.generate_opportunities(comparison)
    
    # Assertions
    assert len(opportunities) >= 1
    
    # Find Turn 1-2 opportunity
    t1_opp = next(o for o in opportunities if o.sector_name == 'Turn 1-2')
    assert t1_opp.rule_type == "entry_braking_late"
    assert "overshot" in t1_opp.diagnosis.lower()
    assert "marker" in t1_opp.drill.lower()
    assert t1_opp.time_lost > 2.0

def test_coaching_exit_throttle_lift():
    # Setup
    generator = SyntheticTelemetryGenerator(track_length=1000.0, dt=1/60.0)
    session = generator.generate_session()
    
    ref_lap = session.laps[0]      # Lap 1: Ref
    target_lap = session.laps[2]   # Lap 3: Exit Error in Turn 3-4
    
    sectorer = OvalSectorer()
    sectors = sectorer.segment_lap(ref_lap)
    
    comparer = TelemetryComparer(step_meters=1.0)
    comparison = comparer.compare_laps(target_lap, ref_lap, sectors)
    
    # Run Coaching Engine
    engine = CoachingEngine(time_loss_threshold=0.10)  # Lower threshold if needed
    opportunities = engine.generate_opportunities(comparison)
    
    # Assertions
    assert len(opportunities) >= 1
    
    # Find Turn 3-4 opportunity
    t2_opp = next(o for o in opportunities if o.sector_name == 'Turn 3-4')
    assert t2_opp.rule_type == "exit_throttle_lift"
    assert "lift" in t2_opp.diagnosis.lower()
    assert "progression" in t2_opp.drill.lower()

def test_coaching_engine_threshold():
    generator = SyntheticTelemetryGenerator(track_length=1000.0, dt=1/60.0)
    session = generator.generate_session()
    ref_lap = session.laps[0]
    target_lap = session.laps[1]
    
    sectorer = OvalSectorer()
    sectors = sectorer.segment_lap(ref_lap)
    
    comparer = TelemetryComparer(step_meters=1.0)
    comparison = comparer.compare_laps(target_lap, ref_lap, sectors)
    
    # Set threshold very high (e.g. 10.0 seconds)
    # The maximum loss is around 3.5s, so no opportunities should be generated
    engine = CoachingEngine(time_loss_threshold=10.0)
    opportunities = engine.generate_opportunities(comparison)
    
    assert len(opportunities) == 0
