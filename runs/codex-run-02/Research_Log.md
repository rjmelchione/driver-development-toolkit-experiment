# Research Log - Codex Run 02

## Research Question

What existing open-source or proven solutions can read iRacing `.ibt` telemetry files and support a Python/uv MVP?

## Findings

| Candidate | Type | Link | Notes | Initial Decision |
|---|---|---|---|---|
| `libibt` | Python package | https://pypi.org/project/libibt/ | Python library for reading iRacing IBT telemetry files. Uses a Rust core with PyO3 bindings and returns PyArrow tables. Documentation shows `uv add libibt`. | Preferred first parser candidate. Validate installation and API with a real or fixture `.ibt` file. |
| `pyirsdk` | Python library | https://github.com/kutu/pyirsdk | Python implementation of the iRacing SDK, focused on live telemetry data. | Useful later for live telemetry, but MVP excludes real-time telemetry and needs `.ibt` files. |
| `ibt-telemetry` | Node.js library | https://github.com/SkippyZA/ibt-telemetry | Open-source parser for iRacing `.ibt` telemetry files. | Not preferred because it would add a Node runtime to a Python-first project. Useful as fallback/reference. |
| `itelem` | Rust crate | https://github.com/gmartsenkov/itelem | Rust `.ibt` parser based on `ibt-telemetry`. | Not preferred for Python MVP unless `libibt` fails and a Rust bridge becomes necessary. |
| `pitwall` | Rust library | https://docs.rs/pitwall | Rust library for live streaming and IBT replay with a unified API. | Strong future option if the project expands into live telemetry or high-performance streaming. |
| MoTeC/Mu workflow | Existing toolchain | https://simracingsetup.com/support/how-to-use-iracing-telemetry-files/ | Common workflow converts `.ibt` to MoTeC files for viewing. | Not preferred for MVP because it adds external manual conversion and does not directly support coaching automation. |

## Research-Based Assumptions

- `.ibt` files should be parsed directly in the MVP rather than requiring MoTeC conversion.
- A Python-native API around Arrow/Pandas-style tabular data will simplify analysis and testing.
- Open-source parser maturity varies; dependency validation is an early implementation task.

## Follow-Up Research Needed

- Validate `libibt` on this Windows environment.
- Confirm available channels in representative Late Model `.ibt` files.
- Identify whether iRacing lap boundary and track distance channels are reliable enough for MVP segmentation.
