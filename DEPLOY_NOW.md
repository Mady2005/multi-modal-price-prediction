# 🚀 Deploy to Railway NOW - Checklist

## Pre-Deployment Check ✅

All files are ready in your repository:
- ✅ `app.py` - FastAPI backend
- ✅ `feature_engineering.py` - Feature processing
- ✅ `model.pkl` - ML model (1.6 MB)
- ✅ `vectorizer.pkl` - TF-IDF vectorizer (80 KB)
- ✅ `requirements.txt` - All dependencies listed
- ✅ `Procfile` - Railway start command

## Deployment Steps (5 minutes)

### 1. Go to Railway
**URL:** https://railway.app

### 2. Sign Up
- Click "Start a New Project"
- Sign up with GitHub (easiest)
- You get $5 free credit automatically

### 3. Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Connect your GitHub account
- Select this repository
- Click "Deploy Now"

### 4. Wait for Build (2-3 minutes)
Railway will automatically:
- Install Python dependencies
- Load your model files
- Start the FastAPI server
- Assign a public URL

### 5. Generate Domain
- Go to "Settings" tab
- Scroll to "Domains" section
- Click "Generate Domain"
- Copy your URL

### 6. Test Your API

**Browser Test:**
```
https://your-app.up.railway.app/docs
```

**PowerShell Test:**
```powershell
$apiUrl = "https://your-app.up.railway.app/predict"

$body = @{
    catalog_content = "Apple iPhone 14 Pro 128GB Space Black"
} | ConvertTo-Json

Invoke-RestMethod -Uri $apiUrl -Method Post -Body $body -ContentType "application/json"
```

**Expected Response:**
```json
{
  "predicted_price": 899.99,
  "currency": "USD",
  "status": "success"
}
```

## Success Indicators

✅ Deployment status: "Success" (green)
✅ Logs show: "Loading model artifacts..."
✅ Logs show: "Application startup complete"
✅ `/docs` endpoint loads
✅ `/predict` returns predictions

## If Something Goes Wrong

**Check the logs in Railway dashboard:**
- Click on your deployment
- Go to "Deployments" tab
- Look for error messages (in red)

**Common fixes:**
1. Model files missing → Commit and push model.pkl and vectorizer.pkl
2. Dependency error → Check requirements.txt
3. Syntax error → Check app.py for typos

## After Successful Deployment

**Save your Railway URL:**
```
Backend API: https://your-app.up.railway.app
Prediction Endpoint: https://your-app.up.railway.app/predict
Documentation: https://your-app.up.railway.app/docs
```

**Use this URL for:**
- Frontend deployment (set as API_URL environment variable)
- Testing and development
- Production use

---

## Ready? Let's Deploy! 🚂

1. Open https://railway.app
2. Follow the 6 steps above
3. Come back when deployed (or if you hit any issues)

**Estimated time: 5 minutes**
**Difficulty: Easy** ⭐⭐⭐⭐⭐
