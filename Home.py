import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Paris 2024 Dashboard | Home",
    page_icon="🏅",
    layout="wide"
)

# --- SIDEBAR: AUTHOR INFO ---
with st.sidebar:
    st.markdown("### 👨‍💻 Created By:")
    st.info("**Abderrahim Zineddine**\n\nGroup 03")
    st.divider()
    st.markdown("### ℹ️ About")
    st.caption("Submitted for the **LA28 Volunteer Selection Challenge**.")

# --- MAIN HERO SECTION ---
st.title("🏅 Paris 2024 Olympic Games Dashboard")
st.markdown("### 🚀 LA28 Volunteer Selection Challenge")

st.markdown("""
Welcome to the interactive data analysis dashboard for the Paris 2024 Olympics. 
This application processes over **11,000 athletes** and **329 events** to bring you actionable insights for the upcoming LA28 selection process.
""")

st.divider()

# --- PAGE GUIDES (GRID LAYOUT) ---
st.subheader("📚 Dashboard Navigation Guide")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### 🏠 Page 1: Overview")
        st.markdown("""
        **"The Command Center"**
        *   **KPIs:** Real-time metrics on Athletes, Countries, and Medals.
        *   **Global Distribution:** Pie charts of medal types.
        *   **Rankings:** Top 10 performing nations.
        """)

    with st.container(border=True):
        st.markdown("#### 👤 Page 3: Athlete Performance")
        st.markdown("""
        **"The Human Story"**
        *   **Profile Card:** Detailed stats for every single athlete.
        *   **Demographics:** Age & Gender distribution analysis.
        *   **Top Performers:** Who won the most individual medals?
        """)

with col2:
    with st.container(border=True):
        st.markdown("#### 🗺️ Page 2: Global Analysis")
        st.markdown("""
        **"The World View"**
        *   **Choropleth Map:** Interactive world map of medal counts.
        *   **Hierarchy:** Sunburst & Treemaps breaking down Continent > Country > Sport.
        *   **Regional Stats:** Comparative bar charts by continent.
        """)

    with st.container(border=True):
        st.markdown("#### 🏟️ Page 4: Sports & Events")
        st.markdown("""
        **"The Arena"**
        *   **Schedule:** Interactive Gantt chart of all 329 events.
        *   **Comparison:** Treemap of medal counts across disciplines.
        *   **Venues:** Mapbox visualization of Olympic sites across France.
        """)

st.divider()

# --- FILTER LOGIC EXPLANATION ---
st.subheader("⚙️ How to use the Filters")

st.markdown("""
This dashboard is equipped with **Global Filters** in the sidebar (Continent, Country, Sport, Gender, Age). 
These filters apply to **almost all charts** to allow for deep-diving into specific data subsets.
""")


st.success("👈 Open the Sidebar to start your journey!")