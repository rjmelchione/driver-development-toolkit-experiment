# Driver Development Toolkit

Analyzes iRacing telemetry files and generates prioritized, evidence-backed coaching recommendations to help drivers improve lap time.

## What It Does

Load an iRacing `.ibt` telemetry file and receive:
- Ranked coaching opportunities by lap time impact
- The likely cause of each time loss
- A specific driving adjustment to attempt
- A focused practice drill
- Supporting telemetry evidence (speed, throttle, brake overlays)

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Windows 10/11

### Installation

```bash
git clone <repository-url>
cd driver-development-toolkit-experiment
uv sync
```

### Run the Application

```bash
uv run streamlit run src/driver_toolkit/ui/app.py
```

Opens in your browser. Select **Use Demo Session** to see coaching output without a real `.ibt` file, or upload your own file.

### Run Tests

```bash
uv run pytest
uv run pytest --cov --cov-report=term-missing  # with coverage
```

## Project Structure

```
src/driver_toolkit/
  models/          ← data types (Session, Lap, TelemetryPoint)
  parsing/         ← .ibt file reading and lap segmentation
  analysis/        ← opportunity detection and quantification
  coaching/        ← coaching recommendations and practice drills
  ui/              ← Streamlit coaching dashboard

docs/              ← engineering artifacts
tests/             ← automated tests (pytest)
runs/claude-run-03/ ← experiment evidence collection
experiment/        ← experiment plan and product vision (read-only)
```

## Engineering Documentation

- [Requirements](docs/Requirements.md)
- [Architecture](docs/Architecture.md)
- [Use Cases](docs/Use_Cases.md)
- [Decision Log](docs/Decision_Log.md)
- [Research Log](docs/Research_Log.md)
- [Test Strategy](docs/Test_Strategy.md)
- [Maintainer Handoff](docs/Maintainer_Handoff.md)

## Experiment Context

This project was built as part of an agentic software development experiment. See [experiment/](experiment/) for the experiment plan and product vision.