# Global Analysis Page — Component Summary

Below is a concise, per-component summary of `pages/2_🗺️_Global_Analysis.py`. Each entry states the page title/section, the UI/visual component used, and which dataframe(s) / source file(s) provide the data.

- **Load Data:** uses `utils.load_data()` returning `athletes_df`, `medallists_df`, `nocs_df`, and `events_df`. Source CSVs: `data/athletes.csv`, `data/medallists.csv`, `data/nocs.csv`, `data/events.csv` (via `utils.py`).

- **Sidebar / Filters:** uses `utils.create_sidebar(athletes_df)` to build global filters (continent, country, sport/discipline, gender, age). Filter options are derived from `athletes_df`.

- **Apply Global Filters:** `df_filtered_global` is produced by applying the sidebar selections to `medallists_df`. This filtered medallists dataframe is the main data source for visualizations on this page.

- **🌍 Medal Distribution by Country (Choropleth):** a Plotly choropleth (`px.choropleth`) built from aggregated counts in `df_filtered_global` (deduplicated per country/discipline/event/medal_type). Uses `utils.get_iso3_code()` to map country names to ISO alpha-3 codes. Source: `data/medallists.csv`.

- **Hierarchy Charts (Sunburst / Treemap):** uses grouped `df_filtered_global` aggregated by `Continent -> Country -> Discipline` to build sunburst and treemap charts (`px.sunburst`, `px.treemap`). Source: `data/medallists.csv`.

- **Continent Bar Chart:** stacked horizontal bar chart showing medal counts per continent and medal type, computed from `df_filtered_global` (deduplicated). Source: `data/medallists.csv`.

- **Top 20 Countries (Interactive):** interactive top-20 stacked bar chart driven by `df_filtered_global` with local checkbox filters for medal types (Gold/Silver/Bronze). Source: `data/medallists.csv`.

**Files referenced:** `pages/2_🗺️_Global_Analysis.py`, `utils.py`, and CSVs in `data/` (notably `medallists.csv` and `athletes.csv`).

Generated on 2025-12-07.
