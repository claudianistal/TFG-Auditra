"""
Service layer for file upload and forensic analysis operations.

This module contains the business logic for handling file uploads,
validation, and coordination with the forensic engine.
"""
from fastapi import UploadFile, HTTPException, status
from app.utils import validate_file, save_file, get_file_path, delete_file
from app.core.engine import ForensicEngine
from app.models import FileUploadResponse
from pathlib import Path


class FileUploadService:
    """
    Service for handling file uploads
    
    This class encapsulates the business logic for:
    - Validating uploaded files
    - Saving files to disk
    """
    
    def __init__(self, engine: ForensicEngine = None):
        """
        Initialize the FileUploadService.
        
        Args:
            engine (ForensicEngine, optional): Instance of ForensicEngine for analysis.
                                             If None, a new instance is created.
        """
        self.engine = engine or ForensicEngine()
    
    async def upload_file(self, file: UploadFile) -> FileUploadResponse:
        """
        Handle file upload, validation, and storage.
        
        This method:
        1. Validates the file (extension, size, format)
        2. Saves the file to disk with a unique ID
        3. Returns metadata about the uploaded file
        
        Args:
            file (UploadFile): The uploaded file from the frontend
            
        Returns:
            FileUploadResponse: Model containing file ID, filename, size, and status
            
        Raises:
            HTTPException: If validation fails (400) or save fails (500)
        """
        try:
            # 1. Validate file
            is_valid, error_msg = validate_file(file)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )
            
            # 2. Save file to disk
            file_id, file_size, original_filename = await save_file(file)
            
            # 3. Return response model (FastAPI serializes to JSON automatically)
            return FileUploadResponse(
                id=file_id,
                filename=original_filename,
                size=file_size,
                status="received"
            )
            
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar archivo: {str(e)}"
            )
    
    def delete_file(self, file_id: str, file_ext: str = None) -> bool:
        """
        Delete a file from the uploads directory.
        
        Args:
            file_id (str): The UUID of the file to delete
            file_ext (str, optional): File extension (e.g., '.wav')
            
        Returns:
            bool: True if deleted, False if not found
        """
        return delete_file(file_id, file_ext)
