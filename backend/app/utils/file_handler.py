"""
File handling utilities for audio file uploads.
"""
import uuid
import os
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile

# Configuración de formatos y tamaños
ALLOWED_EXTENSIONS = {'.wav', '.mp3', '.flac', '.aiff'}
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB en bytes
UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"


def ensure_upload_dir() -> Path:
    """
    Ensure that the uploads directory exists.
    Creates it if it doesn't exist.
    
    Returns:
        Path: Path to the uploads directory
    """
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return UPLOAD_DIR


def validate_file(file: UploadFile) -> Tuple[bool, str]:
    """
    Validate the uploaded file.
    
    Args:
        file (UploadFile): The file to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Validar extensión
    filename = file.filename or ""
    file_ext = Path(filename).suffix.lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(ALLOWED_EXTENSIONS)
        return False, f"Formato no soportado. Formatos permitidos: {allowed}"
    
    # Validar tamaño (se valida al leer el contenido)
    # Aquí solo checkeamos si el archivo es demasiado grande
    # FastAPI no proporciona tamaño antes de lectura, así que lo verificaremos al guardar
    
    return True, ""


async def save_file(file: UploadFile) -> Tuple[str, int, str]:
    """
    Save the uploaded file to disk.
    
    Args:
        file (UploadFile): The file to save
        
    Returns:
        Tuple[str, int, str]: (file_id, file_size, filename)
        
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
    
    # Leer y guardar arquivo
    file_size = 0
    try:
        # Leer contenido del archivo (chequear tamaño durante lectura)
        content = await file.read()
        file_size = len(content)
        
        # Validar tamaño
        if file_size > MAX_FILE_SIZE:
            size_gb = file_size / (1024 * 1024 * 1024)
            max_gb = MAX_FILE_SIZE / (1024 * 1024 * 1024)
            raise ValueError(
                f"Archivo demasiado grande ({size_gb:.2f}GB). "
                f"Máximo permitido: {max_gb:.2f}GB"
            )
        
        # Guardar contenido en disco
        with open(file_path, 'wb') as f:
            f.write(content)
            
    except ValueError:
        # Re-raise validation errors
        raise
    except Exception as e:
        raise ValueError(f"Error al guardar archivo: {str(e)}")
    
    return file_id, file_size, original_filename


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
    upload_dir = ensure_upload_dir()
    
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
    upload_dir = ensure_upload_dir()
    
    if file_ext:
        return upload_dir / f"{file_id}{file_ext}"
    else:
        # Search for file with any extension
        for ext in ALLOWED_EXTENSIONS:
            file_path = upload_dir / f"{file_id}{ext}"
            if file_path.exists():
                return file_path
        return upload_dir / f"{file_id}"  # Return default if not found
