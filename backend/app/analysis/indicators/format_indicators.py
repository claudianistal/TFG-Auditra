"""
File format indicators for AI detection.
"""
from typing import Dict, Any
from .base_indicator import BaseIndicator


class FormatMismatchIndicator(BaseIndicator):
    """Detects mismatch between file extension and actual content format."""
    
    name = "format_mismatch"
    category = "format"
    weight = 25
    description = "Desajuste entre extensión y formato real"
    risk_level = "high"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if file extension matches the actual format.
        Format mismatches are a red flag for manipulation.
        """
        file_extension = metadata.get('file_extension', '').lower().lstrip('.')
        detected_format = metadata.get('ffprobe_format_format_name', '').lower()
        
        # Normalize format names
        format_mapping = {
            'mp3': 'mp3',
            'wav': 'wav',
            'm4a': 'aac',
            'aac': 'aac',
            'flac': 'flac',
            'ogg': 'ogg',
            'opus': 'opus',
        }
        
        expected_format = format_mapping.get(file_extension, '')
        
        # Check if detected format contains expected format (lenient check)
        detected = expected_format and expected_format not in detected_format and \
                   file_extension not in detected_format
        
        return {
            'detected': detected,
            'confidence': 0.95 if detected else 0.0,
            'details': {
                'file_extension': file_extension,
                'detected_format': detected_format,
                'expected_format': expected_format
            },
            'reasoning': 'Desajuste de formato es indicador fuerte de manipulación de archivos'
        }


class SuspiciousFormatFlagIndicator(BaseIndicator):
    """Detects suspicious flags or metadata in format container."""
    
    name = "suspicious_format_flags"
    category = "format"
    weight = 8
    description = "Flags sospechosos en contenedor de formato"
    risk_level = "low"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check for suspicious flags in the format container.
        """
        # This would check for unusual flags or properties in the format structure
        # For now, a simple placeholder check
        detected = False
        
        return {
            'detected': detected,
            'confidence': 0.0,
            'details': {},
            'reasoning': 'Sin flags sospechosos detectados en contenedor'
        }
