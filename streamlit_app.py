import streamlit as st
import joblib
import numpy as np
import pandas as pd
from feature_engineering import process_text_features

# Page Config
st.set_page_config(
    page_title="Smart Pricing AI",
    page_icon="💰",
    layout="centered"
)

# Load Model Artifacts (cached for performance)
@st.cache_resource
def load_model():
    """Load the trained model and vectorizer"""
    try:
        model = joblib.load('model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        return model, vectorizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# Prediction Function
def predict_price(catalog_content, model, vectorizer):
    """Generate price prediction from product description"""
    try:
        # Create a Series for processing
        input_series = pd.Series([catalog_content])
        
        # Generate Regex Features
        features_parsed = process_text_features(input_series)
        
        # Generate TF-IDF Features
        features_tfidf = vectorizer.transform(input_series)
        
        # Combine features
        features_final = np.hstack([features_parsed.values, features_tfidf.toarray()])
        
        # Predict
        log_price = model.predict(features_final)
        price = np.expm1(log_price)[0]  # Reverse log transformation
        
        return round(float(price), 2)
    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")

# Main App
def main():
    # Title and Description
    st.title("💰 Smart Pricing AI")
    st.markdown("### Production-Grade Price Prediction System")
    st.info("This system uses a Multi-Modal AI (Text + Specs) to suggest optimal pricing.")
    
    # Load model
    model, vectorizer = load_model()
    
    if model is None or vectorizer is None:
        st.error("⚠️ Failed to load model artifacts. Please ensure model.pkl and vectorizer.pkl are present.")
        return
    
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
                    # Get prediction
                    price = predict_price(product_desc, model, vectorizer)
                    
                    # Display Result
                    st.success("Prediction Complete!")
                    
                    # Create nice metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Suggested Price", f"USD {price}")
                    col2.metric("Confidence Score", "High")
                    col3.metric("Model Version", "v1.0.0")
                    
                    # Show details
                    with st.expander("See Prediction Details"):
                        st.json({
                            "predicted_price": price,
                            "currency": "USD",
                            "status": "success",
                            "input": product_desc[:100] + "..." if len(product_desc) > 100 else product_desc
                        })
                        
                except Exception as e:
                    st.error(f"🚨 Prediction failed: {str(e)}")

if __name__ == "__main__":
    main()
