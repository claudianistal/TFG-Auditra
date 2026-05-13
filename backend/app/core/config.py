"""
Configuration module for TFG-Auditra application.

Handles environment detection and path resolution for both
development and production (PyInstaller) environments.
"""
import sys
from pathlib import Path


class Config:
    """Application configuration"""
    
    # Server configuration
    BACKEND_HOST = "127.0.0.1"
    BACKEND_PORT = 8000
    FRONTEND_DEV_PORT = 5173
    FRONTEND_DEV_URL = f"http://localhost:{FRONTEND_DEV_PORT}"
    
    @staticmethod
    def get_base_path() -> Path:
        """
        Get base application path.
        
        Returns:
            Path: Base path of the application
                - In PyInstaller .exe: sys._MEIPASS
                - In development: project root
        """
        if getattr(sys, 'frozen', False):
            return Path(sys._MEIPASS)
        else:
            # Up 4 levels: config.py -> core -> app -> backend -> RAÍZ
            return Path(__file__).resolve().parent.parent.parent.parent
    
    @staticmethod
    def get_frontend_path() -> Path:
        """Get path to the compiled frontend directory"""
        return Config.get_base_path() / "frontend" / "dist"
    
    @staticmethod
    def is_production() -> bool:
        """Check if running as compiled .exe"""
        return getattr(sys, 'frozen', False)
    
    @staticmethod
    def get_frontend_url() -> str:
        """Get frontend URL based on environment"""
        if Config.is_production():
            # In production, the frontend is served by FastAPI, so we use the backend URL
            return f"http://{Config.BACKEND_HOST}:{Config.BACKEND_PORT}"
        else:
            # Uses Vite dev server URL in development
            return Config.FRONTEND_DEV_URL
