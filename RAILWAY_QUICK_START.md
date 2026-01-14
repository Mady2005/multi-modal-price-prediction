# 🚂 Railway Deployment - Quick Start Guide

## Why Railway?

Railway is **easier than Render** for FastAPI:
- ✅ Automatic configuration
- ✅ Better error messages  
- ✅ Faster deployments (2-3 min)
- ✅ Free $5 credit (no credit card needed)

---

## 5-Minute Deployment

### Step 1: Sign Up
1. Go to **https://railway.app**
2. Click **"Start a New Project"**
3. Sign up with GitHub
4. Get **$5 free credit**

### Step 2: Deploy
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your Smart Pricing AI repository
4. Click **"Deploy Now"**

Railway automatically detects Python and deploys!

### Step 3: Get URL
1. Go to **"Settings"** → **"Domains"**
2. Click **"Generate Domain"**
3. Copy URL (e.g., `https://your-app.up.railway.app`)

### Step 4: Test
Open in browser: `https://your-app.up.railway.app/docs`

**PowerShell test:**
```powershell
$url = "https://your-app.up.railway.app/predict"
$body = @{ catalog_content = "Apple iPhone 14 Pro" } | ConvertTo-Json
Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json"
```

---

## Files Needed (Already in Repo)

✅ `app.py` - FastAPI backend
✅ `model.pkl` - Trained model  
✅ `vectorizer.pkl` - TF-IDF vectorizer
✅ `requirements.txt` - Dependencies
✅ `Procfile` - Start command (just created)

---

## Verification Checklist

- [ ] Deployment shows "Success" ✅
- [ ] Logs show "Loading model artifacts..."
- [ ] Logs show "Application startup complete"
- [ ] `/docs` endpoint accessible
- [ ] `/predict` returns predictions

---

## Common Issues

**Model files not found?**
```bash
git add model.pkl vectorizer.pkl
git commit -m "Add models"
git push
```

**Build failed?**
Check Railway logs for specific error

**App crashed?**
Verify app.py has no syntax errors

---

## Next Steps

Once deployed:
1. Save your Railway URL
2. Use it for frontend deployment
3. Test the `/predict` endpoint

**That's it! Railway handles everything else automatically.** 🚀
