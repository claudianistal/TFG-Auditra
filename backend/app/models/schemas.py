"""
Pydantic models for request/response validation and documentation.

These models define the structure of data exchanged between frontend and backend.
"""
from pydantic import BaseModel, Field


class FileUploadResponse(BaseModel):
    """
    Response model for successful file upload.
    
    Attributes:
        id: Unique identifier (UUID) for the uploaded file
        filename: Original filename provided by the user
        size: File size in bytes
        status: Current status of the file (e.g., "received", "processing", "analyzed")
    """
    id: str = Field(..., description="Unique file identifier (UUID)")
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., ge=0, description="File size in bytes")
    status: str = Field(..., description="Current status of the file")
