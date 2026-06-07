import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from driver_development_toolkit.parser import Lap

class BaseSectorer(ABC):
    """Abstract base class for lap segmentation engines."""
    @abstractmethod
    def segment_lap(self, lap: Lap) -> List[Dict[str, Any]]:
        """Segments a lap into sectors.
        
        Returns a list of dicts:
            {
                'name': str,          # Sector name (e.g., "Turn 1-2")
                'start_dist': float,  # Start distance in meters
                'end_dist': float,    # End distance in meters
                'type': str           # "turn" or "straight"
            }
        """
        pass

class OvalSectorer(BaseSectorer):
    """Segments an oval track by dynamically detecting turns from lateral acceleration."""
    def __init__(self, lat_accel_threshold: float = 1.5, min_zone_length: float = 30.0, merge_distance: float = 15.0):
        self.lat_accel_threshold = lat_accel_threshold
        self.min_zone_length = min_zone_length
        self.merge_distance = merge_distance

    def segment_lap(self, lap: Lap) -> List[Dict[str, Any]]:
        df = lap.data
        track_length = df['LapDist'].max()
        
        # Smooth LatAccel to avoid noise trigger
        # If there are not enough samples, fallback directly
        if len(df) < 50:
            return self._get_fallback_sectors(track_length)

        # Smooth LatAccel using rolling average
        smoothed_lat_accel = df['LatAccel'].rolling(window=min(30, len(df)//2), center=True).mean().fillna(df['LatAccel'])
        abs_lat = smoothed_lat_accel.abs().values
        dist = df['LapDist'].values
        
        # Find points above threshold
        is_turn = abs_lat > self.lat_accel_threshold
        
        # Identify turn segments
        turns = []
        in_turn = False
        start_d = 0.0
        
        for i in range(len(df)):
            if is_turn[i] and not in_turn:
                in_turn = True
                start_d = dist[i]
            elif not is_turn[i] and in_turn:
                in_turn = False
                end_d = dist[i]
                if end_d - start_d >= self.min_zone_length:
                    turns.append((start_d, end_d))
        
        # If the lap ends while still in a turn
        if in_turn:
            end_d = dist[-1]
            if end_d - start_d >= self.min_zone_length:
                turns.append((start_d, end_d))
                
        # Merge turns that are close together
        merged_turns = []
        if turns:
            current_turn = turns[0]
            for next_turn in turns[1:]:
                # If distance between current turn end and next turn start is small
                if next_turn[0] - current_turn[1] < self.merge_distance:
                    current_turn = (current_turn[0], next_turn[1])
                else:
                    merged_turns.append(current_turn)
                    current_turn = next_turn
            merged_turns.append(current_turn)
            
        # We expect exactly 2 turns for a standard oval (Turn 1-2 and Turn 3-4)
        # If we didn't find exactly 2, we fallback to default proportions
        if len(merged_turns) != 2:
            return self._get_fallback_sectors(track_length)
            
        # Create full list of sectors
        t1_start, t1_end = merged_turns[0]
        t2_start, t2_end = merged_turns[1]
        
        sectors = [
            {
                'name': 'Frontstretch',
                'start_dist': 0.0,
                'end_dist': t1_start,
                'type': 'straight'
            },
            {
                'name': 'Turn 1-2',
                'start_dist': t1_start,
                'end_dist': t1_end,
                'type': 'turn'
            },
            {
                'name': 'Backstretch',
                'start_dist': t1_end,
                'end_dist': t2_start,
                'type': 'straight'
            },
            {
                'name': 'Turn 3-4',
                'start_dist': t2_start,
                'end_dist': t2_end,
                'type': 'turn'
            },
            {
                'name': 'Frontstretch',
                'start_dist': t2_end,
                'end_dist': track_length,
                'type': 'straight'
            }
        ]
        
        # Consolidate split Frontstretch if needed
        # (It starts at end of Turn 4 and wraps around 0m to Turn 1 start)
        return sectors

    def _get_fallback_sectors(self, track_length: float) -> List[Dict[str, Any]]:
        """Fallback split based on standard oval proportions (20-50-70-100%)."""
        return [
            {
                'name': 'Frontstretch',
                'start_dist': 0.0,
                'end_dist': track_length * 0.20,
                'type': 'straight'
            },
            {
                'name': 'Turn 1-2',
                'start_dist': track_length * 0.20,
                'end_dist': track_length * 0.50,
                'type': 'turn'
            },
            {
                'name': 'Backstretch',
                'start_dist': track_length * 0.50,
                'end_dist': track_length * 0.70,
                'type': 'straight'
            },
            {
                'name': 'Turn 3-4',
                'start_dist': track_length * 0.70,
                'end_dist': track_length * 0.95,
                'type': 'turn'
            },
            {
                'name': 'Frontstretch',
                'start_dist': track_length * 0.95,
                'end_dist': track_length,
                'type': 'straight'
            }
        ]


class TelemetryComparer:
    """Compares target lap telemetry to a reference lap using distance-based interpolation."""
    def __init__(self, step_meters: float = 1.0):
        self.step_meters = step_meters

    def compare_laps(self, target_lap: Lap, ref_lap: Lap, sectors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aligns target and reference laps to a common distance grid and computes differences."""
        # Find maximum distance of the track
        max_dist = min(target_lap.data['LapDist'].max(), ref_lap.data['LapDist'].max())
        
        # Define common distance grid
        common_dist = np.arange(0.0, max_dist, self.step_meters)
        
        # Interpolate variables for both laps
        interpolated_target = {}
        interpolated_ref = {}
        
        channels = ['SessionTime', 'Speed', 'Throttle', 'Brake', 'Steering', 'LatAccel', 'LongAccel']
        
        for channel in channels:
            interpolated_target[channel] = np.interp(
                common_dist, 
                target_lap.data['LapDist'].values, 
                target_lap.data[channel].values
            )
            interpolated_ref[channel] = np.interp(
                common_dist, 
                ref_lap.data['LapDist'].values, 
                ref_lap.data[channel].values
            )
            
        # Calculate time-slip (Delta-T)
        # Shift reference SessionTime so both start at 0.0
        target_time_relative = interpolated_target['SessionTime'] - interpolated_target['SessionTime'][0]
        ref_time_relative = interpolated_ref['SessionTime'] - interpolated_ref['SessionTime'][0]
        
        delta_t = target_time_relative - ref_time_relative
        
        # Compute time lost per sector
        sector_results = []
        for sec in sectors:
            start_d = sec['start_dist']
            end_d = sec['end_dist']
            
            # Find indices in common_dist corresponding to start/end distances
            start_idx = np.searchsorted(common_dist, start_d)
            end_idx = min(np.searchsorted(common_dist, end_d), len(common_dist) - 1)
            
            # Time lost in this sector is the change in delta-T from start to end
            t_lost = delta_t[end_idx] - delta_t[start_idx]
            
            sector_results.append({
                'name': sec['name'],
                'start_dist': start_d,
                'end_dist': end_d,
                'type': sec['type'],
                'time_lost': float(t_lost)
            })
            
        return {
            'common_dist': common_dist,
            'delta_t': delta_t,
            'target_data': interpolated_target,
            'ref_data': interpolated_ref,
            'sectors': sector_results
        }
