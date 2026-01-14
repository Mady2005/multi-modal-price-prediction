# 💰 Smart Pricing AI - Multi-Modal Product Price Prediction

An advanced multi-modal (text/image) price prediction system for e-commerce, featuring a production-ready FastAPI backend, Streamlit frontend, and analytics dashboard. Trained on 150,000+ products with deployment-ready architecture.

## 🎯 Project Overview

This project combines machine learning, feature engineering, and modern web technologies to create a complete pricing intelligence system that can be deployed to the cloud.

### Core ML Features
* **Engineered 2,500+ features** from unstructured text using a hybrid pipeline:
    * **Foundation Model Embeddings:** `Sentence-Transformers` (`all-MiniLM-L6-v2`) for semantic understanding
    * **Keyword Analysis:** `TF-IDF` vectorization for high-importance phrase identification
    * **Forensic Parsing:** `Regex` and keyword matching to extract structured data (`weight_grams`, `spec_gb`, `brand`)
* **Deep Learning Vision Pipeline:** `CLIP` (ViT Foundation Model) to convert product images into 512-dimension semantic vectors
* **Robust Ensemble Models:** `LightGBM` and `XGBoost` (GPU-accelerated) with 5-Fold Cross-Validation, optimized for **SMAPE** metric

### Production Features
* **FastAPI REST API:** High-performance backend with automatic documentation
* **Streamlit Frontend:** User-friendly web interface for price predictions
* **Analytics Dashboard:** Real-time insights and pricing trends visualization
* **Cloud-Ready:** Deployment configurations for Railway, Render, and Streamlit Cloud
* **Database Integration:** PostgreSQL support for data persistence
* **Environment-Based Config:** Seamless local development and cloud deployment

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Smart Pricing AI                      │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │  Streamlit   │─────▶│   FastAPI    │                │
│  │  Frontend    │      │   Backend    │                │
│  │ (frontend.py)│      │   (app.py)   │                │
│  └──────────────┘      └──────────────┘                │
│                               │                          │
│  ┌──────────────┐            │                          │
│  │  Analytics   │            │                          │
│  │  Dashboard   │            │                          │
│  │(dashboard.py)│            │                          │
│  └──────┬───────┘            │                          │
│         │                    │                          │
│         │    ┌───────────────▼────────┐                │
│         └───▶│  PostgreSQL Database   │                │
│              │   (Product Data)       │                │
│              └────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd smart-pricing-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the FastAPI backend**
```bash
uvicorn app:app --reload
```
Access API docs at: `http://localhost:8000/docs`

4. **Run the Streamlit frontend** (in a new terminal)
```bash
streamlit run frontend.py
```
Access frontend at: `http://localhost:8501`

5. **Run the analytics dashboard** (optional)
```bash
streamlit run dashboard.py
```

### Alternative: Unified Streamlit App

For simpler deployment, use the all-in-one Streamlit app:
```bash
streamlit run streamlit_app.py
```
This combines the frontend and backend into a single application.

## ☁️ Cloud Deployment

### Option 1: Railway (Recommended - Easiest)

**Deploy FastAPI Backend:**
1. Go to https://railway.app
2. Sign up with GitHub (get $5 free credit)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Railway auto-detects Python and deploys!

**Detailed guide:** See `DEPLOY_NOW.md`

### Option 2: Streamlit Cloud

**Deploy Unified App:**
1. Go to https://share.streamlit.io
2. Connect your GitHub repository
3. Select `streamlit_app.py` as the main file
4. Deploy!

### Option 3: Render

**Deploy Backend:**
- Follow the guide in `.kiro/specs/render-deployment/`
- Includes PostgreSQL database setup
- Full microservices architecture

## 📁 Project Structure

```
smart-pricing-ai/
├── app.py                      # FastAPI backend API
├── frontend.py                 # Streamlit user interface
├── dashboard.py                # Analytics dashboard
├── streamlit_app.py           # Unified Streamlit app (all-in-one)
├── feature_engineering.py      # Feature extraction utilities
├── model.pkl                   # Trained LightGBM model
├── vectorizer.pkl             # TF-IDF vectorizer
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway/Heroku deployment config
├── config.py                  # Configuration management
├── train.py                   # Model training script
├── etl_pipeline.py           # Data processing pipeline
├── price_prediction_model.ipynb  # Jupyter notebook (development)
├── DEPLOY_NOW.md             # Railway deployment guide
├── RAILWAY_QUICK_START.md    # Quick Railway setup
└── .kiro/specs/              # Deployment specifications
    └── render-deployment/    # Render deployment guides
```

## 🛠️ Technologies Used

### Machine Learning & Data Science
* Python 3.9+
* Pandas & NumPy
* Scikit-learn
* TensorFlow/PyTorch (via `sentence-transformers` & `clip`)
* LightGBM
* XGBoost

### Web Framework & API
* FastAPI - High-performance REST API
* Uvicorn - ASGI server
* Pydantic - Data validation

### Frontend & Visualization
* Streamlit - Interactive web apps
* Plotly - Data visualization
* Requests - HTTP client

### Database & Storage
* PostgreSQL - Relational database
* SQLAlchemy - ORM
* psycopg2 - PostgreSQL adapter

### Deployment & DevOps
* Railway - Cloud platform
* Render - Cloud platform
* Streamlit Cloud - Streamlit hosting
* Docker - Containerization (optional)
* Git - Version control

## 📊 API Endpoints

### POST `/predict`
Predict the price of a product based on its description.

**Request:**
```json
{
  "catalog_content": "Apple iPhone 14 Pro 128GB Space Black"
}
```

**Response:**
```json
{
  "predicted_price": 899.99,
  "currency": "USD",
  "status": "success"
}
```

### GET `/docs`
Interactive API documentation (FastAPI auto-generated)

## 🧪 Testing

Run unit tests:
```bash
pytest test_config.py
```

Test the API locally:
```powershell
$body = @{ catalog_content = "Samsung Galaxy S23 Ultra" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body -ContentType "application/json"
```

## 📈 Model Performance

* **Metric:** SMAPE (Symmetric Mean Absolute Percentage Error)
* **Training Data:** 150,000+ products
* **Features:** 2,500+ engineered features
* **Cross-Validation:** 5-Fold CV
* **Models:** LightGBM + XGBoost ensemble

## 🔧 Configuration

### Environment Variables

**Frontend (`frontend.py`):**
- `API_URL` - FastAPI backend URL (default: `http://127.0.0.1:8000/predict`)

**Dashboard (`dashboard.py`):**
- `DATABASE_URL` - PostgreSQL connection string

**Local Development:**
- No environment variables needed (uses localhost defaults)

**Cloud Deployment:**
- Set environment variables in your platform's dashboard

## 📝 Development Workflow

1. **Train Model:** Run `price_prediction_model.ipynb` or `train.py`
2. **Test Locally:** Start FastAPI backend and Streamlit frontend
3. **Verify API:** Test `/predict` endpoint with sample data
4. **Deploy Backend:** Use Railway or Render
5. **Deploy Frontend:** Use Streamlit Cloud
6. **Monitor:** Check logs and performance metrics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Resources

* **Dataset:** [Link to Kaggle Competition Page]
* **Railway Deployment:** See `DEPLOY_NOW.md`
* **Render Deployment:** See `.kiro/specs/render-deployment/`
* **API Documentation:** Available at `/docs` endpoint when running

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, Streamlit, and LightGBM**
