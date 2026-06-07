# Decision Log – Antigravity Run 01

| Decision | Context | Options Considered | Selected Option | Rationale | Risk / Tradeoff |
|---|---|---|---|---|---|
| Use `pyirsdk` for parser | Need to parse iRacing `.ibt` binary telemetry files. | 1. Custom binary parser<br>2. `pyirsdk` library<br>3. `itelem` library | `pyirsdk` | Official wrapper, pure Python, allows loading local IBT files offline without iRacing running. | Standard dependency; requires pyirsdk to remain functional and updated. |
| Streamlit + Plotly UI | Product vision requires a coaching-first interface showing ranked opportunities and interactive telemetry overlays. | 1. CLI with markdown output<br>2. Custom desktop GUI (Tkinter/PyQt)<br>3. Streamlit web application | Streamlit + Plotly | Fast to implement, interactive charts for telemetry traces, modern UI layout, easy to run locally. | Requires Python runtime; not a standalone binary. |
