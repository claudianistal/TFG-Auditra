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
    frontend_dist = Config.get_frontend_path()
    if frontend_dist.exists():
        app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
    else:
        print(f"Advertencia: No se encontró frontend en {frontend_dist}")
