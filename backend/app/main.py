import uvicorn
import webview
import threading
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints
from app.utils import ensure_upload_dir

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

# --- FASTAPI SERVER ---

def run_fastapi():
    # Ensure uploads directory exists before starting server
    ensure_upload_dir()
    # Launch FastAPI server on localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    # 1. Init FastAPI in a separate thread to keep the main thread free for the GUI
    t = threading.Thread(target=run_fastapi, daemon=True)
    t.start()

    # 2. Determinate the frontend URL (Vite dev server is running on port 5173)
    frontend_url = "http://localhost:5173"
    
    # 3. Create the webview window pointing to the frontend
    webview.create_window(
        'TFG: Analizador Forense de Audio IA', 
        frontend_url,
        width=1200,
        height=800,
        resizable=True
    )

    webview.start()