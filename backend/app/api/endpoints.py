from fastapi import APIRouter, UploadFile, File
from app.services import FileUploadService
from app.models import FileUploadResponse
from app.core.engine import ForensicEngine

router = APIRouter()
engine = ForensicEngine()  # Instancia global del motor de análisis
file_service = FileUploadService(engine)  # Servicio de gestión de archivos


@router.post("/upload", response_model=FileUploadResponse)
async def upload_audio(file: UploadFile = File(...)):
    """
    Handle audio file upload.
    
    Receives an audio file (WAV, MP3, FLAC, AIFF), validates it,
    saves it to disk, and returns metadata with a unique file ID.
    
    Args:
        file (UploadFile): Audio file from the frontend
        
    Returns:
        FileUploadResponse: File ID, filename, size, and status
        
    Raises:
        HTTPException: 400 if validation fails, 500 if save fails
    """
    return await file_service.upload_file(file)