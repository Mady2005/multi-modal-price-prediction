# Multi-Modal Product Price Prediction

Developed an advanced multi-modal (text/image) price prediction model for an e-commerce dataset of 150,000+ products.

### Core Features
* Engineered over 2,500+ features from **unstructured text** by creating a hybrid pipeline combining:
    * **Foundation Model Embeddings:** Using `Sentence-Transformers` (`all-MiniLM-L6-v2`) to capture semantic meaning.
    * **Keyword Analysis:** `TF-IDF` vectorization to identify high-importance phrases.
    * **Forensic Parsing:** `Regex` and keyword matching to extract structured data (e.g., `weight_grams`, `spec_gb`, `brand`).
* Implemented a **Deep Learning** pipeline using `CLIP` (a `ViT` Foundation Model) to analyze and convert all product images into 512-dimension semantic vectors for visual feature extraction.
* Trained and tuned a robust ensemble of `LightGBM` and `XGBoost` (GPU-accelerated) models using 5-Fold Cross-Validation, achieving high accuracy on the **SMAPE** metric.

### Technologies Used
* Python
* Pandas & NumPy
* Scikit-learn
* TensorFlow/PyTorch (via `sentence-transformers` & `clip`)
* LightGBM
* XGBoost
* Git

### How to Run
1.  Data for this project can be found at [Link to Kaggle Competition Page].
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the `price_prediction_model.ipynb` notebook.
