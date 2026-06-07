# Coaching Rules Review – Driver Development Toolkit

**Purpose of this document**  
The coaching rules are the core product value of this system. They were written by the development agent from general motorsport knowledge without domain expert input. This document presents every rule for structured review by a qualified iRacing driver or driving coach.

**How to review**  
For each rule, answer the four review questions and record your assessment. Rules that receive a "Needs Revision" or "Reject" assessment will be updated before the experiment closes.

**Review status**: Awaiting domain expert review

---

## How Rules Are Triggered

Before reviewing the rules, it helps to understand what triggers each type:

| Opportunity Type | Trigger Condition |
|---|---|
| **Over-Slowing** | Average corner speed across all laps is ≥ 1.5 m/s (~3.4 mph) below the reference lap at that corner |
| **Late Throttle** | Average throttle application point across all laps is ≥ 1.5% track distance later than the reference lap after the apex |
| **Early Brake** | Average brake application point across all laps is ≥ 1.5% track distance earlier than the reference lap before the apex |
| **General Corner** | Meaningful time loss at a corner without a single dominant signal matching the above |

"Reference lap" is the driver's fastest valid lap in the session. All comparisons are self-comparisons — the driver vs. their own best.

---

## Rule 1: Over-Slowing

**Triggered when**: The driver's average minimum corner speed is more than ~3.4 mph below their reference lap at a specific corner.

**Cause text shown to driver**:
> You are carrying [X] mph less than your best lap through [Corner]. The car is being over-slowed, leaving speed on the table that forces you to re-accelerate from a lower baseline.

**Recommendation shown to driver**:
> Commit to a later, harder initial brake application at [Corner]. Trust the car's grip and carry more entry speed. Use the last 15% of the braking zone as a trail, not a stomp — releasing the brake gradually as you approach the apex lets the car rotate without losing forward momentum.

**Practice drill shown to driver**:
> Dedicated over-slowing drill at [Corner]: On a series of laps, deliberately delay your brake point by one car length each lap until you feel the front push. Then back off one car length — that is your target brake point. Repeat until the new point is consistent.

**Review questions**:
1. Is the cause diagnosis accurate? When a driver consistently carries less speed through a corner than their best lap, is over-slowing the correct primary conclusion, or are there common alternative explanations?
2. Is the recommendation technically correct for Late Model driving? Is "trail braking" appropriate for this car class?
3. Is the practice drill practical and safe in an iRacing context?
4. Overall assessment: **[ ] Accept** / **[ ] Accept with minor edits** / **[ ] Needs revision** / **[ ] Reject**

**Notes**:

---

## Rule 2: Late Throttle

**Triggered when**: The driver's average throttle application point after the apex is more than ~1.5% of track distance later than their reference lap.

**Cause text shown to driver**:
> You are applying throttle later than your best lap after [Corner]. The delay causes a speed recovery deficit on the following straight that compounds into measurable lap time loss.

**Recommendation shown to driver**:
> At [Corner], commit to throttle application at the apex. The key is rotation: get the car pointed straight before the apex so that full throttle is available the moment you unwind the steering. If oversteer prevents early throttle, the issue is corner entry — adjust entry speed or line to allow earlier commitment.

**Practice drill shown to driver**:
> Throttle application drill at [Corner]: Focus exclusively on the moment throttle goes to 100%. Use a reference point (a cone, curb, or mark) and practice reaching full throttle AT that point, not after it. Complete 5 laps with this as your only focus.

**Review questions**:
1. Is "commit to throttle at the apex" the correct instruction for Late Model cars? Does this vary significantly by corner type (hairpin vs. sweeper)?
2. The recommendation mentions oversteer preventing early throttle. Is this the most common cause of late throttle in a Late Model, or is there a more typical root cause?
3. Is "100% throttle at a reference point" a realistic practice target, or is progressive throttle more appropriate for this car class?
4. Overall assessment: **[ ] Accept** / **[ ] Accept with minor edits** / **[ ] Needs revision** / **[ ] Reject**

**Notes**:

---

## Rule 3: Early Brake

**Triggered when**: The driver's average brake application point is more than ~1.5% of track distance earlier than their reference lap before the apex.

**Cause text shown to driver**:
> You are initiating braking earlier than your best lap at [Corner]. Early braking converts straight-line speed to heat before the corner, rather than carrying that speed into the entry.

**Recommendation shown to driver**:
> At [Corner], delay your brake marker by one recognisable reference point. Maintain full throttle longer before committing to the brakes. When you do brake, use firm initial pressure — a shorter, harder braking event preserves more entry speed than a long, gentle scrub.

**Practice drill shown to driver**:
> Brake point drill at [Corner]: Mark your current brake point on the track (note a curb, sign, or seam). On each of 5 laps, delay braking by one additional reference point. Stop when the car cannot make the apex. The last successful point is your target.

**Review questions**:
1. Is the distinction between "over-slowing" and "early brake" meaningful to a Late Model driver? Can these be confused with each other — for example, is it possible to brake early AND carry good corner speed?
2. Is "shorter, harder braking event" the correct guidance for Late Model cars, or does this risk inducing lockup or instability?
3. Is the drill safe and repeatable? Progressively later braking until missing the apex could create consistency problems.
4. Overall assessment: **[ ] Accept** / **[ ] Accept with minor edits** / **[ ] Needs revision** / **[ ] Reject**

**Notes**:

---

## Rule 4: Inconsistent Braking

**Triggered when**: High variance in brake application point across laps at the same corner. *(Note: this type is defined in the system but the detection threshold is not yet tuned. It may not currently trigger in practice.)*

**Cause text shown to driver**:
> Your brake point at [Corner] varies significantly lap to lap. Inconsistent braking produces unpredictable entry speeds that prevent you from committing to a consistent line and throttle application point.

**Recommendation shown to driver**:
> At [Corner], identify and commit to a fixed external reference point for your brake marker. This may be a track feature, marshal post, or painted mark. Use it every lap without variation. Consistency first — optimisation second.

**Practice drill shown to driver**:
> Consistency drill at [Corner]: Complete 10 laps using only a single fixed brake marker. Do not adjust it lap to lap. Review your telemetry afterward; if brake points are within 5 meters of each other, the consistency goal is achieved. Then begin experimenting with the marker position.

**Review questions**:
1. Is "find a fixed external reference point" the primary coaching strategy for inconsistent braking in iRacing? Are there meaningful alternatives (e.g. focusing on feel rather than visual markers)?
2. The drill targets 10 laps with the same marker regardless of outcome. Is this the right structure, or should it adapt based on results?
3. Is "5 meters" a meaningful consistency target for a Late Model? What would be a realistic tolerance at, say, Bristol vs. Lime Rock?
4. Overall assessment: **[ ] Accept** / **[ ] Accept with minor edits** / **[ ] Needs revision** / **[ ] Reject**

**Notes**:

---

## Rule 5: General Corner

**Triggered when**: Meaningful time loss at a corner without a dominant signal (speed deficit below over-slowing threshold, brake/throttle deltas below their thresholds).

**Cause text shown to driver**:
> You are losing approximately [X]s at [Corner] compared to your best lap. The telemetry shows a speed deficit at the corner apex without a single dominant cause.

**Recommendation shown to driver**:
> Review your complete approach to [Corner]. Compare your telemetry trace to your best lap from entry through exit. Focus on: (1) brake point consistency, (2) minimum corner speed, and (3) throttle application point. Address the largest visible delta first.

**Practice drill shown to driver**:
> Focus lap drill at [Corner]: Complete 5 laps concentrating only on this corner. Ignore lap time. Try varying brake point, trail braking length, and throttle point independently. Note which change has the biggest positive effect, then build from there.

**Review questions**:
1. Is "compare the trace yourself and find the biggest delta" useful coaching for an experienced driver, or is it too generic to act on?
2. Should the system decline to give a recommendation when it cannot identify a cause, rather than giving a generic one?
3. Is independent variation of brake point, trail braking, and throttle point a valid experimental protocol for a driver to self-diagnose a corner? Are there dependencies between these that make isolated variation difficult?
4. Overall assessment: **[ ] Accept** / **[ ] Accept with minor edits** / **[ ] Needs revision** / **[ ] Reject**

**Notes**:

---

## Additional Review Questions

Beyond the individual rules, please consider:

**Q1 – Missing opportunity types**  
The system currently detects four types of opportunity. What categories of time loss in a Late Model session are NOT covered by these four types and would be important to add?

**Q2 – Opportunity type overlap**  
Are there situations where the system would correctly detect a problem but classify it under the wrong type? For example, could "over-slowing" and "early brake" be triggered simultaneously and produce conflicting advice?

**Q3 – Self-comparison validity**  
The system compares the driver to their own fastest lap. For what types of improvement would this approach fail to produce useful coaching? (For example: a driver who is consistently slow through all corners in the same way every lap.)

**Q4 – Oval-specific considerations**  
The primary target is iRacing Late Model, which runs primarily on ovals. Do any of these rules apply differently or incorrectly in an oval context compared to a road course? Are there oval-specific coaching priorities that are absent from this list?

**Q5 – Priority ranking**  
The system ranks opportunities by estimated time impact, calculated as `speed_deficit_in_m/s × 0.13 seconds`. Is this a reasonable ranking heuristic, or would you prioritize coaching opportunities by a different criterion (e.g., ease of improvement, technique dependency)?

---

## Review Summary

| Rule | Assessment | Priority for Revision |
|---|---|---|
| Over-Slowing | | |
| Late Throttle | | |
| Early Brake | | |
| Inconsistent Braking | | |
| General Corner | | |

**Overall coaching quality assessment**:

**Rules requiring immediate revision before production use**:

**Missing opportunity types to add**:

**Reviewer**: ___________  
**Review date**: ___________
