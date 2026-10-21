import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC")
st.caption("Explore the first 10,000 records from the September 2014 dataset.")

DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

@st.cache_data
def load_data():
    frame = pd.read_csv(DATA_URL, nrows=10000)
    frame.columns = frame.columns.str.lower()
    frame["date/time"] = pd.to_datetime(frame["date/time"])
    return frame

with st.spinner("Loading pickup data..."):
    pickups = load_data()

if st.checkbox("Show raw data"):
    st.subheader("Raw pickup records")
    st.dataframe(pickups)

st.subheader("Pickups by hour")
counts, _ = np.histogram(
    pickups["date/time"].dt.hour,
    bins=24,
    range=(0, 24),
)
hourly = pd.DataFrame(
    {"Pickups": counts},
    index=pd.Index(range(24), name="Hour"),
)
st.bar_chart(hourly)

selected_hour = st.slider("Select an hour", 0, 23, 17)
selected = pickups[
    pickups["date/time"].dt.hour == selected_hour
]

st.subheader(f"Pickup locations: {selected_hour:02d}:00–{selected_hour:02d}:59")
st.write(f"{len(selected):,} pickups in the loaded sample.")
st.map(selected[["lat", "lon"]])