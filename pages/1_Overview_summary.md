# Overview Page — Component Summary

Below is a concise, per-component summary of `pages/1_🏠_Overview.py`. Each entry states the page title/section, the UI/visual component used, and which dataframe(s) / source file(s) provide the data.

- **Load Data:** uses the helper `utils.load_data()` which returns `athletes_df`, `medallists_df`, `nocs_df`, and `events_df`. Data comes from `data/athletes.csv`, `data/medallists.csv`, `data/nocs.csv`, and `data/events.csv` (via `utils.py`).

- **Sidebar / Filters:** uses `utils.create_sidebar(athletes_df)` to build interactive filters (continent, country, sport/discipline, gender, age). Filter inputs are derived from `athletes_df` (from `data/athletes.csv`).

- **Apply Filters:** applies the sidebar selection to `medallists_df` and `athletes_df` to produce `raw_filtered_medals`, `medals_clean`, and `filtered_athletes`. Source data: `data/medallists.csv` and `data/athletes.csv` (via `medallists_df` and `athletes_df`).

- **📊 Key Performance Indicators (KPI Metrics):** displays `st.metric` values for:
  - Total Athletes — computed from `filtered_athletes` (filtered `athletes_df`).
  - Total Countries — unique `country` in `filtered_athletes`.
  - Total Sports — unique `disciplines` in `filtered_athletes`.
  - Total Medals — count of rows in `medals_clean` (filtered `medallists_df`, deduplicated).
  - Total Events — derived from `events_df` (data/events.csv), optionally filtered by sport.

- **🏅 Global Medal Distribution (Pie Chart):** a Plotly pie chart (`px.pie`) built from `medals_clean['medal_type']` counts (Gold/Silver/Bronze). Source: `medallists_df` / `data/medallists.csv`.

- **🏆 Top 10 Countries by Medal Count (Bar Chart):** a horizontal Plotly bar chart (`px.bar`) showing top 10 countries by medal counts taken from `medals_clean['country']` (grouped counts). Source: `medallists_df` / `data/medallists.csv`.

**Files referenced:** `pages/1_🏠_Overview.py`, `utils.py`, and CSVs in the `data/` folder (`athletes.csv`, `medallists.csv`, `nocs.csv`, `events.csv`).

Generated on 2025-12-07.
