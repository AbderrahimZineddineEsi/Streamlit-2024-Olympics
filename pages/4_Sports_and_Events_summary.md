# Sports & Events Page — Component Summary

Below is a concise, per-component summary of `pages/4_🏟️_Sports_and_Events.py`. Each entry states the page title/section, the UI/visual component used, and which dataframe(s) / source file(s) provide the data.

- **Load Data:** uses `utils.load_data()` to get `athletes_df`, `medallists_df`, `nocs_df`, and `events_df` (from `data/` CSVs). Additionally loads schedule data from `data/schedule.csv` or `data/schedules.csv` into `schedule_df` specifically for this page.

- **Sidebar / Filters:** uses `utils.create_sidebar(athletes_df)` for global demographic filters (continent, country, gender, age). The page also provides local filters (sport, venue, date) which apply only to schedule visualizations.

- **📅 Event Schedule (Gantt / Timeline):** builds a timeline/Gantt chart (`px.timeline`) from `schedule_df` (columns: `start_date`, `end_date`, `discipline`, `venue`, `event`). Local filters: sport, venue, and date. Source: `data/schedule.csv` or `data/schedules.csv`.

- **🧱 Medal Count by Sport (Treemap):** computes medal totals per `discipline` from `medallists_df` after applying global demographic filters (continent, country, gender, age) but intentionally ignoring the global `sport` filter. Local checkboxes control inclusion of Gold/Silver/Bronze. Source: `data/medallists.csv`.

- **📍 Olympic Venues Map (Mapbox Scatter):** extracts `venue` and `location_description` from `schedule_df`, maps locations to coordinates via a city-coordinate lookup, and plots venue markers with hover tooltips listing sports (from `schedule_df`). Source: `data/schedule.csv` / `data/schedules.csv`.

**Files referenced:** `pages/4_🏟️_Sports_and_Events.py`, `utils.py`, and CSVs in `data/` (`schedule.csv` or `schedules.csv`, `medallists.csv`, `athletes.csv`).

Generated on 2025-12-07.
