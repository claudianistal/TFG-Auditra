"""
Pydantic models for request/response validation and documentation.

These models define the structure of data exchanged between frontend and backend.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


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


class IndicatorDetail(BaseModel):
    """Details of a single indicator result."""
    name: str = Field(..., description="Unique indicator identifier")
    display_name: str = Field(..., description="Human-readable indicator name")
    category: str = Field(..., description="Indicator category")
    weight: int = Field(..., description="Weight in scoring")
    detected: bool = Field(..., description="Whether indicator was detected")
    risk_level: str = Field(..., description="low, medium, or high")
    reasoning_key: str = Field(..., description="i18n translation key for indicator reasoning")
    details: Dict[str, Any] = Field(..., description="Additional technical details")


class AnalysisResponse(BaseModel):
    """
    Complete analysis response for AI detection.
    """
    file_id: str = Field(..., description="Unique file identifier")
    filename: str = Field(..., description="Original filename")
    risk_score: int = Field(..., ge=0, le=100, description="Overall risk score 0-100")
    likelihood: str = Field(..., description="bajo, medio, or alto")
    likelihood_description: str = Field(..., description="Human-readable likelihood description")
    score_color: str = Field(..., description="green, yellow, or red")
    detected_factors: List[IndicatorDetail] = Field(..., description="Detected indicators")
    missing_factors: List[IndicatorDetail] = Field(..., description="Non-detected indicators")
    all_indicators: List[IndicatorDetail] = Field(..., description="All indicator results")
    conclusion_key: str = Field(..., description="i18n translation key for conclusion")
    recommendations: List[str] = Field(..., description="Actionable recommendations (i18n keys)")
    analysis_date: str = Field(..., description="ISO timestamp of analysis")
