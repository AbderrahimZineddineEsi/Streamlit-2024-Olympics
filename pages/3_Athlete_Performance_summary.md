# Athlete Performance Page — Component Summary

Below is a concise, per-component summary of `pages/3_👤_Athlete_Performance.py`. Each entry states the page title/section, the UI/visual component used, and which dataframe(s) / source file(s) provide the data.

- **Load Data:** calls `utils.load_data()` to receive `athletes_df`, `medallists_df`, `nocs_df`, and `events_df`. Primary sources are `data/athletes.csv` and `data/medallists.csv`.

- **Sidebar / Filters:** uses `utils.create_sidebar(athletes_df)` to create global filters (continent, country, sport/discipline, gender, age). Filter choices are based on `athletes_df`.

- **Apply Global Filters:** `df_athletes_filtered` and `df_medals_filtered` are built by applying the sidebar filters to `athletes_df` and `medallists_df` respectively. These filtered frames power the page's visualizations.

- **1. Athlete Profile (Profile Card):** interactive selectbox to choose an athlete from `df_athletes_filtered`. Displays athlete details (name, nickname, country, sport(s), coach, height, weight, age, birth date) and a gender-based avatar. Source: `data/athletes.csv`.

- **2. Age Distribution (Violin):** shows age distribution by sport and gender using a Plotly violin plot (`px.violin`) from `df_athletes_filtered`. Includes local multiselect to compare specific sports. Source: `data/athletes.csv`.

- **3. Gender Distribution (Pie Chart):** a Plotly pie chart (`px.pie`) showing counts by `gender` from `df_athletes_filtered`. Source: `data/athletes.csv`.

- **4. Top Athletes by Medal Count (Bar Chart):** ranks athletes by medal counts using `df_medals_filtered` pivoted into medal columns (Gold/Silver/Bronze/Total) and plotted via `px.bar`. Local sort-priority controls are available. Source: `data/medallists.csv`.

**Files referenced:** `pages/3_👤_Athlete_Performance.py`, `utils.py`, and CSVs in `data/` (`athletes.csv`, `medallists.csv`).

Generated on 2025-12-07.
