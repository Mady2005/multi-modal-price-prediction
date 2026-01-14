# Render Deployment Fix Guide

## ✅ Pre-Deployment Verification (Completed)

- ✅ model.pkl exists (1.53 MB)
- ✅ vectorizer.pkl exists (78.34 KB)
- ✅ requirements.txt is complete
- ✅ FastAPI app imports successfully
- ✅ All dependencies are listed

## 🔧 Common Render Deployment Issues & Solutions

### Issue 1: Files Not in Git Repository

**Problem**: Model files or Python files not committed to Git

**Solution**:
```powershell
# Check what's in your Git repository
git status

# Add all necessary files
git add model.pkl vectorizer.pkl app.py feature_engineering.py requirements.txt config.py
git commit -m "Add all deployment files"
git push origin main
```

**⚠️ IMPORTANT**: Render deploys from your Git repository, not your local files!

### Issue 2: Incorrect Start Command

**Problem**: Wrong uvicorn command or port

**Correct Start Command**:
```
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Verify in Render Dashboard**:
- Go to your service settings
- Check "Start Command" field
- Should be exactly: `uvicorn app:app --host 0.0.0.0 --port 8000`

### Issue 3: Python Version Mismatch

**Problem**: Render using wrong Python version

**Solution**: Create a `runtime.txt` file

### Issue 4: Build Command Issues

**Correct Build Command**:
```
pip install -r requirements.txt
```

## 📋 Step-by-Step Render Deployment Checklist

### Step 1: Ensure All Files Are Committed to Git

```powershell
# Check Git status
git status

# If model files show as "not staged" or "untracked":
git add model.pkl vectorizer.pkl
git add app.py feature_engineering.py config.py
git add requirements.txt
git commit -m "Add all deployment files"
git push origin main
```

### Step 2: Create/Update Render Service

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your Git repository
4. Configure:

**Service Configuration**:
```
Name: smart-pricing-api
Runtime: Python 3
Branch: main
Build Command: pip install -r requirements.txt
Start Command: uvicorn app:app --host 0.0.0.0 --port 8000
Instance Type: Free
```

### Step 3: Wait for Deployment

- Build phase: 2-5 minutes
- Deploy phase: 1-2 minutes
- Watch the logs for errors

### Step 4: Check Logs for Specific Errors

**Look for these in the logs**:

✅ **Success indicators**:
```
==> Build successful
Loading model artifacts...
Application startup complete
Uvicorn running on http://0.0.0.0:8000
```

❌ **Error indicators**:
```
FileNotFoundError: model.pkl
ModuleNotFoundError: No module named 'feature_engineering'
Error: Could not find application 'app:app'
```

## 🚨 Most Common Error Solutions

### Error: "FileNotFoundError: model.pkl"

**Cause**: Model files not in Git repository

**Fix**:
```powershell
git add model.pkl vectorizer.pkl
git commit -m "Add model files"
git push origin main
```

### Error: "ModuleNotFoundError: No module named 'X'"

**Cause**: Missing dependency in requirements.txt

**Fix**: Add the missing package to requirements.txt and push

### Error: "Could not find application 'app:app'"

**Cause**: Incorrect start command or app.py structure

**Fix**: Verify start command is `uvicorn app:app --host 0.0.0.0 --port 8000`

### Error: Build takes too long / times out

**Cause**: Large dependencies (lightgbm, scikit-learn)

**Fix**: This is normal, wait 5-7 minutes for first build

## 🧪 Testing After Deployment

Once deployed, test with:

```powershell
# Replace with your actual Render URL
$apiUrl = "https://your-service-name.onrender.com/predict"

$body = @{
    catalog_content = "Apple iPhone 14 Pro 128GB"
} | ConvertTo-Json

Invoke-RestMethod -Uri $apiUrl -Method Post -Body $body -ContentType "application/json"
```

Expected response:
```json
{
  "predicted_price": 899.99,
  "currency": "USD",
  "status": "success"
}
```

## 📝 What to Share If Still Failing

If deployment still fails, please share:

1. **Last 30 lines of the deployment logs** (from Render dashboard)
2. **Service URL** (from Render dashboard)
3. **Specific error message** (usually in red in the logs)

## 🎯 Quick Checklist

Before asking for help, verify:

- [ ] All files committed to Git and pushed
- [ ] Build command is: `pip install -r requirements.txt`
- [ ] Start command is: `uvicorn app:app --host 0.0.0.0 --port 8000`
- [ ] Runtime is set to Python 3
- [ ] Waited at least 5 minutes for build to complete
- [ ] Checked logs for specific error messages

## 🔄 Alternative: Try Railway (Easier than Render)

If Render continues to fail, Railway is often easier:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and FastAPI
6. Click "Deploy"

Railway often "just works" with less configuration!

