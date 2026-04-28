"""
Service layer for file upload and forensic analysis operations.

This module contains the business logic for handling file uploads,
validation, and extraction of file metadata and patterns.
"""
from fastapi import UploadFile, HTTPException, status
from app.utils import validate_file, save_file, get_file_path, delete_file
from app.models import FileUploadResponse
from pathlib import Path
from datetime import datetime
import base64

from app.metadata import MetadataFactory
from app.patterns import PatternAnalyzer


class FileUploadService:
    """
    Service for handling file uploads and analysis.
    
    This class encapsulates the business logic for:
    - Validating uploaded files
    - Saving files to disk
    - Extracting metadata
    - Analyzing binary patterns
    """
    
    def __init__(self):
        """Initialize the FileUploadService."""
        pass
    
    async def upload_file(self, file: UploadFile) -> FileUploadResponse:
        """
        Handle file upload, validation, and storage.
        
        This method:
        1. Validates the file (extension, size, format)
        2. Saves the file to disk with a unique ID
        3. Calculates the SHA-256 hash for verification
        4. Returns metadata about the uploaded file
        
        Args:
            file (UploadFile): The uploaded file from the frontend
            
        Returns:
            FileUploadResponse: Model containing file ID, filename, size, hash, and status
            
        Raises:
            HTTPException: If validation fails (400) or save fails (500)
        """
        try:
            # 1. Validate file extension (before reading)
            original_filename = file.filename or ""
            is_valid, error_msg = validate_file(original_filename)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )
            
            # 2. Save file to disk and calculate hash (includes full validation)
            file_id, file_size, original_filename, file_hash = await save_file(file)
            
            # 3. Return response model with hash
            return FileUploadResponse(
                id=file_id,
                filename=original_filename,
                size=file_size,
                hash=file_hash,
                hash_algorithm="SHA-256",
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
    
    def get_file_metadata(self, file_id: str) -> dict:
        """
        Extract raw forensic metadata from an uploaded file using the MetadataFactory.
        """
        try:
            # 1. Locate the file
            file_path = get_file_path(file_id)
            
            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"File with ID {file_id} not found"
                )
            
            # 2. Get the appropriate extractor via Factory
            # The factory handles the logic of which format to use
            extractor = MetadataFactory.get_extractor(str(file_path))
            
            # 3. Extract all metadata (including raw/null values for forensic value)
            metadata = extractor.get_all_metadata()
            
            # 4. Return structured response
            return {
                "file_id": file_id,
                "filename": file_path.name,
                "metadata": metadata,
                "extracted_at": datetime.utcnow().isoformat() + "Z"
            }
            
        except HTTPException:
            raise
        except ValueError as e:
            # Catch unsupported format errors from the Factory
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during forensic metadata extraction: {str(e)}"
            )
    
    def get_patterns(self, file_id: str, width: int = 512) -> dict:
        """
        Analyze file patterns: generate bitmap visualization and hex dumps.
        
        Args:
            file_id (str): The UUID of the file to analyze
            width (int): Width of bitmap in bytes
            
        Returns:
            dict: Bitmap as base64 PNG + formatted hex dumps
            
        Raises:
            HTTPException: If file not found or analysis fails
        """
        try:
            # 1. Locate the file
            file_path = get_file_path(file_id)
            
            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"File with ID {file_id} not found"
                )
            
            # 2. Generate bitmap
            png_bytes = PatternAnalyzer.generate_bitmap(str(file_path), width=width)
            image_base64 = base64.b64encode(png_bytes).decode('utf-8')
            
            # 3. Extract hex dumps
            hex_data = PatternAnalyzer.extract_hex_dumps(str(file_path), num_bytes=1024)
            
            # 4. Return structured response
            return {
                "file_id": file_id,
                "filename": file_path.name,
                "image_base64": image_base64,
                "hex_start": hex_data["hex_start"],
                "hex_end": hex_data["hex_end"],
                "total_file_size": hex_data["total_file_size"],
                "width_used": width,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
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
                detail=f"Error analyzing patterns: {str(e)}"
            )
    
    def get_autosimilarity(self, file_id: str, width: int = 512) -> dict:
        """
        Generate only the bitmap visualization (autosimilarity analysis).
        
        Args:
            file_id (str): The UUID of the file to analyze
            width (int): Width of bitmap in bytes
            
        Returns:
            dict: Bitmap as base64 PNG
            
        Raises:
            HTTPException: If file not found or analysis fails
        """
        try:
            # 1. Locate the file
            file_path = get_file_path(file_id)
            
            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"File with ID {file_id} not found"
                )
            
            # 2. Generate bitmap only
            png_bytes = PatternAnalyzer.generate_bitmap(str(file_path), width=width)
            image_base64 = base64.b64encode(png_bytes).decode('utf-8')
            
            # 3. Return structured response
            return {
                "file_id": file_id,
                "filename": file_path.name,
                "image_base64": image_base64,
                "width_used": width,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
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
                detail=f"Error analyzing autosimilarity: {str(e)}"
            )
    
    def get_padding(self, file_id: str) -> dict:
        """
        Extract only the hex dumps (padding detection analysis).
        
        Args:
            file_id (str): The UUID of the file to analyze
            
        Returns:
            dict: Hex dumps from start and end of file
            
        Raises:
            HTTPException: If file not found or analysis fails
        """
        try:
            # 1. Locate the file
            file_path = get_file_path(file_id)
            
            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"File with ID {file_id} not found"
                )
            
            # 2. Extract hex dumps only
            hex_data = PatternAnalyzer.extract_hex_dumps(str(file_path), num_bytes=1024)
            
            # 3. Return structured response
            return {
                "file_id": file_id,
                "filename": file_path.name,
                "hex_start": hex_data["hex_start"],
                "hex_end": hex_data["hex_end"],
                "full_hex": hex_data["full_hex"],
                "total_file_size": hex_data["total_file_size"],
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error analyzing padding: {str(e)}"
            )
