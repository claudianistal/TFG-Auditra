from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services import FileUploadService
from app.models import FileUploadResponse

router = APIRouter()
file_service = FileUploadService()  # Servicio de gestión de archivos


@router.post("/upload", response_model=FileUploadResponse)
async def upload_audio(file: UploadFile = File(...)):
    """
    Handle audio file upload.
    
    Receives an audio file (WAV, MP3, M4A), validates it,
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


@router.get("/metadata/{file_id}")
async def get_metadata(file_id: str):
    """
    Extract and return metadata from an uploaded audio file.
    
    Analyzes the audio file and extracts all available metadata
    including title, artist, album, genre, duration, bitrate, etc.
    
    Args:
        file_id (str): The UUID of the file to analyze
        
    Returns:
        dict: {
            "file_id": str,
            "filename": str,
            "metadata": {
                ... (all extracted metadata fields)
            },
            "extracted_at": ISO 8601 timestamp
        }
        
    Raises:
        HTTPException: 404 if file not found, 400 if unsupported format, 500 on errors
    """
    return file_service.get_file_metadata(file_id)


@router.get("/patterns/{file_id}")
async def get_patterns(file_id: str, width: int = 512):
    """
    Analyze and return pattern visualizations from an audio file.
    
    Generates a bitmap visualization of file contents (autosimilitude)
    and extracts hex dumps from file start/end for padding detection.
    
    Args:
        file_id (str): The UUID of the file to analyze
        width (int): Width of bitmap in bytes (default 512, range: 128-2048)
        
    Returns:
        dict: {
            "file_id": str,
            "filename": str,
            "image_base64": base64-encoded PNG image,
            "hex_start": [list of formatted hex dump lines],
            "hex_end": [list of formatted hex dump lines],
            "total_file_size": int,
            "width_used": int,
            "generated_at": ISO 8601 timestamp
        }
        
    Raises:
        HTTPException: 404 if file not found, 400 if validation fails, 500 on errors
    """
    # Validate width parameter
    if width < 128 or width > 2048:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Width must be between 128 and 2048 bytes"
        )
    
    return file_service.get_patterns(file_id, width)
