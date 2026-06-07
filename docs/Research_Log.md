# Research Log – Driver Development Toolkit

Version: 1.0  
Status: Active

---

## Topic: Python Libraries for iRacing .ibt File Parsing

**Date**: 2026-06-06  
**Researcher**: Agent (Claude Code Run 03)  
**Method**: Web search (WebSearch tool) + library documentation review

### Libraries Evaluated

| Library | Language | Type | .ibt File Support | Maintenance | Decision |
|---|---|---|---|---|---|
| pyirsdk | Python | Live SDK + .ibt | Yes (confirmed) | Active (v1.3.5, Mar 2024) | **Adopted** |
| ibt-telemetry (SkippyZA) | JavaScript/Node.js | .ibt file only | Yes | Unknown | Rejected – wrong language |
| teamjorge/ibt | Go | .ibt file only | Yes | Unknown | Rejected – wrong language |
| itelem (gmartsenkov) | Python (Rust core) | .ibt file only | Yes | Unknown | Considered |
| telemetry-parser | Python (Rust core) | Camera/video only | No | Active | Rejected – wrong domain |
| Custom binary parser | Python | Custom | Yes | N/A | Rejected – unnecessary complexity |

### Selected: pyirsdk

**Package name**: `pyirsdk`  
**PyPI**: `pip install pyirsdk`  
**GitHub**: github.com/kutu/pyirsdk  
**Maintainer**: Lauri Koivunen (kutu)

**Adoption rationale**:
- Confirmed Python support for offline `.ibt` file reading via `ir.startup(test_file='path.ibt')`
- Established library with documented iRacing community usage
- Active maintenance (latest release March 2024)
- Exposes all standard telemetry channels (Speed, Throttle, Brake, Gear, RPM, LapCurrentLapTime, LapDistPct, etc.)
- No benefit to implementing custom binary parsing of an undocumented proprietary format

**Known limitations**:
- Library was primarily designed for live SDK usage; .ibt iteration requires custom lap segmentation logic on top
- `.ibt` format is not officially documented by iRacing; library is based on reverse-engineering
- Lap-by-lap iteration requires monitoring the `LapCurrentLapTime` channel for resets rather than native lap enumeration

**Validation status**: Not yet validated against a real `.ibt` file. Integration testing deferred until real files are available (see A-001 in Requirements.md).

---

## Topic: Existing Open-Source iRacing Coaching / Analysis Tools

**Date**: 2026-06-06  
**Researcher**: Agent (Claude Code Run 03)  
**Method**: Web search

### Tools Reviewed

| Tool | Type | Coaching? | Open Source? | Decision |
|---|---|---|---|---|
| MoTeC i2 Standard | Desktop analysis software | No (manual analysis) | No | Reference only |
| Cosworth Pi Toolbox | Desktop analysis software | No (manual analysis) | No | Reference only |
| iRacing data logger (joshtenorio) | Python telemetry viewer | No | Yes | Reference only |
| Coach Dave Academy guides | Documentation | Manual coaching | N/A | Reference only |

### Conclusion

No existing open-source Python tool providing automated coaching recommendations from `.ibt` data was found. The analysis and coaching layers of this project represent novel functionality. The parsing layer (pyirsdk) reuses an established library per the experiment requirement to prefer existing solutions.

---

## Topic: Streamlit for Coaching Dashboard

**Date**: 2026-06-06  
**Researcher**: Agent (Claude Code Run 03)  
**Method**: Prior knowledge + library documentation

### Evaluation Summary

Streamlit was selected as the UI framework. Alternatives considered:

| Option | Pros | Cons | Decision |
|---|---|---|---|
| Streamlit | Pure Python, easy charts, local browser, fast iteration | Requires browser, limited custom layout | **Selected** |
| CLI (Rich library) | No browser required, simple | Cannot display telemetry overlay charts effectively | Rejected |
| PyQt6 desktop | Native app, no browser | Significant additional complexity, separate UI paradigm | Rejected |
| Dash (Plotly) | Powerful charts, more layout control | More boilerplate, similar browser requirement to Streamlit | Not selected |

**Rationale for Streamlit**: The product vision requires coaching-first display with telemetry overlay charts (speed/throttle/brake traces). Streamlit provides this in pure Python with minimal boilerplate. Coaching-first layout is achievable with Streamlit's column and expander widgets. The local browser requirement is acceptable for a data analysis tool used on a development PC.
