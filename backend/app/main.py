import uvicorn
import webview
import threading
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- CONFIGURACIÓN DE LA APP ---
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

# --- LÓGICA PARA ENCONTRAR LOS ARCHIVOS ---
"""
    # Obtiene la ruta absoluta para PyInstaller o para desarrollo normal
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    # 1. Definimos dónde está la carpeta dist (relativa a este archivo main.py)
    path_to_dist = get_resource_path(os.path.join("frontend", "dist"))
    # 2. Si la carpeta existe, le decimos a FastAPI que la sirva
    if os.path.exists(path_to_dist):
        app.mount("/", StaticFiles(directory=path_to_dist, html=True), name="static")
"""


# --- LÓGICA DE EJECUCIÓN ---

def run_fastapi():
    # Lanzamos el backend en el puerto 8000
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    # 1. Arrancar FastAPI en un hilo secundario para que no bloquee la interfaz
    t = threading.Thread(target=run_fastapi, daemon=True)
    t.start()

    # 2. Determinar la URL del Frontend (en desarrollo o producción)
    frontend_url = "http://localhost:5173" 

    # 3. Lanzar la ventana de escritorio (PyWebView)
    webview.create_window(
        'TFG: Analizador Forense de Audio IA', 
        frontend_url,
        width=1200,
        height=800,
        resizable=True
    )
    webview.start()