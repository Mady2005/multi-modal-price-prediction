from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from feature_engineering import process_text_features

# 1. Initialize the App
app = FastAPI(title="Smart Pricing API")

# 2. Load the Artifacts (Model & Vectorizer)
# We load these once when the app starts so it's fast
print("Loading model artifacts...")
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# 3. Define the Input Format
class ProductInput(BaseModel):
    catalog_content: str

# 4. Define the Prediction Endpoint
@app.post("/predict")
def predict_price(item: ProductInput):
    try:
        # A. Create a Series for processing
        input_series = pd.Series([item.catalog_content])

        # B. Generate Regex Features (using your helper file)
        features_parsed = process_text_features(input_series)

        # C. Generate TF-IDF Features (transform only, do not fit!)
        features_tfidf = vectorizer.transform(input_series)

        # D. Combine
        features_final = np.hstack([features_parsed.values, features_tfidf.toarray()])

        # E. Predict
        log_price = model.predict(features_final)
        price = np.expm1(log_price)[0] # Reverse the log transformation

        return {
            "predicted_price": round(float(price), 2),
            "currency": "USD",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run this: uvicorn app:app --reload