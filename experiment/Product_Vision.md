# Vision

Create a software application that helps drivers improve lap time by analyzing iRacing telemetry and transforming telemetry data into actionable coaching recommendations.

The application should function as a driver development coach rather than a telemetry viewer. While telemetry evidence must always be available, the primary value of the system is identifying performance opportunities, explaining their causes, recommending corrective actions, and suggesting focused practice activities.

The initial implementation will target iRacing Late Model telemetry data and use `.ibt` files as its primary data source.

---

# Problem Statement

Drivers often have access to large amounts of telemetry data but struggle to determine:

- Where they are losing time
- Why performance differences exist
- Which improvements will have the greatest impact
- How to practice specific skills effectively

Existing telemetry tools frequently require the driver to perform much of the analysis themselves.

The goal of this project is to reduce the gap between telemetry data and actionable driver coaching.

---

# Product Goals

The system should:

1. Analyze real iRacing telemetry data.
2. Identify where lap time is being lost.
3. Determine likely causes of performance loss.
4. Estimate the impact of identified opportunities.
5. Recommend specific driving adjustments.
6. Suggest focused practice activities.
7. Present telemetry evidence supporting recommendations.

---

# Analysis Philosophy

The system should generate meaningful coaching insights from a driver's own telemetry whenever possible.

Reference laps from other drivers may enhance analysis but should not be required.

The system should support:

- Self-comparison across laps
- Session-to-session analysis
- Consistency analysis
- Reference lap comparison when available

The system should identify performance opportunities using whatever evidence is available and provide the most useful coaching recommendations possible from the available data.

---

# Coaching Philosophy

The system should answer four questions for every significant performance opportunity:

## Where am I losing time?

Quantify the opportunity.

## Why am I losing time?

Identify the likely cause.

## What should I change?

Provide actionable coaching guidance.

## How should I practice it?

Recommend a focused training activity or drill.

---

# Evidence and Traceability

Recommendations should be traceable to supporting telemetry evidence.

Drivers should be able to understand why a recommendation was generated and what telemetry observations support it.

The system should prioritize explainable coaching recommendations over opaque conclusions whenever practical.

Users should be able to drill into supporting evidence and understand the reasoning behind significant findings.

---

# Output Philosophy

The system should prioritize coaching opportunities by expected lap-time impact.

Example:

1. Turn 3 Brake Release (+0.18s)
2. Turn 7 Throttle Application (+0.11s)
3. Turn 1 Corner Entry (+0.08s)

Drivers should be able to focus on the highest-value improvement while still viewing all identified opportunities.

---

# User Experience

The application should be coaching-first and telemetry-supported.

Users should first see:

- Key findings
- Ranked opportunities
- Recommended actions
- Practice suggestions

Users should then be able to drill down into supporting telemetry evidence.

The primary interface should emphasize understanding and improvement rather than raw data exploration.

---

# Target User

The long-term vision is to support drivers of varying skill levels through adaptive coaching and analysis.

The MVP should focus on experienced drivers who already understand basic telemetry concepts and are seeking help identifying, prioritizing, and addressing performance opportunities.

---

# Engineering Expectations

The system should be understandable and maintainable by a future developer.

The implementation should include sufficient engineering structure, documentation, rationale, and supporting artifacts such that future enhancements can be made without reverse engineering implementation details.

Major assumptions, design decisions, and tradeoffs should be documented.

Maintainability is considered a first-class requirement alongside functional capability.

---

# Initial Scope

## Included

- iRacing `.ibt` telemetry files
- Late Model support
- Lap analysis
- Session analysis
- Opportunity ranking
- Coaching recommendations
- Practice recommendations
- Telemetry evidence

## Excluded

- Real-time telemetry
- Vehicle setup optimization
- Race strategy
- Crew chief functionality
- External telemetry services
- Cloud infrastructure
- Multiplayer or team features

---

# Future Considerations

While not part of the MVP scope, future versions may expand into:

- Additional vehicle classes
- Setup analysis
- Race analysis
- Driver development history and progression
- Session comparison across seasons
- Additional coaching capabilities

The MVP should not optimize exclusively for Late Model support if doing so would unnecessarily limit future extension.

Future expansion should be enabled through thoughtful design rather than premature complexity.

---

# Success Criteria

The project is successful if a driver can load a telemetry file and quickly understand:

1. The largest opportunities for improvement.
2. The likely causes of those opportunities.
3. The driving changes that should be attempted.
4. How to practice those changes effectively.

The driver should also be able to understand the telemetry evidence supporting those recommendations.

The objective of the MVP is not to create the most comprehensive telemetry analysis platform, but to demonstrate that meaningful driver coaching recommendations can be generated from real iRacing telemetry data.

The resulting system should be understandable, maintainable, and extensible by future developers without requiring reverse engineering of the implementation.