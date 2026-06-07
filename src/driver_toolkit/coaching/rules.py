"""Rules-based coaching recommendations and practice drills.

Each OpportunityType maps to a structured coaching response answering the four
coaching questions from the product vision:
  1. Where am I losing time?  → Opportunity.corner_label + impact_label (caller provides)
  2. Why am I losing time?    → CoachingResult.cause
  3. What should I change?    → CoachingResult.recommendation
  4. How should I practice?   → CoachingResult.drill

This module is the intended extension point for future LLM-powered coaching.
The interface (get_coaching(Opportunity) → CoachingResult) is stable; the
implementation can be replaced without changing any other layer.
"""

from dataclasses import dataclass

from driver_toolkit.analysis.opportunity_detector import Opportunity, OpportunityType


@dataclass
class CoachingResult:
    """Coaching output for a single opportunity answering the four coaching questions."""

    opportunity: Opportunity
    cause: str              # Why is time being lost?
    recommendation: str     # What should the driver change?
    drill: str              # How should the driver practice it?

    @property
    def corner_label(self) -> str:
        return self.opportunity.corner_label

    @property
    def impact_label(self) -> str:
        return self.opportunity.impact_label

    @property
    def opportunity_type(self) -> OpportunityType:
        return self.opportunity.opportunity_type


def get_coaching(opportunity: Opportunity) -> CoachingResult:
    """Map an Opportunity to a CoachingResult using rule-based logic.

    Args:
        opportunity: A detected performance opportunity with type and telemetry.

    Returns:
        CoachingResult with cause, recommendation, and drill.
    """
    handler = _RULES.get(opportunity.opportunity_type, _rule_general_corner)
    return handler(opportunity)


def _rule_over_slowing(opp: Opportunity) -> CoachingResult:
    speed_mph = abs(opp.speed_delta) * 2.237  # m/s → mph for readability
    return CoachingResult(
        opportunity=opp,
        cause=(
            f"You are carrying {speed_mph:.1f} mph less than your best lap through "
            f"{opp.corner_label}. The car is being over-slowed, leaving speed "
            "on the table that forces you to re-accelerate from a lower baseline."
        ),
        recommendation=(
            f"Commit to a later, harder initial brake application at {opp.corner_label}. "
            "Trust the car's grip and carry more entry speed. Use the last 15% of the "
            "braking zone as a trail, not a stomp — releasing the brake gradually as you "
            "approach the apex lets the car rotate without losing forward momentum."
        ),
        drill=(
            f"Dedicated over-slowing drill at {opp.corner_label}: "
            "On a series of laps, deliberately delay your brake point by one car length "
            "each lap until you feel the front push. Then back off one car length — that "
            "is your target brake point. Repeat until the new point is consistent."
        ),
    )


def _rule_late_throttle(opp: Opportunity) -> CoachingResult:
    return CoachingResult(
        opportunity=opp,
        cause=(
            f"You are applying throttle later than your best lap after "
            f"{opp.corner_label}. The delay causes a speed recovery deficit on "
            "the following straight that compounds into measurable lap time loss."
        ),
        recommendation=(
            f"At {opp.corner_label}, commit to throttle application at the apex. "
            "The key is rotation: get the car pointed straight before the apex so "
            "that full throttle is available the moment you unwind the steering. "
            "If oversteer prevents early throttle, the issue is corner entry — "
            "adjust entry speed or line to allow earlier commitment."
        ),
        drill=(
            f"Throttle application drill at {opp.corner_label}: "
            "Focus exclusively on the moment throttle goes to 100%. Use a reference "
            "point (a cone, curb, or mark) and practice reaching full throttle AT that "
            "point, not after it. Complete 5 laps with this as your only focus."
        ),
    )


def _rule_early_brake(opp: Opportunity) -> CoachingResult:
    return CoachingResult(
        opportunity=opp,
        cause=(
            f"You are initiating braking earlier than your best lap at "
            f"{opp.corner_label}. Early braking converts straight-line speed to "
            "heat before the corner, rather than carrying that speed into the entry."
        ),
        recommendation=(
            f"At {opp.corner_label}, delay your brake marker by one recognisable "
            "reference point. Maintain full throttle longer before committing to the "
            "brakes. When you do brake, use firm initial pressure — a shorter, harder "
            "braking event preserves more entry speed than a long, gentle scrub."
        ),
        drill=(
            f"Brake point drill at {opp.corner_label}: "
            "Mark your current brake point on the track (note a curb, sign, or seam). "
            "On each of 5 laps, delay braking by one additional reference point. Stop "
            "when the car cannot make the apex. The last successful point is your target."
        ),
    )


def _rule_inconsistent_braking(opp: Opportunity) -> CoachingResult:
    return CoachingResult(
        opportunity=opp,
        cause=(
            f"Your brake point at {opp.corner_label} varies significantly lap to lap. "
            "Inconsistent braking produces unpredictable entry speeds that prevent "
            "you from committing to a consistent line and throttle application point."
        ),
        recommendation=(
            f"At {opp.corner_label}, identify and commit to a fixed external reference "
            "point for your brake marker. This may be a track feature, marshal post, or "
            "painted mark. Use it every lap without variation. Consistency first — "
            "optimisation second."
        ),
        drill=(
            f"Consistency drill at {opp.corner_label}: "
            "Complete 10 laps using only a single fixed brake marker. Do not adjust it "
            "lap to lap. Review your telemetry afterward; if brake points are within "
            "5 meters of each other, the consistency goal is achieved. Then begin "
            "experimenting with the marker position."
        ),
    )


def _rule_general_corner(opp: Opportunity) -> CoachingResult:
    return CoachingResult(
        opportunity=opp,
        cause=(
            f"You are losing approximately {opp.impact_label} at {opp.corner_label} "
            "compared to your best lap. The telemetry shows a speed deficit at the "
            "corner apex without a single dominant cause."
        ),
        recommendation=(
            f"Review your complete approach to {opp.corner_label}. Compare your "
            "telemetry trace to your best lap from entry through exit. Focus on: "
            "(1) brake point consistency, (2) minimum corner speed, and "
            "(3) throttle application point. Address the largest visible delta first."
        ),
        drill=(
            f"Focus lap drill at {opp.corner_label}: "
            "Complete 5 laps concentrating only on this corner. Ignore lap time. "
            "Try varying brake point, trail braking length, and throttle point "
            "independently. Note which change has the biggest positive effect, "
            "then build from there."
        ),
    )


_RULES = {
    OpportunityType.OVER_SLOWING: _rule_over_slowing,
    OpportunityType.LATE_THROTTLE: _rule_late_throttle,
    OpportunityType.EARLY_BRAKE: _rule_early_brake,
    OpportunityType.INCONSISTENT_BRAKING: _rule_inconsistent_braking,
    OpportunityType.GENERAL_CORNER: _rule_general_corner,
}
