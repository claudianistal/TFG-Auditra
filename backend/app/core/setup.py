"""
Setup module for configuring FastAPI application components.

Handles frontend static files mounting and other initialization tasks.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import Config


def setup_frontend(app: FastAPI) -> None:
    """
    Configure frontend static files mounting.
    
    Mounts the compiled frontend files to the root path when in production mode.
    In development mode, the frontend is served separately by Vite.
    
    Args:
        app: FastAPI application instance
    """
    # Only mount static files in production mode, in development the frontend is served by Vite
    if Config.is_production():
        frontend_dist = Config.get_frontend_path()
        if frontend_dist.exists():
            app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
        else:
            print(f"Advertencia: No se encontró frontend empaquetado en {frontend_dist}")
    else:
        # In development mode, the frontend is served by Vite on a separate port, so we don't mount static files here
        print(f"Modo Desarrollo: Frontend gestionado externamente por Vite en {Config.FRONTEND_DEV_URL}")
