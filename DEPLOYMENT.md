# Render Deployment Guide for Plant Disease Classifier Backend

## 📋 Prerequisites

1. **GitHub Account** - Your code needs to be on GitHub
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Git Repository** - Your backend code should be committed to Git

## 🚀 Step-by-Step Deployment Instructions

### Step 1: Push Your Code to GitHub

1. **Create a new repository on GitHub:**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `plant-disease-classifier-backend`
   - Make it public or private
   - Don't initialize with README (you already have files)

2. **Connect your local repository to GitHub:**
   ```bash
   cd backend
   git remote add origin https://github.com/Naivedya07/plant-disease-classifier-backend.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Go to Render Dashboard:**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign in or create account

2. **Create New Web Service:**
   - Click "New +" button
   - Select "Web Service"

3. **Connect GitHub Repository:**
   - Choose "Build and deploy from a Git repository"
   - Click "Connect" next to GitHub
   - Authorize Render to access your repositories
   - Select your `plant-disease-classifier-backend` repository

4. **Configure Service Settings:**
   ```
   Name: plant-disease-classifier-backend
   Region: Choose closest to your users
   Branch: main
   Root Directory: (leave blank)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

5. **Set Environment Variables:**
   - Click "Advanced" 
   - Add these environment variables:
   ```
   PORT = 10000
   FLASK_DEBUG = false
   MODEL_PATH = model/plant_disease_model.h5
   ```

6. **Choose Plan:**
   - Select "Free" tier for testing
   - Click "Create Web Service"

### Step 3: Monitor Deployment

1. **Watch Build Logs:**
   - Render will show real-time build logs
   - Wait for "Build successful" message
   - Then wait for "Deploy live" status

2. **Check Service Health:**
   - Your service URL will be: `https://plant-disease-classifier-backend.onrender.com`
   - Test the endpoint: `https://your-service-url.onrender.com/predict`

### Step 4: Test Your Deployed API

Use this curl command to test:
```bash
curl -X POST -F "image=@path/to/plant/image.jpg" https://your-service-url.onrender.com/predict
```

Or use Postman:
- Method: POST
- URL: `https://your-service-url.onrender.com/predict`
- Body: form-data with key "image" and your plant image file

## 📁 Required Files for Deployment

Make sure these files are in your repository:

✅ **app.py** - Main Flask application
✅ **requirements.txt** - Python dependencies
✅ **runtime.txt** - Python version (python-3.10.12)
✅ **render.yaml** - Render configuration (optional but recommended)
✅ **model/plant_disease_model.h5** - Your trained model
✅ **utils/predict.py** - Prediction logic
✅ **.gitignore** - Excludes .env and __pycache__

## 🔧 Configuration Files

### requirements.txt
```
Flask==3.1.1
tensorflow==2.18.0
numpy
pillow
python-dotenv
Flask-CORS
```

### runtime.txt
```
python-3.10.12
```

### render.yaml
```yaml
services:
  - type: web
    name: plant-disease-classifier-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python app.py"
    envVars:
      - key: PORT
        value: 10000
      - key: FLASK_DEBUG
        value: false
      - key: MODEL_PATH
        value: "model/plant_disease_model.h5"
```

## 🚨 Common Issues & Solutions

### Issue 1: Build Fails - Python Version
**Solution:** Ensure `runtime.txt` specifies `python-3.10.12`

### Issue 2: Model File Too Large
**Solution:** 
- Check if model file is under 500MB
- Consider using Git LFS for large files
- Or host model file externally and download during build

### Issue 3: Import Errors
**Solution:** 
- Verify all dependencies in `requirements.txt`
- Check file paths are relative, not absolute

### Issue 4: Port Issues
**Solution:** 
- Ensure app.py uses `PORT` environment variable
- Default to port 5000 for local development

### Issue 5: CORS Errors
**Solution:** 
- Update CORS configuration in app.py
- Allow your frontend domain in production

## 🔄 Updating Your Deployment

To update your deployed service:
1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push origin main
   ```
3. Render will automatically redeploy

## 📊 Monitoring

- **Logs:** Check Render dashboard for application logs
- **Metrics:** Monitor CPU, memory usage in Render dashboard
- **Health:** Set up health check endpoint if needed

## 💰 Pricing

- **Free Tier:** 750 hours/month, sleeps after 15 minutes of inactivity
- **Paid Tiers:** Always-on services, more resources available

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Python on Render](https://render.com/docs/python)
- [Environment Variables](https://render.com/docs/environment-variables)

## 📞 Support

If you encounter issues:
1. Check Render build logs
2. Review this deployment guide
3. Check Render's documentation
4. Contact Render support if needed