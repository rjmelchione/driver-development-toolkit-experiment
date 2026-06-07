# Research Log – Antigravity Run 01

| External Library / Project | Description / Link | Evaluated Approach | Decision & Rationale |
|---|---|---|---|
| `pyirsdk` | Python implementation of the iRacing SDK. [github.com/kutu/pyirsdk](https://github.com/kutu/pyirsdk) | Parsing `.ibt` telemetry files offline using `irsdk.IBT`. | **Adopted:** Pure Python wrapper around iRacing SDK structures; doesn't require extra C/C++ compilation. Supports reading telemetry files offline. |
| `itelem` | Python library for `.ibt` files. | Parsing `.ibt` telemetry files. | **Rejected (for now):** Less active and documented than `pyirsdk`, but remains a fallback if native issues occur with pyirsdk's `ctypes` usage on Windows. |
| `Streamlit` | Python web app library. [streamlit.io](https://streamlit.io) | Frontend for visualizing ranked opportunities and telemetry traces. | **Proposed:** Extremely rapid setup, built-in interactive plotting, and modern aesthetic layout. |
| `Plotly` | Interactive plotting library. | Overlapping throttle/brake and speed traces. | **Proposed:** Integrates perfectly with Streamlit and provides hover/zoom features for inspecting telemetry details. |
