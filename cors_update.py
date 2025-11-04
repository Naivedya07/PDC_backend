# After you get your frontend URL, update app.py CORS configuration:

# Replace the CORS section in backend/app.py with:
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:8000",  # Local development
            "https://your-frontend-url.onrender.com",  # Replace with actual URL
            "https://your-frontend-url.netlify.app",   # If using Netlify
            "https://your-frontend-url.vercel.app"     # If using Vercel
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})