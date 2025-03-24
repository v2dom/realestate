import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.title("Real Estate Data Dashboard")

# Load data from the database
try:
    conn = sqlite3.connect("database.db")
    df = pd.read_sql("SELECT * FROM listings", conn)
    conn.close()
    
    if df.empty:
        st.warning("No data found in the database. Please run the scraper first.")
    else:
        st.subheader("Listings Overview")
        st.dataframe(df)
        
        st.subheader("Price Distribution")
        fig = px.histogram(df, x="Price", title="Price Distribution of Listings")
        st.plotly_chart(fig)
        
except Exception as e:
    st.error(f"An error occurred: {e}")