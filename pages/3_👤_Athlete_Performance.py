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
    page_title="Athlete Performance - Paris 2024 Olympics",
    page_icon="👤",
    layout="wide"
)

# --- LOAD DATA & SIDEBAR ---
athletes_df, medallists_df, nocs_df, events_df = utils.load_data()
filters = utils.create_sidebar(athletes_df)

# --- APPLY GLOBAL FILTERS ---

# 1. Filter Athletes DataFrame
df_athletes_filtered = athletes_df[
    (athletes_df['Continent'].isin(filters['continent'])) &
    (athletes_df['country'].isin(filters['country'])) &
    (athletes_df['disciplines'].isin(filters['sport'])) &
    (athletes_df['gender'].isin(filters['gender'])) &
    (athletes_df['Age'].between(filters['age'][0], filters['age'][1]))
]

# 2. Filter Medallists DataFrame (Now supports Age filtering via utils merge!)
df_medals_filtered = medallists_df[
    (medallists_df['Continent'].isin(filters['continent'])) &
    (medallists_df['country'].isin(filters['country'])) &
    (medallists_df['discipline'].isin(filters['sport'])) &
    (medallists_df['gender'].isin(filters['gender'])) &
    (medallists_df['Age'].between(filters['age'][0], filters['age'][1]))
]

st.title("👤 Athlete Performance")

# ==============================================================================
# TASK 1: ATHLETE PROFILE CARD
# ==============================================================================
st.header("1. Athlete Profile")

if not df_athletes_filtered.empty:
    # Search box only shows athletes from the filtered dataset
    name_list = sorted(df_athletes_filtered['name'].unique())
    selected_name = st.selectbox("🔎 Search for an athlete (in filtered list):", name_list)

    if selected_name:
        athlete = df_athletes_filtered[df_athletes_filtered['name'] == selected_name].iloc[0]

        col1, col2 = st.columns([1,3])

        with col1 :
            # Gender-based Avatar Logic
            gender = athlete.get('gender', 'Unknown')
            if gender in ['Female', 'W']:
                img_url = "https://cdn-icons-png.flaticon.com/512/4140/4140047.png"
            elif gender in ['Male', 'M']:
                img_url = "https://cdn-icons-png.flaticon.com/512/4140/4140037.png"
            else:
                img_url = "https://cdn-icons-png.flaticon.com/512/1077/1077114.png"
            
            st.image(img_url, width=150)
            
        with col2 : 
            st.title(athlete['name'])
            
            if 'nickname' in athlete and pd.notna(athlete['nickname']) :
                st.caption(f"**Also known as:** {athlete['nickname']}")
                
            height = f"{athlete['height']} cm" if pd.notna(athlete['height']) and athlete['height'] != 0 else "N/A"
            weight = f"{athlete['weight']} kg" if pd.notna(athlete['weight']) and athlete['weight'] != 0 else "N/A"
            
            # Format disciplines
            disciplines_str = str(athlete['disciplines']).replace("[", "").replace("]", "").replace("'", "")
            
            # Format coach
            if pd.notna(athlete['coach']):
                coach_str = str(athlete['coach']).replace("[", "").replace("]", "").replace("'", "")
            else:
                coach_str = 'N/A'
            
            st.markdown(f"""
            **📍 Country:** {athlete['country']}
            **🏃 Sport:** {disciplines_str}
            **🧑‍🏫 Coach:** {coach_str}
            **📏 Height:** {height}  &nbsp; | &nbsp; **⚖️ Weight:** {weight}
            **🎂 Age:** {athlete.get('Age', 'N/A')} years ({athlete.get('birth_date', 'N/A')})
            """)
else:
    st.warning("No athletes found for the current filters.")

st.divider()

# ==============================================================================
# TASK 2: AGE DISTRIBUTION
# ==============================================================================
st.subheader("📊 Athlete Age Distribution")

if not df_athletes_filtered.empty:
    # Use the filtered dataset directly
    plot_data = df_athletes_filtered.copy()
    
    # Optional Local Filter: Compare specific sports within the global selection
    available_sports = sorted(plot_data['disciplines'].unique())
    selected_sports_local = st.multiselect('Compare specific sports (Optional):', available_sports)

    if selected_sports_local: 
        plot_data = plot_data[plot_data['disciplines'].isin(selected_sports_local)]

    # Display statistics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Total Athletes", len(plot_data))
    with col2: st.metric("Men", len(plot_data[plot_data['gender'] == 'Male']))
    with col3: st.metric("Women", len(plot_data[plot_data['gender'] == 'Female']))
    with col4: st.metric("Avg Age", f"{plot_data['Age'].mean():.1f}")
    with col5: st.metric("Age Range", f"{plot_data['Age'].min():.0f} - {plot_data['Age'].max():.0f}")

    if not plot_data.empty:
        violin_fig = px.violin(
            plot_data,
            y='Age',
            x='disciplines',
            color="gender",
            violinmode="overlay",
            box=True,
            points='all', # Warning: Can be slow if too many points
            title="Age Distribution by Sport & Gender",
            color_discrete_map={'Male': '#36A2EB', 'Female': '#FF6384'}
        )
        st.plotly_chart(violin_fig, use_container_width=True)
else:
    st.warning("No data available for Age Distribution.")

st.divider()

# ==============================================================================
# TASK 3: GENDER DISTRIBUTION
# ==============================================================================
st.subheader("👫 Gender Distribution")

if not df_athletes_filtered.empty:
    plot_data_gender = df_athletes_filtered

    # 3. Create Pie Chart
    if not plot_data_gender.empty:
        fig_gender = px.pie(
            plot_data_gender, 
            names='gender', 
            title=f"Gender Distribution",
            color='gender',
            color_discrete_map={'Male': '#36A2EB', 'Female': '#FF6384'}
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    else:
        st.info("No data for this specific grouping.")
else:
    st.warning("No data available for Gender Distribution.")

st.divider()

# ==============================================================================
# TASK 4: TOP ATHLETES BY MEDAL COUNT
# ==============================================================================
st.subheader("🏅 Top Athletes by Medal Count")
if not df_medals_filtered.empty:
    
    # Local Filter: Sorting Priority
    col_sort, _ = st.columns([1, 3])
    sort_options = ['Gold', 'Silver', 'Bronze', 'Total']
    sel_sort = col_sort.multiselect("Sort Priority", sort_options, default=['Total'])

    # 1. Pivot Data
    df_pivot = df_medals_filtered.pivot_table(
        index='name', 
        columns='medal_type', 
        aggfunc='size', 
        fill_value=0
    )

    # Ensure columns exist
    for medal in ['Gold Medal', 'Silver Medal', 'Bronze Medal']:
        if medal not in df_pivot.columns: df_pivot[medal] = 0

    # Calculate Total
    df_pivot['Total'] = df_pivot['Gold Medal'] + df_pivot['Silver Medal'] + df_pivot['Bronze Medal']

    # 2. Sort Data
    map_sort = {'Gold': 'Gold Medal', 'Silver': 'Silver Medal', 'Bronze': 'Bronze Medal', 'Total': 'Total'}
    
    if not sel_sort:
        sort_by_cols = ['Total']
    else:
        sort_by_cols = [map_sort[x] for x in sel_sort]

    # Get Top 10
    top_10_df = df_pivot.sort_values(sort_by_cols, ascending=False).head(10).reset_index()

    # 3. Prepare Plot
    df_plot = top_10_df.melt(
        id_vars=['name', 'Total'], 
        value_vars=['Gold Medal', 'Silver Medal', 'Bronze Medal'], 
        var_name='medal_type', 
        value_name='Count'
    )

    # 4. Plot
    fig_top = px.bar(
        df_plot,
        x="Count",
        y="name",
        color="medal_type",
        title=f"Top 10 Athletes (Sorted by: {', '.join(sel_sort) if sel_sort else 'Total'})",
        orientation='h',
        text='Count',
        color_discrete_map={
            'Gold Medal': '#FFD700',
            'Silver Medal': '#C0C0C0',
            'Bronze Medal': '#CD7F32'
        },
        category_orders={
            "name": top_10_df['name'].tolist(),
            "medal_type": ['Gold Medal', 'Silver Medal', 'Bronze Medal'] 
        }
    )

    fig_top.update_traces(textposition='inside', texttemplate='%{text}')
    fig_top.update_layout(
        yaxis=dict(title="", automargin=True),
        xaxis=dict(title="Medal Count", showgrid=False),
        legend=dict(orientation="h", title=None, y=-0.1),
        height=500
    )
    
    st.plotly_chart(fig_top, use_container_width=True)

else:
    st.warning("No medals found for the current Global Filters.")