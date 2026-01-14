# Railway Deployment Guide - Smart Pricing AI

## Why Railway?
- ✅ Easier than Render (better error messages)
- ✅ $5 free credit per month (no credit card required initially)
- ✅ Automatic deployments from GitHub
- ✅ Built-in PostgreSQL database
- ✅ Simple configuration

## Prerequisites
- GitHub account with your code pushed
- Railway account (sign up at https://railway.app)

---

## Step 1: Prepare Your Repository

Make sure these files are in your GitHub repository:
- ✅ `app.py` (FastAPI backend)
- ✅ `feature_engineering.py`
- ✅ `model.pkl`
- ✅ `vectorizer.pkl`
- ✅ `requirements.txt`
- ✅ `Procfile` (we'll create this)

### Create Procfile

<function_calls>
<invoke name="fsWrite">
<parameter name="path">Procfileb: uvicorn app:app --host 0.0.0.0 --port $PORT
