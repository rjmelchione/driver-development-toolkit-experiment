# Product Understanding

## Vision Summary

Driver Development Toolkit is a coaching-first telemetry analysis application for iRacing drivers. Its purpose is not to replace full telemetry viewers, but to turn real telemetry data into ranked, actionable driving improvement opportunities.

The MVP targets iRacing Late Model `.ibt` telemetry files. A driver should be able to load telemetry and quickly understand:

1. Where lap time is being lost.
2. Why the loss is likely occurring.
3. What driving adjustment to try.
4. How to practice that adjustment.
5. What telemetry evidence supports the recommendation.

## Product Positioning

The system should behave like a driver development coach supported by telemetry evidence. Raw telemetry remains available as supporting evidence, but the primary workflow should start with prioritized coaching insights.

## MVP Interpretation

The first implementation milestone should prove the core coaching loop:

- Read an iRacing `.ibt` file.
- Extract completed laps and key telemetry channels.
- Compare driver performance across laps from the same session.
- Detect high-value opportunity areas.
- Produce ranked recommendations with evidence.

## Out of Scope for MVP

- Real-time telemetry.
- Setup optimization.
- Race strategy.
- Crew chief behavior.
- Cloud storage or external telemetry services.
- Team/multiplayer workflows.
