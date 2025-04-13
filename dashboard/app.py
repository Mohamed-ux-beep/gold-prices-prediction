# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv("data/gold_prices.csv", parse_dates=["timestamp"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Page title
st.title("📈 Gold Price Tracker")
st.line_chart(df.set_index("timestamp")["price_eur"])

# Optional: Stats
st.write("Latest Price:", df.iloc[-1]["price_eur"], "EUR")
st.write("Total Records:", len(df))

