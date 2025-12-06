import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils 

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sports & Events Analysis",
    page_icon="🏟️",
    layout="wide"
)

st.title("🏟️ Sports & Events Analysis")

# --- 1. LOAD DATA ---
# Load Global Data via Utils
athletes_df, medallists_df, nocs_df, events_df = utils.load_data()

# Load Schedule Data (Specific to this page)
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, '..', 'data')

file_path = os.path.join(data_dir, 'schedule.csv')
if not os.path.exists(file_path):
    file_path = os.path.join(data_dir, 'schedules.csv')

try:
    schedule_df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("Could not find schedule.csv")
    st.stop()

# Preprocess Schedule
schedule_df['start_date'] = pd.to_datetime(schedule_df['start_date'], errors='coerce')
schedule_df['end_date'] = pd.to_datetime(schedule_df['end_date'], errors='coerce')
schedule_df = schedule_df.dropna(subset=['start_date', 'end_date'])
schedule_df.loc[schedule_df['start_date'] == schedule_df['end_date'], 'end_date'] += pd.Timedelta(minutes=30)
schedule_df['Day'] = schedule_df['start_date'].dt.date

# --- SIDEBAR (GLOBAL FILTERS) ---
filters = utils.create_sidebar(athletes_df)

# ==============================================================================
# TASK 1: EVENT SCHEDULE (Local Filters Only)
# ==============================================================================
st.header("📅 Event Schedule (Gantt Chart)")

col1, col2, col3 = st.columns(3)

# A. Local Sport Filter
all_sports = sorted(schedule_df['discipline'].unique())
sel_sports = col1.multiselect("Filter by Sport", all_sports)
if not sel_sports: sel_sports = all_sports 

# Apply local sport filter
filtered_by_sport = schedule_df[schedule_df['discipline'].isin(sel_sports)]

# B. Local Venue Filter
all_venues = sorted(filtered_by_sport['venue'].dropna().astype(str).unique())
sel_venues = col2.multiselect("Filter by Venue", all_venues)
if not sel_venues: sel_venues = all_venues

# Apply local venue filter
filtered_by_sport_venue = filtered_by_sport[filtered_by_sport['venue'].isin(sel_venues)]

# C. Local Date Filter
unique_dates = sorted(filtered_by_sport_venue['Day'].dropna().unique())
date_options = ["All Dates"] + [d.strftime('%Y-%m-%d') for d in unique_dates]
sel_date_str = col3.selectbox("Filter by Date", date_options)

# Filter Final Data
df_gantt = schedule_df[
    (schedule_df['discipline'].isin(sel_sports)) &
    (schedule_df['venue'].isin(sel_venues))
]

is_zoomed_in = False
if sel_date_str != "All Dates":
    filter_date = pd.to_datetime(sel_date_str).date()
    df_gantt = df_gantt[df_gantt['Day'] == filter_date]
    is_zoomed_in = True

# Plot Task 1
if not df_gantt.empty:
    df_gantt = df_gantt.sort_values('start_date', ascending=False)
    
    # Coloring Logic
    if len(sel_sports) <= 1 and len(sel_venues) > 1:
        color_col = 'venue'
    elif len(sel_venues) <= 1:
        color_col = 'discipline'
    else:
        color_col = 'venue' if len(sel_sports) < len(all_sports) else 'discipline'

    fig_timeline = px.timeline(
        df_gantt,
        x_start="start_date",
        x_end="end_date",
        y=color_col,
        color=color_col,
        hover_data=["discipline", "venue", "event", "start_date", "end_date"],
        title=f"Schedule ({'Hourly View' if is_zoomed_in else 'Daily View'})"
    )

    if is_zoomed_in:
        xaxis_config = dict(title="Time of Day", tickformat="%H:%M", dtick=7200000, gridcolor='rgba(255,255,255,0.1)')
    else:
        xaxis_config = dict(title="Date", tickformat="%d %b", dtick=86400000.0, gridcolor='rgba(255,255,255,0.1)')

    fig_timeline.update_layout(
        xaxis=xaxis_config,
        yaxis=dict(title=""),
        height=600,
        barmode='overlay',
        legend_title=color_col.capitalize(),
        showlegend=True
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.warning("No events found for this combination of filters.")

st.divider()

# ==============================================================================
# TASK 2: MEDAL COUNT BY SPORT (TREEMAP)
# ==============================================================================
st.header("🧱 Medal Count by Sport (Treemap)")

# --- FILTERING LOGIC ---
# Apply Global Filters (Continent, Country, Gender, Age)
# BUT IGNORE 'sport' filter as requested
df_treemap_filtered = medallists_df[
    (medallists_df['Continent'].isin(filters['continent'])) &
    (medallists_df['country'].isin(filters['country'])) &
    # (medallists_df['discipline'].isin(filters['sport'])) &  <-- IGNORED
    (medallists_df['gender'].isin(filters['gender'])) &
    (medallists_df['Age'].between(filters['age'][0], filters['age'][1]))
]

# Local Checkboxes
col1, col2, col3 = st.columns(3)
include_gold = col1.checkbox("🥇 Include Gold Medals", value=True)
include_silver = col2.checkbox("🥈 Include Silver Medals", value=True)
include_bronze = col3.checkbox("🥉 Include Bronze Medals", value=True)

if not df_treemap_filtered.empty:
    # Prepare Data
    df_treemap = df_treemap_filtered.pivot_table(
        index='discipline', 
        columns='medal_type', 
        aggfunc='size', 
        fill_value=0
    ).reset_index()

    # Ensure columns exist
    for medal in ['Gold Medal', 'Silver Medal', 'Bronze Medal']:
        if medal not in df_treemap.columns: df_treemap[medal] = 0

    # Calculate Total based on checkboxes
    df_treemap['Total'] = 0
    if include_gold: df_treemap['Total'] += df_treemap['Gold Medal']
    if include_silver: df_treemap['Total'] += df_treemap['Silver Medal']
    if include_bronze: df_treemap['Total'] += df_treemap['Bronze Medal']

    # Remove zero totals
    df_treemap = df_treemap[df_treemap['Total'] > 0]

    if not df_treemap.empty:
        fig_treemap = px.treemap(
            df_treemap,
            path=['discipline'],
            values='Total',
            hover_data=['Gold Medal', 'Silver Medal', 'Bronze Medal'], 
            title="Total Medals by Sport (Filtered by Demographics)",
            color='Total',
            color_continuous_scale='Viridis'
        )
        fig_treemap.update_traces(textinfo="label+value")
        st.plotly_chart(fig_treemap, use_container_width=True)
    else:
        st.warning("No medals match the current filters.")
else:
    st.warning("No data matches the Global Sidebar filters (Continent/Country/Gender/Age).")

st.divider()

# ==============================================================================
# TASK 3: VENUE MAP
# ==============================================================================
st.header("📍 Olympic Venues Map")

# Use schedule_df which is already loaded
venues_with_locations = schedule_df[['venue', 'location_description']].drop_duplicates()

# City Coordinate Mapping (Your Logic)
city_coordinates = {
    'Paris': {'lat': 48.8566, 'lon': 2.3522},
    'Saint-Etienne': {'lat': 45.4397, 'lon': 4.3872},
    'Lyon': {'lat': 45.7640, 'lon': 4.8357},
    'Marseille': {'lat': 43.2965, 'lon': 5.3698},
    'Bordeaux': {'lat': 44.8378, 'lon': -0.5792},
    'Nantes': {'lat': 47.2184, 'lon': -1.5536},
    'Nice': {'lat': 43.7102, 'lon': 7.2620},
    'Versailles': {'lat': 48.8049, 'lon': 2.1204},
    'Tahiti': {'lat': -17.6509, 'lon': -149.4260},
    'Vaires-sur-Marne': {'lat': 48.8656, 'lon': 2.6361},
    'Saint-Quentin-en-Yvelines': {'lat': 48.7864, 'lon': 2.0350},
    'Chateauroux': {'lat': 46.8109, 'lon': 1.6914},
    'Colombes': {'lat': 48.9220, 'lon': 2.2530}
}

def get_coords_from_location(location_desc):
    if pd.isna(location_desc): return None, None
    for city, coords in city_coordinates.items():
        if city.lower() in location_desc.lower():
            return coords['lat'], coords['lon']
    return city_coordinates['Paris']['lat'], city_coordinates['Paris']['lon']

# Map Coordinates
venues_with_locations['lat'], venues_with_locations['lon'] = zip(*venues_with_locations['location_description'].apply(get_coords_from_location))
venues_map_df = venues_with_locations.dropna(subset=['lat', 'lon'])

# Get Sports per Venue for Tooltip
venue_sports = schedule_df.groupby('venue')['discipline'].apply(lambda x: ', '.join(sorted(set(x)))).reset_index()
venue_sports.columns = ['venue', 'sports_display']

# Merge
venues_map_df = venues_map_df.merge(venue_sports, on='venue', how='left')

# Plot
fig_map = px.scatter_mapbox(
    venues_map_df,
    lat='lat',
    lon='lon',
    hover_name='venue',
    hover_data={'sports_display': True, 'lat': False, 'lon': False},
    zoom=5,
    height=450,
    title='Paris 2024 Olympic Venues',
    color_discrete_sequence=['#FF6B6B']
)
fig_map.update_traces(marker=dict(size=15))
fig_map.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 40, "l": 0, "b": 0})

st.plotly_chart(fig_map, use_container_width=True)
st.info("💡 Hover over markers to see venue names and sports. Zoom in/out to explore the map!")