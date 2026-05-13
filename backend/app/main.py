import uvicorn
import webview
import threading
import time
import socket
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

app.include_router(endpoints.router, prefix="/api")
setup_frontend(app)

# --- NETWORK UTILS ---

def find_free_port(start_port=8000, max_port=8050):
    """Search for a free port starting from start_port up to max_port."""
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                # If the bind is successful, the port is free
                s.bind((Config.BACKEND_HOST, port))
                return port
            except OSError:
                # If bind fails, the port is in use, so we try the next one
                continue
    raise RuntimeError(f"No free ports found between {start_port} and {max_port}")

def wait_for_server(port, timeout=10):
    """Wait actively for the FastAPI server to respond on the specified port."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Try to connect to the port
            with socket.create_connection((Config.BACKEND_HOST, port), timeout=1):
                return True
        except OSError:
            # If it fails, wait half a second and try again
            time.sleep(0.5)
    return False

# --- FASTAPI SERVER ---

def run_fastapi(port):
    """Start FastAPI server dynamically on the assigned port"""
    ensure_upload_dir()
    uvicorn.run(
        app, 
        host=Config.BACKEND_HOST, 
        port=port, 
        log_level="info"
    )

if __name__ == "__main__":
    # 1. Find a free port for FastAPI to run on
    active_port = find_free_port(Config.BACKEND_PORT, Config.BACKEND_PORT + 50)
    
    # Update the Config with the active port so that other parts of the app can reference it
    Config.BACKEND_PORT = active_port 

    # 2. Initiate FastAPI in a separate thread to keep the main thread responsive for WebView
    t = threading.Thread(target=run_fastapi, args=(active_port,), daemon=True)
    t.start()
    
    # 3. Wait for FastAPI to start correctly
    if wait_for_server(active_port):
        print(f"Servidor iniciado correctamente en el puerto {active_port}")
        
        # 4. Obtain the frontend URL using the active port and create the WebView window
        frontend_url = Config.get_frontend_url()
        
        window =webview.create_window("AUDITRA", frontend_url)
        webview.start(lambda: window.maximize())
    else:
        # If the server fails to start within the timeout, log an error and exit
        print("Error crítico: El servidor backend no pudo arrancar a tiempo.")
        import sys
        sys.exit(1)