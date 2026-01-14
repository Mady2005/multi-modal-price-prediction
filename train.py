import pandas as pd
import numpy as np
import joblib  # Standard tool for saving ML models
import lightgbm as lgb
from sklearn.feature_extraction.text import TfidfVectorizer
from feature_engineering import process_text_features # Import your own code!

# 1. Load Data
print("Loading data...")
train_df = pd.read_csv('train.csv') # Ensure train.csv is in this folder
y_train = np.log1p(train_df['price'])

# 2. Feature Engineering (Regex/Parsing)
print("Generating regex features...")
X_parsed = process_text_features(train_df['catalog_content'])

# 3. TF-IDF (The Turbocharger)
print("Fitting TF-IDF...")
tfidf = TfidfVectorizer(ngram_range=(1, 3), max_features=2000, stop_words='english')
X_tfidf = tfidf.fit_transform(train_df['catalog_content'].fillna(''))

# 4. Combine Features
# Note: For this API demo, we are SKIPPING embeddings to keep it lightweight. 
# If you want embeddings, you'd load the .npy files here.
X_final = np.hstack([X_parsed.values, X_tfidf.toarray()])

# 5. Train Model
print("Training LightGBM...")
model = lgb.LGBMRegressor(n_estimators=500, learning_rate=0.05, seed=42)
model.fit(X_final, y_train)

# 6. Save Artifacts (CRITICAL STEP)
print("Saving model and vectorizer...")
joblib.dump(model, 'model.pkl')
joblib.dump(tfidf, 'vectorizer.pkl')
print("✅ Done! 'model.pkl' and 'vectorizer.pkl' are ready.")