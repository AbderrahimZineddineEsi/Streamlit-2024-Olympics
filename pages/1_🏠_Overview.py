import streamlit as st
import pandas as pd
import plotly.express as px
import utils # <--- Import your new file

st.set_page_config(page_title="Overview", layout="wide")

# 1. Load Data using utils
athletes_df, medallists_df, nocs_df, events_df = utils.load_data()

# 2. Create Sidebar using utils
filters = utils.create_sidebar(athletes_df)

# 3. Apply Filters using the dictionary returned by utils
raw_filtered_medals = medallists_df[
    (medallists_df['Continent'].isin(filters['continent'])) &
    (medallists_df['country'].isin(filters['country'])) &
    (medallists_df['discipline'].isin(filters['sport'])) &
    (medallists_df['gender'].isin(filters['gender'])) &
    (athletes_df['Age'].between(filters['age'][0], filters['age'][1]))

]
medals_clean = raw_filtered_medals.drop_duplicates(subset=['country', 'discipline', 'event', 'medal_type'])

# A. Filter Athletes DataFrame (For "Total Athletes" KPI)
filtered_athletes = athletes_df[
    (athletes_df['Continent'].isin(filters['continent'])) &
    (athletes_df['country'].isin(filters['country'])) &
    (athletes_df['disciplines'].isin(filters['sport'])) &
    (athletes_df['gender'].isin(filters['gender'])) &
    (athletes_df['Age'].between(filters['age'][0], filters['age'][1]))
]



# --- MAIN PAGE CONTENT ---
st.title("🏅 Paris 2024 Olympic Games - Overview")
st.markdown("### Key Performance Indicators and Medal Standings")

# --- TASK 2: KPI METRICS ---
st.header("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

# Calculate dynamic metrics based on filters
metric_athletes = filtered_athletes.shape[0]
metric_countries = filtered_athletes['country'].nunique() # Countries visible in selection
metric_sports = filtered_athletes['disciplines'].nunique() # Sports visible in selection
metric_medals = medals_clean.shape[0] # Now counts Medals, not Athletes!
metric_events = events_df.shape[0] # Events usually remain static unless linked to sport filter

# Events we filter it only by Sport
if len(filters['sport']) > 0 :
    metric_events = events_df[events_df['sport'].isin(filters['sport'])].shape[0]

with col1: st.metric("Total Athletes", f"{metric_athletes:,}")
with col2: st.metric("Total Countries", metric_countries)
with col3: st.metric("Total Sports", metric_sports)
with col4: st.metric("Total Medals", metric_medals)
with col5: st.metric("Total Events", metric_events)

st.divider()

# --- TASK 3: GLOBAL MEDAL DISTRIBUTION (PIE CHART) ---
st.header("🏅 Global Medal Distribution")

# Aggregate counts from the FILTERED dataframe
medal_counts = medals_clean['medal_type'].value_counts()
# Ensure all types exist even if count is 0
gold_count = medal_counts.get('Gold Medal', 0)
silver_count = medal_counts.get('Silver Medal', 0)
bronze_count = medal_counts.get('Bronze Medal', 0)

if metric_medals > 0:
    pie_medals_types_df = pd.DataFrame({
        "Medal": ['Gold', 'Silver', 'Bronze'],
        "Count": [gold_count, silver_count, bronze_count]
    })

    pie_fig = px.pie(
        pie_medals_types_df,
        values='Count',
        names='Medal',
        title="Distribution of Medals (Based on Selection)",
        color='Medal',
        color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': "#CD7F32"},
        hole=0.4
    )
    pie_fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(pie_fig, use_container_width=True)
else:
    st.info("No medals found for the current filters.")

st.divider()

# --- TASK 4: TOP 10 MEDAL STANDINGS (BAR CHART) ---
st.header("🏆 Top 10 Countries by Medal Count")

if metric_medals > 0:
    # We must recalculate the Top 10 dynamically from the filtered data
    # Group by Country and count rows
    country_medal_counts = medals_clean['country'].value_counts().reset_index()
    country_medal_counts.columns = ['country', 'Total']
    
    # Get Top 10
    top_10 = country_medal_counts.head(10)
    # Sort for the chart (smallest at bottom, largest at top for horizontal bar)
    top_10 = top_10.sort_values('Total', ascending=True)

    bar_fig = px.bar(
        top_10,
        x="Total",
        y='country',
        orientation='h',
        title="Top 10 Countries (Filtered)",
        labels={'Total': 'Total Medals', 'country': 'Country'},
        color='Total',
        color_continuous_scale='Viridis',
        text='Total',
    )
    bar_fig.update_traces(textposition='outside')
    bar_fig.update_layout(showlegend=False, height=500)
    
    st.plotly_chart(bar_fig, use_container_width=True)
else:
    st.info("No data available for rankings.")