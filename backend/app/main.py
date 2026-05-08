import uvicorn
import webview
import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints
from app.utils import ensure_upload_dir
from app.core.config import Config
from app.core.setup import setup_frontend

# --- APP CONFIGURATION ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(endpoints.router, prefix="/api")

# Configure frontend static files
setup_frontend(app)

# --- FASTAPI SERVER ---

def run_fastapi():
    """Start FastAPI server with proper configuration"""
    ensure_upload_dir()
    uvicorn.run(
        app, 
        host=Config.BACKEND_HOST, 
        port=Config.BACKEND_PORT, 
        log_level="info"
    )

if __name__ == "__main__":
    # 1. Init FastAPI in a separate thread to keep the main thread free for the GUI
    t = threading.Thread(target=run_fastapi, daemon=True)
    t.start()
    
    # 2. Wait for FastAPI to start
    time.sleep(2)
    
    # 3. Get frontend URL based on environment
    frontend_url = Config.get_frontend_url()
    
    print(f"Abriendo webview: {frontend_url}")
    
    # 4. Create the webview window pointing to the frontend
    window = webview.create_window(
        'AUDITRA', 
        frontend_url,
        width=1200,
        height=800,
        resizable=True
    )

    webview.start(lambda: window.maximize())