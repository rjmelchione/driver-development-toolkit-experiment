import numpy as np
from typing import List, Dict, Any

class CoachingOpportunity:
    """Represents a diagnosed driving error with advice and practice recommendations."""
    def __init__(
        self, 
        sector_name: str, 
        opportunity_name: str, 
        time_lost: float, 
        rule_type: str, 
        diagnosis: str, 
        advice: str, 
        drill: str
    ):
        self.sector_name = sector_name
        self.opportunity_name = opportunity_name  # e.g., "Turn 1-2 Entry Braking (+0.35s)"
        self.time_lost = time_lost
        self.rule_type = rule_type                # e.g., "entry_braking_late"
        self.diagnosis = diagnosis
        self.advice = advice
        self.drill = drill

    def __repr__(self):
        return f"Opportunity: {self.opportunity_name} | Lost: {self.time_lost:.3f}s"

class CoachingEngine:
    """Evaluates comparison telemetry and flags performance opportunities based on heuristics."""
    def __init__(self, time_loss_threshold: float = 0.15):
        self.time_loss_threshold = time_loss_threshold

    def generate_opportunities(self, comparison: Dict[str, Any]) -> List[CoachingOpportunity]:
        opportunities = []
        sectors = comparison['sectors']
        common_dist = comparison['common_dist']
        target_data = comparison['target_data']
        ref_data = comparison['ref_data']
        delta_t = comparison['delta_t']
        
        for sec in sectors:
            # We only evaluate corners (turns) for driving input coaching in the MVP
            if sec['type'] != 'turn':
                continue
                
            time_lost = sec['time_lost']
            
            # If the driver lost significant time, diagnose why
            if time_lost >= self.time_loss_threshold:
                start_d = sec['start_dist']
                end_d = sec['end_dist']
                
                # Find indices in the common grid
                start_idx = np.searchsorted(common_dist, start_d)
                end_idx = min(np.searchsorted(common_dist, end_d), len(common_dist) - 1)
                
                # Extract sector arrays
                sec_dist = common_dist[start_idx:end_idx]
                t_throttle = target_data['Throttle'][start_idx:end_idx]
                t_brake = target_data['Brake'][start_idx:end_idx]
                t_speed = target_data['Speed'][start_idx:end_idx]
                t_steering = target_data['Steering'][start_idx:end_idx]
                
                r_throttle = ref_data['Throttle'][start_idx:end_idx]
                r_brake = ref_data['Brake'][start_idx:end_idx]
                r_speed = ref_data['Speed'][start_idx:end_idx]
                r_steering = ref_data['Steering'][start_idx:end_idx]
                
                # Segment turn into zones: Entry (first 35%), Mid (35%-65%), Exit (last 35%)
                sec_len = end_d - start_d
                entry_cutoff = start_d + 0.35 * sec_len
                exit_cutoff = start_d + 0.65 * sec_len
                
                entry_indices = np.where(sec_dist < entry_cutoff)[0]
                mid_indices = np.where((sec_dist >= entry_cutoff) & (sec_dist < exit_cutoff))[0]
                exit_indices = np.where(sec_dist >= exit_cutoff)[0]
                
                # --- 1. Corner Entry Diagnosis ---
                entry_diagnosed = False
                if len(entry_indices) > 0:
                    # Diagnose late braking (Braking zone can start on the straight before turn_start)
                    # Search window: from 45m before turn start to the entry cutoff
                    search_start_d = max(0.0, start_d - 45.0)
                    search_start_idx = np.searchsorted(common_dist, search_start_d)
                    search_end_idx = np.searchsorted(common_dist, entry_cutoff)
                    
                    t_brake_window = target_data['Brake'][search_start_idx:search_end_idx]
                    r_brake_window = ref_data['Brake'][search_start_idx:search_end_idx]
                    
                    t_active = np.where(t_brake_window > 0.1)[0]
                    r_active = np.where(r_brake_window > 0.1)[0]
                    
                    if len(t_active) > 0 and len(r_active) > 0:
                        t_brake_start_d = common_dist[search_start_idx + t_active[0]]
                        r_brake_start_d = common_dist[search_start_idx + r_active[0]]
                        
                        # Overshot / Late braking
                        t_min_speed = np.min(t_speed)
                        r_min_speed = np.min(r_speed)
                        
                        if (t_brake_start_d - r_brake_start_d) > 5.0 and (r_min_speed - t_min_speed) > 1.0:
                            opportunities.append(CoachingOpportunity(
                                sector_name=sec['name'],
                                opportunity_name=f"{sec['name']} - Braking Entry point (+{time_lost:.2f}s)",
                                time_lost=time_lost,
                                rule_type="entry_braking_late",
                                diagnosis="Overshot the corner entry. You braked too late, causing you to slide past the apex and lose corner speed.",
                                advice="Try braking 5 to 10 meters earlier to stabilize the car on entry and roll more speed through the apex.",
                                drill="Braking Marker Drill: Pick a visual marker on the wall or fence (e.g., a line, cone, or flag) and commit to braking exactly at that point on every lap."
                            ))
                            entry_diagnosed = True
                            
                    # Diagnose slow/abrupt brake release
                    if not entry_diagnosed:
                        # Average brake in the latter half of the entry zone
                        half_entry = len(entry_indices) // 2
                        t_late_brake = np.mean(t_brake[entry_indices[half_entry:]])
                        r_late_brake = np.mean(r_brake[entry_indices[half_entry:]])
                        
                        # If driver holds more brake on turn-in
                        if t_late_brake > 0.25 and r_late_brake < 0.10:
                            opportunities.append(CoachingOpportunity(
                                sector_name=sec['name'],
                                opportunity_name=f"{sec['name']} - Brake Release Profile (+{time_lost:.2f}s)",
                                time_lost=time_lost,
                                rule_type="entry_braking_slow_release",
                                diagnosis="Holding the brake pedal too hard or too long into the corner turn-in. This loads the front tires excessively, causing understeer.",
                                advice="Try releasing the brake pedal more smoothly as you increase your steering input.",
                                drill="Brake Release Drill: Focus on trail braking. Gradually ease off the brake pedal in proportion to turning the steering wheel, aiming for 0% brake exactly at the apex."
                            ))
                            entry_diagnosed = True
                            
                # --- 2. Mid-Corner/Apex Diagnosis ---
                mid_diagnosed = False
                if len(mid_indices) > 0 and not entry_diagnosed:
                    # Diagnose coasting (0% throttle, 0% brake)
                    t_throttle_mid = t_throttle[mid_indices]
                    t_brake_mid = t_brake[mid_indices]
                    r_throttle_mid = r_throttle[mid_indices]
                    
                    # Coasting condition: both inputs near zero
                    coasting_mask = (t_throttle_mid < 0.05) & (t_brake_mid < 0.05)
                    coasting_samples = np.sum(coasting_mask)
                    coasting_time = coasting_samples * (sec_len / len(sec_dist)) * 0.016  # approx time
                    
                    ref_coasting_mask = (r_throttle_mid < 0.05) & (ref_data['Brake'][start_idx:end_idx][mid_indices] < 0.05)
                    ref_coasting_time = np.sum(ref_coasting_mask) * (sec_len / len(sec_dist)) * 0.016
                    
                    if coasting_time > 0.8 and ref_coasting_time < 0.3:
                        opportunities.append(CoachingOpportunity(
                            sector_name=sec['name'],
                            opportunity_name=f"{sec['name']} - Mid-Corner Coasting (+{time_lost:.2f}s)",
                            time_lost=time_lost,
                            rule_type="mid_coasting",
                            diagnosis="Excessive coasting in the middle of the turn. You are waiting too long between releasing the brake and applying the throttle.",
                            advice="Transition more quickly from releasing the brake to picking up the throttle at the apex.",
                            drill="Active Input Drill: Minimize the 'dead time' where you have no pedals applied. Try to begin picking up maintenance throttle (10-20%) as soon as you finish trailing off the brake."
                        ))
                        mid_diagnosed = True
                        
                    # Diagnose unstable steering (sawing the wheel)
                    if not mid_diagnosed:
                        t_steer_std = np.std(t_steering[mid_indices])
                        r_steer_std = np.std(r_steering[mid_indices])
                        
                        if (t_steer_std - r_steer_std) > 8.0:  # jerkiness threshold
                            opportunities.append(CoachingOpportunity(
                                sector_name=sec['name'],
                                opportunity_name=f"{sec['name']} - Mid-Corner Steering Stability (+{time_lost:.2f}s)",
                                time_lost=time_lost,
                                rule_type="mid_steering_saw",
                                diagnosis="Steering input is unstable (sawing at the wheel). Jerkiness upsets the chassis balance and slides the tires.",
                                advice="Try to turn in with a single, smooth motion and hold a steady steering angle through the center of the corner.",
                                drill="Steering Smoothness Drill: Look further ahead through the corner. Visualizing the exit early naturally stabilizes your hands and smooths out steering inputs."
                            ))
                            mid_diagnosed = True
                            
                # --- 3. Corner Exit Diagnosis ---
                # Check exit throttle lift across mid and exit zones
                exit_diagnosed = False
                if not entry_diagnosed and not mid_diagnosed:
                    # Evaluate lifts starting from mid-corner onwards
                    mid_exit_indices = np.where(sec_dist >= entry_cutoff)[0]
                    if len(mid_exit_indices) > 0:
                        t_throttle_me = t_throttle[mid_exit_indices]
                        
                        # Diagnose abrupt throttle/lift (wheelspin)
                        has_lift = False
                        peak_reached = 0.0
                        for val in t_throttle_me:
                            if val > peak_reached:
                                peak_reached = val
                            if peak_reached > 0.5 and val < (peak_reached - 0.3):
                                has_lift = True
                                break
                                
                        if has_lift:
                            opportunities.append(CoachingOpportunity(
                                sector_name=sec['name'],
                                opportunity_name=f"{sec['name']} - Exit Throttle Lift (+{time_lost:.2f}s)",
                                time_lost=time_lost,
                                rule_type="exit_throttle_lift",
                                diagnosis="Abrupt throttle application on exit followed by a lift. Stomping the gas too early spun the rear tires or caused understeer, forcing a correction.",
                                advice="Wait slightly longer for the car to rotate before applying power, then apply it in one progressive, continuous motion.",
                                drill="Throttle Progression Drill: Practice a smooth squeeze (e.g., 20%, 50%, 80%, 100%) as you unwind the steering wheel, ensuring you don't have to lift once you commit."
                            ))
                            exit_diagnosed = True
                            
                    # Diagnose delayed throttle application (only if no lift was diagnosed)
                    if len(exit_indices) > 0 and not exit_diagnosed:
                        t_throttle_exit = t_throttle[exit_indices]
                        r_throttle_exit = r_throttle[exit_indices]
                        
                        # Find distance where throttle reaches 90%
                        t_full_idx = np.where(t_throttle_exit > 0.9)[0]
                        r_full_idx = np.where(r_throttle_exit > 0.9)[0]
                        
                        if len(t_full_idx) > 0 and len(r_full_idx) > 0:
                            t_full_d = sec_dist[exit_indices[t_full_idx[0]]]
                            r_full_d = sec_dist[exit_indices[r_full_idx[0]]]
                            
                            # Target reached full throttle significantly later
                            if (t_full_d - r_full_d) > 8.0:
                                opportunities.append(CoachingOpportunity(
                                    sector_name=sec['name'],
                                    opportunity_name=f"{sec['name']} - Delayed Throttle Application (+{time_lost:.2f}s)",
                                    time_lost=time_lost,
                                    rule_type="exit_throttle_delayed",
                                    diagnosis="Hesitant throttle application on exit. You reached full throttle too late, hurting your top speed down the straight.",
                                    advice="Be more committed to the gas once the car points down the straight. Try to squeeze the throttle a few meters earlier.",
                                    drill="Exit Commit Drill: Focus on getting the car rotated early in the corner so that you can straighten the wheel and commit to full throttle sooner."
                                ))
                                exit_diagnosed = True
                                
            # If time lost is positive but didn't trigger any specific entry/mid/exit rules,
            # or was below the threshold, we don't flag a major opportunity.
            
        # Sort opportunities by time lost descending (most critical first)
        opportunities.sort(key=lambda o: o.time_lost, reverse=True)
        return opportunities
