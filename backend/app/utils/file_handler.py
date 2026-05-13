"""File handling utilities for audio file uploads."""
import uuid
import os
import sys
import hashlib
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile

# Configuración de formatos y tamaños
ALLOWED_EXTENSIONS = {'.wav', '.mp3', '.m4a'}
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB en bytes


def get_upload_dir() -> Path:
    """
    Get the upload directory path. Uses Documents folder for easy access.
    Compatible with PyInstaller and all Python distributions.
    
    Returns:
        Path: Path to the uploads directory
    """
    home = Path.home()
    
    posibles_rutas = [
        home / 'Documentos',                 
        home / 'Documents',                  
        home / 'OneDrive' / 'Documents',     
        home / 'OneDrive' / 'Documentos',
    ]
    
    base_dir = home # Final fallback: (C:\Users\Name)
    
    for ruta in posibles_rutas:
        if ruta.exists():
            base_dir = ruta
            break
            
    uploads_dir = base_dir / 'TFG_Auditra_Uploads'
    
    return uploads_dir


def ensure_upload_dir() -> Path:
    """
    Ensure that the uploads directory exists.
    Creates it if it doesn't exist.
    
    Returns:
        Path: Path to the uploads directory
    """
    upload_dir = get_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def validate_file(filename: str, file_size: int = None) -> Tuple[bool, str]:
    """
    Validate the uploaded file (extension and optionally size).
    
    Args:
        filename (str): The name of the file
        file_size (int, optional): Size of the file in bytes. If provided, size is validated.
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Validar extensión
    file_ext = Path(filename).suffix.lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(ALLOWED_EXTENSIONS)
        return False, f"Formato no soportado. Formatos permitidos: {allowed}"
    
    # Validar tamaño si se proporciona
    if file_size is not None and file_size > MAX_FILE_SIZE:
        size_gb = file_size / (1024 * 1024 * 1024)
        max_gb = MAX_FILE_SIZE / (1024 * 1024 * 1024)
        return False, f"Archivo demasiado grande ({size_gb:.2f}GB). Máximo permitido: {max_gb:.2f}GB"
    
    return True, ""


def calculate_file_hash(file_content: bytes, algorithm: str = 'sha256') -> str:
    """
    Calculate the hash of file content.
    
    Args:
        file_content (bytes): The content of the file to hash
        algorithm (str): Hash algorithm to use (default: sha256)
        
    Returns:
        str: Hexadecimal hash string
    """
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(file_content)
    return hash_obj.hexdigest()


async def save_file(file: UploadFile) -> Tuple[str, int, str, str]:
    """
    Save the uploaded file to disk and calculate its hash.
    
    Args:
        file (UploadFile): The file to save
        
    Returns:
        Tuple[str, int, str, str]: (file_id, file_size, original_filename, file_hash)
        
    Raises:
        ValueError: If file is too large or cannot be saved
    """
    # Generar ID único
    file_id = str(uuid.uuid4())
    
    # Obtener extensión
    original_filename = file.filename or "audio"
    file_ext = Path(original_filename).suffix.lower()
    
    # Ruta donde guardar
    upload_dir = ensure_upload_dir()
    file_path = upload_dir / f"{file_id}{file_ext}"
    
    # Asegurarse de que la ruta es absoluta
    file_path = file_path.resolve()
    
    # Leer y guardar archivo
    file_size = 0
    file_hash = ""
    try:
        # Leer contenido del archivo
        content = await file.read()
        file_size = len(content)
        
        # Validar tamaño (y extensión como double-check)
        original_filename = file.filename or "audio"
        is_valid, error_msg = validate_file(original_filename, file_size)
        if not is_valid:
            raise ValueError(error_msg)
        
        # Calcular hash del archivo
        file_hash = calculate_file_hash(content, 'sha256')
        
        # Guardar contenido en disco
        with open(file_path, 'wb') as f:
            f.write(content)
            
    except ValueError as ve:
        raise
    except Exception as e:
        raise ValueError(f"Error al guardar archivo: {str(e)}")
    
    return file_id, file_size, original_filename, file_hash


def delete_file(file_id: str, file_ext: str = None) -> bool:
    """
    Delete a file from the uploads directory.
    
    Args:
        file_id (str): The UUID of the file
        file_ext (str, optional): The file extension (e.g., '.wav'). 
                                 If not provided, will search for any extension.
    
    Returns:
        bool: True if deleted, False if not found
    """
    upload_dir = get_upload_dir()
    
    if file_ext:
        file_path = upload_dir / f"{file_id}{file_ext}"
        if file_path.exists():
            file_path.unlink()
            return True
    else:
        # Search for file with any extension
        for ext in ALLOWED_EXTENSIONS:
            file_path = upload_dir / f"{file_id}{ext}"
            if file_path.exists():
                file_path.unlink()
                return True
    
    return False


def get_file_path(file_id: str, file_ext: str = None) -> Path:
    """
    Get the full path to a file in the uploads directory.
    
    Args:
        file_id (str): The UUID of the file
        file_ext (str, optional): The file extension (e.g., '.wav')
    
    Returns:
        Path: Full path to the file (may or may not exist)
    """
    upload_dir = get_upload_dir()
    
    if file_ext:
        return upload_dir / f"{file_id}{file_ext}"
    else:
        # Search for file with any extension
        for ext in ALLOWED_EXTENSIONS:
            file_path = upload_dir / f"{file_id}{ext}"
            if file_path.exists():
                return file_path
        return upload_dir / f"{file_id}"  # Return default if not found

def get_binary_path(binary_name: str) -> str:
    """
    Get the absolute path to a binary tool (e.g., exiftool.exe, ffprobe.exe).
    Works in both development mode and PyInstaller frozen mode.
    
    Args:
        binary_name (str): The name of the binary
        
    Returns:
        str: Absolute path to the binary
    """
    if getattr(sys, 'frozen', False):
        # Si estamos ejecutando desde el .exe generado por PyInstaller
        base_path = Path(sys._MEIPASS)
    else:
        # En modo desarrollo, la carpeta bin está en backend/bin
        # __file__ es backend/app/utils/file_handler.py
        base_path = Path(__file__).parent.parent.parent

    bin_path = base_path / 'bin' / binary_name
    return str(bin_path.resolve())

