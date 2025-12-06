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
    page_title="Global Analysis - Paris 2024 Olympics",
    page_icon="🗺️",
    layout="wide"
)

# --- LOAD DATA & SIDEBAR ---
# Load centralized data
athletes_df, medallists_df, nocs_df, events_df = utils.load_data()

# Create Sidebar Filters
filters = utils.create_sidebar(athletes_df)

# --- APPLY GLOBAL FILTERS ---
# We filter the medallists dataset based on sidebar selection
# This creates the 'Main Dataframe' for this page
df_filtered_global = medallists_df[
    (medallists_df['Continent'].isin(filters['continent'])) &
    (medallists_df['country'].isin(filters['country'])) &
    (medallists_df['discipline'].isin(filters['sport'])) &
    (medallists_df['gender'].isin(filters['gender'])) &
    (medallists_df['Age'].between(filters['age'][0], filters['age'][1]))
]

# --- PAGE CONTENT ---
st.title("🗺️ Global Analysis")
st.markdown("### Geographical Medal Distribution Across Countries")

# ==============================================================================
# TASK 1: CHOROPLETH MAP (Dynamic)
# ==============================================================================
st.header("🌍 Medal Distribution by Country")

if not df_filtered_global.empty:
    # 1. Prepare Data for Map
    df_for_map = df_filtered_global.drop_duplicates(subset=['country', 'discipline', 'event', 'medal_type'])
    # We must aggregate the filtered data to get new totals per country
    map_data = df_for_map.groupby('country').size().reset_index(name='Total')
    
    # Calculate breakdown for hover tooltips
    medal_breakdown = df_for_map.pivot_table(
        index='country', columns='medal_type', aggfunc='size', fill_value=0
    ).reset_index()
    
    # Merge Totals with Breakdown
    map_data = map_data.merge(medal_breakdown, on='country', how='left')
    
    # Ensure all columns exist
    for m in ['Gold Medal', 'Silver Medal', 'Bronze Medal']:
        if m not in map_data.columns: map_data[m] = 0

    # Get ISO Codes using Utils
    map_data['iso_alpha'] = map_data['country'].apply(utils.get_iso3_code)

    # 2. Create Map
    fig_choropleth = px.choropleth(
        map_data,
        locations='iso_alpha',
        color='Total',
        hover_name='country',
        hover_data={
            'iso_alpha': False,
            'Total': True,
            'Gold Medal': True,
            'Silver Medal': True,
            'Bronze Medal': True
        },
        color_continuous_scale='YlOrRd',
        labels={'Total': 'Total Medals'},
        title='Global Medal Distribution (Filtered)'
    )

    fig_choropleth.update_layout(
        geo=dict(showframe=True, showcoastlines=True, projection_type='equirectangular'),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(fig_choropleth, use_container_width=True)
else:
    st.warning("No medals found for the current filters.")


# ==============================================================================
# TASK 2: HIERARCHY CHARTS (Sunburst / Treemap / Icicle)
# ==============================================================================
if not df_filtered_global.empty:
    # Prepare Data: Group by Continent -> Country -> Discipline
    df_hierarchy = df_filtered_global.drop_duplicates(subset=['country', 'discipline', 'event', 'medal_type'])
    df_hierarchy = df_hierarchy.groupby(['Continent', 'country', 'discipline']).size().reset_index(name='Medal_Count')

    col_sun, col_tree = st.columns(2)
    
    with col_sun:
        st.subheader("Medal Hierarchy (Sunburst)")
        sunburst_fig = px.sunburst(
            df_hierarchy,
            path=['Continent', 'country', 'discipline'],
            values='Medal_Count',
            title="Continent > Country > Sport"
        )
        st.plotly_chart(sunburst_fig, use_container_width=True)

    with col_tree:
        st.subheader("Medal Hierarchy (Treemap)")
        treemap_fig = px.treemap(
            df_hierarchy,
            path=['Continent', 'country', 'discipline'],
            values='Medal_Count',
            title="Continent > Country > Sport"
        )
        st.plotly_chart(treemap_fig, use_container_width=True)

    # # Icicle Chart (Full Width)
    # st.subheader("Medal Hierarchy (Icicle)")
    # icicle_fig = px.icicle(
    #     df_hierarchy, 
    #     path=['Continent', 'country', 'discipline'], 
    #     values='Medal_Count',
    #     color='Continent',
    #     title="Medal Hierarchy (Icicle Chart)"
    # )
    # icicle_fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), height=500)
    # st.plotly_chart(icicle_fig, use_container_width=True)


# ==============================================================================
# TASK 3: CONTINENT BAR CHART
# ==============================================================================
if not df_filtered_global.empty:
    # Prepare Data
    df_cont_grouped = df_filtered_global.drop_duplicates(subset=['country', 'discipline', 'event', 'medal_type'])
    df_cont_grouped = df_cont_grouped.groupby(['Continent', 'medal_type']).size().reset_index(name='Medal_Count')
    
    # Calculate sorting order (Total medals per continent)
    cont_totals = df_cont_grouped.groupby('Continent')['Medal_Count'].sum().sort_values(ascending=True)
    continent_order = cont_totals.index.tolist()

    continent_bar_fig = px.bar(
        df_cont_grouped,
        x='Medal_Count',
        y='Continent',
        color='medal_type',
        title='<b>Medal Distribution by Continent</b>',
        text='Medal_Count',
        color_discrete_map={
            'Gold Medal': '#FFD700',
            'Silver Medal': '#C0C0C0',
            'Bronze Medal': "#CD7F32" # Updated Bronze hex
        },
        orientation='h',
        category_orders={"Continent": continent_order}
    )

    # Styling from your code
    continent_bar_fig.update_traces(
        textposition='inside',
        texttemplate='<b>%{text}</b>',
        insidetextanchor='middle',
        marker_line_width=0
    )

    continent_bar_fig.update_layout(
        height=500,
        barmode='stack',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14, color="white"),
        title_x=0,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showline=False, tickfont=dict(weight='bold')),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", title=None)
    )

    st.plotly_chart(continent_bar_fig, use_container_width=True)


# ==============================================================================
# TASK 4: TOP 20 COUNTRIES (Interactive)
# ==============================================================================
st.subheader("🏆 Top 20 Countries by Medal Count")

# --- 1. LOCAL FILTER: Checkboxes ---
col1, col2, col3 = st.columns(3)
show_gold = col1.checkbox("🥇 Gold Medal", value=True)
show_silver = col2.checkbox("🥈 Silver Medal", value=True)
show_bronze = col3.checkbox("🥉 Bronze Medal", value=True)

# Build list of selected types
selected_medals_local = []
if show_gold: selected_medals_local.append('Gold Medal')
if show_silver: selected_medals_local.append('Silver Medal')
if show_bronze: selected_medals_local.append('Bronze Medal')

if not selected_medals_local:
    st.warning("⚠️ Please select at least one medal type.")
elif not df_filtered_global.empty:
    # --- 2. APPLY LOCAL FILTER TO THE GLOBALLY FILTERED DATA ---
    df_local = df_filtered_global.drop_duplicates(subset=['country', 'discipline', 'event', 'medal_type'])
    df_local = df_local[df_filtered_global['medal_type'].isin(selected_medals_local)]

    if not df_local.empty:
        # A. Find Top 20 based on current selection
        top_20_countries = df_local['country'].value_counts().head(20).index.tolist()

        # B. Filter data to only Top 20
        df_plot = df_local[df_local['country'].isin(top_20_countries)]
        
        # C. Group for Chart
        df_chart = df_plot.groupby(['country', 'medal_type']).size().reset_index(name='Medal_Count')

        # D. Plot
        fig_top20 = px.bar(
            df_chart,
            x='Medal_Count',
            y='country',
            color='medal_type',
            title=f"Top 20 Countries (Filtered by Selection)",
            text='Medal_Count',
            orientation='h',
            color_discrete_map={
                'Gold Medal': '#FFD700',
                'Silver Medal': '#C0C0C0',
                'Bronze Medal': '#CD7F32'
            },
            # Critical Sorting
            category_orders={
                "country": top_20_countries, 
                "medal_type": ['Gold Medal', 'Silver Medal', 'Bronze Medal']
            }
        )

        # Styling
        fig_top20.update_traces(
            textposition='inside',
            texttemplate='<b>%{text}</b>',
            marker_line_width=0
        )

        fig_top20.update_layout(
            height=700,
            barmode='stack',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14, color="white"),
            title_x=0,
            xaxis=dict(showgrid=False, showticklabels=False, title=""),
            yaxis=dict(showgrid=False, title="", tickfont=dict(size=14)),
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center", title=None)
        )

        st.plotly_chart(fig_top20, use_container_width=True)
    else:
        st.warning("No data matches the Checkbox selection.")
else:
    st.warning("No data matches the Global Sidebar filters.")