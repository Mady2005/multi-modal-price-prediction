import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

# 1. Connect to the Database (Use environment variable for cloud deployment, fallback to localhost for local dev)
DB_CONNECTION_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/pricing_data")
engine = create_engine(DB_CONNECTION_URL)

st.set_page_config(page_title="Executive Pricing Dashboard", layout="wide")

st.title("📊 Executive Pricing Dashboard")
st.markdown("### Real-Time Insights from the Data Warehouse")

# 2. Load Data from Postgres
# We use a standard SQL query here
@st.cache_data(ttl=60) # Cache data for 60 seconds so it doesn't reload constantly
def load_data():
    query = "SELECT * FROM products_cleaned"
    return pd.read_sql(query, engine)

try:
    df = load_data()
    
    # --- SECTION A: High-Level KPIs ---
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    total_products = len(df)
    avg_price = df['price'].mean()
    premium_products = len(df[df['price'] > 100])
    
    col1.metric("Total Products Scanned", f"{total_products:,}")
    col2.metric("Average Market Price", f"${avg_price:.2f}")
    col3.metric("Premium Items (>$100)", f"{premium_products:,}")
    
    # --- SECTION B: Deep Dive Analytics ---
    st.divider()
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("💰 Price Distribution")
        # A Histogram shows where most products are priced
        fig_hist = px.histogram(df, x="price", nbins=50, title="How are products priced?", color_discrete_sequence=['#3366cc'])
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col_chart2:
        st.subheader("🏆 Top Brands by Inventory")
        # Let's see which brands appear most often
        if 'brand' in df.columns:
            # Simple pandas logic to get top 10 brands
            top_brands = df['brand'].value_counts().head(10).reset_index()
            top_brands.columns = ['Brand', 'Count']
            
            fig_bar = px.bar(top_brands, x='Count', y='Brand', orientation='h', title="Who dominates the inventory?", color='Count')
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Brand column not found. Did you run the latest ETL?")

    # --- SECTION C: Raw Data Explorer ---
    with st.expander("🔎 Inspect Raw Data (SQL Table View)"):
        st.dataframe(df)

except Exception as e:
    st.error("🚨 Could not connect to the Database!")
    st.write(f"Error details: {e}")
    st.info("💡 Tip: Make sure your Docker container ('pricing_db') is running.")