# utils.py
import streamlit as st
import pandas as pd
import os
import pycountry_convert as pc
from datetime import date
import pycountry 

# --- 1. HELPER FUNCTIONS ---
def get_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except:
        return "Other"

def calculate_age(birth_date):
    if pd.isnull(birth_date): return None
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# --- 2. DATA LOADING (Centralized & Cached) ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    athletes = pd.read_csv(os.path.join(data_dir, 'athletes.csv'))
    medallists = pd.read_csv(os.path.join(data_dir, 'medallists.csv'))
    nocs = pd.read_csv(os.path.join(data_dir, 'nocs.csv'))
    events = pd.read_csv(os.path.join(data_dir, 'events.csv'))
    
    # 1. Clean Athletes Data
    # Clean disciplines string: "['Swimming']" -> "Swimming"
    athletes['disciplines'] = athletes['disciplines'].astype(str).str.replace(r"[\[\]']", "", regex=True)
    
    # Calculate Age
    athletes['birth_date'] = pd.to_datetime(athletes['birth_date'], errors='coerce')
    athletes['Age'] = athletes['birth_date'].apply(calculate_age)
    
    # Get Continent
    athletes['Continent'] = athletes['country'].apply(get_continent)
    
    # 2. MERGE: Join Athletes info (Age, Gender) into Medallists
    # We drop 'gender' from medallists first so we can replace it with the clean 'gender' from athletes
    medallists = medallists.drop(columns=['gender'], errors='ignore')
    
    medallists = medallists.merge(
        athletes[['code', 'Age', 'gender']], # Select only what we need to add/fix
        left_on='code_athlete',              # Key in Medallists
        right_on='code',                     # Key in Athletes
        how='left'
    )
    
    # 3. Final Polish for Medallists
    medallists['Continent'] = medallists['country'].apply(get_continent)
    
    return athletes, medallists, nocs, events


# --- 3. SIDEBAR FILTER WIDGETS ---
def create_sidebar(athletes_df):
    st.sidebar.header("🌍 Global Filters")

    # 1. Continent
    all_continents = sorted(athletes_df['Continent'].unique())
    sel_continent = st.sidebar.multiselect("Select Continent", all_continents)
    if not sel_continent: sel_continent = all_continents

    # 2. Country (Cascading)
    available_countries = sorted(athletes_df[athletes_df['Continent'].isin(sel_continent)]['country'].unique())
    sel_country = st.sidebar.multiselect("Select Country", available_countries)
    if not sel_country: sel_country = available_countries

    # 3. Sport
    all_sports = sorted(athletes_df['disciplines'].unique())
    sel_sport = st.sidebar.multiselect("Select Sport", all_sports)
    if not sel_sport: sel_sport = all_sports

    # 4. Gender
    all_genders = sorted(athletes_df['gender'].dropna().unique())
    sel_gender = st.sidebar.multiselect("Select Gender", all_genders)
    if not sel_gender: sel_gender = all_genders

    # 5. Age
    min_age = int(athletes_df['Age'].min())
    max_age = int(athletes_df['Age'].max())
    sel_age = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))

    # Return dictionary of selected filters
    return {
        "continent": sel_continent,
        "country": sel_country,
        "sport": sel_sport,
        "gender": sel_gender,
        "age": sel_age
    }
    
def get_iso3_code(country_name):
    try:
        # Fuzzy search handles "United States" -> "USA"
        country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_3
    except:
        # Manual mappings for Olympic specific names
        manual_map = {
            'Great Britain': 'GBR',
            'Korea': 'KOR',
            'Chinese Taipei': 'TWN',
            'Hong Kong, China': 'HKG',
            'Refugee Olympic Team': None,
            'Kosovo': 'XKX'
        }
        return manual_map.get(country_name, None)
    
    

def count_medals(df):
    """
    Counts medals correctly by handling team sports.
    Drops duplicate rows for the same Event + Country + Medal Type.
    """
    if df.empty:
        return df
    
    # We keep only ONE row per Country per Event per Medal Type
    # e.g., Merges 19 Moroccan Football players into 1 row
    return df.drop_duplicates(subset=['country', 'discipline', 'event', 'medal_type'])