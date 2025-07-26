# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    h1, h2, h3 {
        color: #31333f;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .block-container {
        padding: 2rem 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🦠 Covid-19 Data Visualization Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("covid_data.csv")
    df = df[df["iso_code"].str.len() == 3]  # Filter only countries
    df["date"] = pd.to_datetime(df["date"])
    return df

data = load_data()

# Sidebar - country selection
st.sidebar.header("🌍 Select a Country")
countries = data["location"].unique()
country = st.sidebar.selectbox("", sorted(countries))

# Filter data by selected country
country_data = data[data["location"] == country]

# Latest available data
latest_data = country_data.sort_values("date", ascending=False).iloc[0]

# Show metrics
st.markdown("## 📍 Covid Summary for **{}**".format(country))
col1, col2, col3 = st.columns(3)
col1.metric("Total Cases", f'{int(latest_data["total_cases"] or 0):,}')
col2.metric("Total Deaths", f'{int(latest_data["total_deaths"] or 0):,}')
col3.metric("Total Vaccinations", f'{int(latest_data["total_vaccinations"] or 0):,}')

# Line chart - Daily new cases
st.markdown("---")
st.markdown("## 📈 Daily New Cases")
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(country_data["date"], country_data["new_cases"], color="orange", linewidth=2)
ax1.set_xlabel("Date")
ax1.set_ylabel("New Cases")
ax1.set_title(f"Daily New Cases in {country}")
st.pyplot(fig1)

# Bar chart - Total Cases & Deaths over time
st.markdown("---")
st.markdown("## 📊 Total Cases vs Deaths")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(country_data["date"], country_data["total_cases"], label="Total Cases", color="blue", linewidth=2)
ax2.plot(country_data["date"], country_data["total_deaths"], label="Total Deaths", color="red", linewidth=2)
ax2.set_xlabel("Date")
ax2.set_ylabel("Count")
ax2.legend()
st.pyplot(fig2)

# Pie chart - Case breakdown
if not pd.isna(latest_data["total_cases"]) and not pd.isna(latest_data["total_deaths"]):
    st.markdown("---")
    st.markdown("## 🧩 Recovered vs Deaths")
    recovered = latest_data["total_cases"] - latest_data["total_deaths"]
    pie_labels = ["Recovered", "Deaths"]
    pie_data = [recovered, latest_data["total_deaths"]]
    fig3, ax3 = plt.subplots()
    ax3.pie(pie_data, labels=pie_labels, autopct="%1.1f%%", colors=["#00cc96", "#ef553b"])
    st.pyplot(fig3)
