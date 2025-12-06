# 🏅 Paris 2024 Olympic Games Dashboard

### LA28 Volunteer Selection Challenge
**Author:** Abderrahim Zineddine (Group 03)

## 📖 Overview
This interactive Streamlit dashboard provides a comprehensive analysis of the **Paris 2024 Summer Olympic Games**. Built for the LA28 Volunteer Selection Challenge, it processes data on over 11,000 athletes and 329 events to visualize performance, demographics, and logistics.

The application transforms raw CSV data into interactive narratives, allowing users to explore medal counts, athlete profiles, and the geographical distribution of victories.

---

## 🚀 Features & Pages

The dashboard is structured into four dedicated analysis pages:

### **1. 🏠 Overview (The Command Center)**
*   **High-Level KPIs:** Real-time metrics for Total Athletes, Countries, Sports, and Medals.
*   **Medal Distribution:** Interactive pie charts showing the split of Gold, Silver, and Bronze.
*   **Top Performers:** A dynamic horizontal bar chart ranking the Top 10 countries.

### **2. 🗺️ Global Analysis (The World View)**
*   **Interactive World Map:** A Choropleth map visualizing medal density across the globe.
*   **Hierarchical Drill-Down:** Sunburst and Treemap charts showing the relationship between *Continent > Country > Sport*.
*   **Regional Insights:** Comparative analysis of medal counts by Continent.

### **3. 👤 Athlete Performance (The Human Story)**
*   **Athlete Profile Card:** A searchable interface to view detailed stats (Height, Weight, Coach, Sport) for any athlete.
*   **Demographics:** Analysis of Age and Gender distributions using Violin and Pie charts.
*   **Top Athletes:** Ranking the most decorated individual athletes of the games.

### **4. 🏟️ Sports & Events (The Arena)**
*   **Event Schedule:** An interactive Gantt Chart/Timeline with hourly zooming capabilities.
*   **Sport Comparison:** A Treemap visualizing the total medal output of every sport discipline.
*   **Venue Map:** A Mapbox visualization pinpointing Olympic venues across France and Tahiti.

---

## ⚙️ Global Filters
The sidebar contains powerful filters that persist across pages to customize your analysis:
*   **🌍 Continent & Country:** Filter data by specific regions.
*   **🏃 Sport (Discipline):** Focus on specific sports (e.g., Swimming, Judo).
*   **👫 Gender:** Analyze performance by Male or Female athletes.
*   **🎂 Age Range:** Filter athletes by specific age groups.

---

## 🛠️ Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AbderrahimZineddineEsi/Streamlit-2024-Olympics
    cd  Streamlit-2024-Olympics
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run Home.py
    ```

## 📂 Project Structure
├── Home.py # Main Entry Point 
├── pages/
│ ├── 1_🏠_Overview.py 
│ ├── 2_🗺️_Global_Analysis.py
│ ├── 3_👤_Athlete_Performance.py
│ └── 4_🏟️_Sports_and_Events.py
├── data/ # CSV Datasets
├── utils.py # Helper functions & Data Loading
├── requirements.txt # Python dependencies
└── README.md # Documentation

## 📊 Data Source
The dataset used in this project is sourced from the [Paris 2024 Olympic Summer Games on Kaggle](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games).
