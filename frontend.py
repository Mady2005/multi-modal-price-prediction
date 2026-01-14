import streamlit as st
import requests
import pandas as pd
import json
import os

# Define the API URL (Use environment variable for cloud deployment, fallback to localhost for local dev)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

# Page Config
st.set_page_config(
    page_title="Smart Pricing AI",
    page_icon="💰",
    layout="centered"
)

# Title and Description
st.title("💰 Smart Pricing AI")
st.markdown("### Production-Grade Price Prediction System")
st.info("This system uses a Multi-Modal AI (Text + Specs) to suggest optimal pricing.")

# Input Form
with st.form("prediction_form"):
    st.header("Product Details")
    
    product_desc = st.text_area(
        "Product Description (Catalog Content)",
        height=150,
        placeholder="e.g. Pack of 12 Apple iPhones 16GB with A15 Bionic chip..."
    )
    
    # Submit Button
    submitted = st.form_submit_button("Predict Price 🚀")

if submitted:
    if not product_desc:
        st.warning("Please enter a product description.")
    else:
        with st.spinner("Analyzing market data..."):
            try:
                # 1. Send data to your FastAPI Backend (Docker)
                payload = {"catalog_content": product_desc}
                response = requests.post(API_URL, json=payload)
                
                # 2. Handle the response
                if response.status_code == 200:
                    result = response.json()
                    price = result['predicted_price']
                    currency = result['currency']
                    
                    # 3. Display Result
                    st.success("Prediction Complete!")
                    
                    # Create nice metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Suggested Price", f"{currency} {price}")
                    col2.metric("Confidence Score", "High") # Placeholder
                    col3.metric("Model Version", "v1.0.0")
                    
                    # Show raw JSON for debug (optional)
                    with st.expander("See API Response"):
                        st.json(result)
                        
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("🚨 Could not connect to the Backend API.")
                st.caption("Is your Docker container running on port 8000?")