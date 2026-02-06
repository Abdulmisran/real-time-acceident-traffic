import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚦 Road Accident Analysis Dashboard (Real Data)")

# -----------------------
# Load Data
# -----------------------
data = pd.read_csv("accident_prediction_india.csv")

# Try parsing date if exists
for col in data.columns:
    if "date" in col.lower():
        data[col] = pd.to_datetime(data[col], errors="coerce")
        date_col = col
        break
else:
    date_col = None

st.subheader("Dataset Preview")
st.dataframe(data.head())

# -----------------------
# Basic Metrics
# -----------------------
st.subheader("Key Metrics")

col1, col2 = st.columns(2)
col1.metric("Total Records", len(data))

if "casualties" in data.columns:
    col2.metric("Total Casualties", int(data["casualties"].sum()))

# -----------------------
# City / Area Hotspots
# -----------------------
loc_col = [c for c in data.columns if "city" in c.lower() or "state" in c.lower()]

if loc_col:
    loc = loc_col[0]
    hotspot = data[loc].value_counts().head(10).reset_index()
    hotspot.columns = ["location","count"]

    fig_hot = px.bar(hotspot, x="location", y="count",
                     title="Top Accident Hotspots")
    st.plotly_chart(fig_hot)

# -----------------------
# Severity Distribution
# -----------------------
sev_col = [c for c in data.columns if "severity" in c.lower()]

if sev_col:
    fig_sev = px.pie(data, names=sev_col[0],
                     title="Accident Severity Distribution")
    st.plotly_chart(fig_sev)

# -----------------------
# Weather Impact
# -----------------------
weather_col = [c for c in data.columns if "weather" in c.lower()]

if weather_col:
    w = data[weather_col[0]].value_counts().reset_index()
    w.columns = ["weather","count"]

    fig_weather = px.bar(w, x="weather", y="count",
                         title="Accidents by Weather Condition")
    st.plotly_chart(fig_weather)

# -----------------------
# Monthly Trend
# -----------------------
if date_col:
    data["month"] = data[date_col].dt.to_period("M").astype(str)
    m = data["month"].value_counts().sort_index().reset_index()
    m.columns = ["month","count"]

    fig_month = px.line(m, x="month", y="count",
                        title="Monthly Accident Trend")
    st.plotly_chart(fig_month)
