"""
Pydantic models for request/response validation and documentation.

These models define the structure of data exchanged between frontend and backend.
"""
from pydantic import BaseModel, Field
from typing import Optional


class FileUploadResponse(BaseModel):
    """
    Response model for successful file upload.
    
    Attributes:
        id: Unique identifier (UUID) for the uploaded file
        filename: Original filename provided by the user
        size: File size in bytes
        status: Current status of the file (e.g., "received", "processing", "analyzed")
        hash: SHA-256 hash of the original file
        hash_algorithm: Algorithm used to calculate the hash
    """
    id: str = Field(..., description="Unique file identifier (UUID)")
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., ge=0, description="File size in bytes")
    status: str = Field(..., description="Current status of the file")
    hash: str = Field(..., description="SHA-256 hash of the original file")
    hash_algorithm: str = Field(default="SHA-256", description="Hash algorithm used")
