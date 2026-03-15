from fastapi import APIRouter, UploadFile, File, HTTPException, status
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


@router.delete("/upload/{file_id}")
async def delete_audio(file_id: str):
    """
    Delete an uploaded audio file.
    
    Removes the file from the uploads directory by its unique ID.
    Called when user removes a file from the processing queue.
    
    Args:
        file_id (str): The UUID of the file to delete
        
    Returns:
        dict: {"success": True, "message": "File deleted"}
        
    Raises:
        HTTPException: 404 if file not found, 500 if delete fails
    """
    try:
        deleted = file_service.delete_file(file_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File with ID {file_id} not found"
            )
        return {"success": True, "message": "File deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}"
        )
