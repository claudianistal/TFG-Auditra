import uvicorn
import webview
import threading
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- APP CONFIGURATION ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/analizar")
async def analizar_audio():
    return {
        "archivo": "evidencia_001.wav",
        "resultado": "Sintético (IA)",
        "probabilidad": 0.94,
        "metadatos": {
            "encoder": "ElevenLabs",
            "bitrate": "128kbps",
            "hash_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
    }

# --- FASTAPI SERVER ---

def run_fastapi():
    # Lauch FastAPI server on localhost:8000
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