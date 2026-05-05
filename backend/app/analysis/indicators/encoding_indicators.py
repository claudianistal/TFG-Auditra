"""
Encoding library indicators for AI detection.
"""
from typing import Dict, Any
from .base_indicator import BaseIndicator


class EncodingLibraryIndicator(BaseIndicator):
    """Detects suspicious encoding libraries (Lavf/FFmpeg) fingerprints in metadata.
    
    Weight: 90 (ALTO) - Strongly indicates AI-generated audio.
    """
    
    name = "encoding_library"
    category = "encoding"
    weight = 90
    description = "Librería de codificación sospechosa detectada (Lavf/FFmpeg)"
    risk_level = "high"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if suspicious encoding libraries are detected in metadata.
        Lavf/FFmpeg is commonly used in AI audio generation tools.
        """
        # Specific encoder field labels to check (in order)
        encoder_fields_map = {
            'Exif:Encoding Library': metadata.get('Exif:Encoding Library', ''),
            'Ffprobe_format_encoder': metadata.get('Ffprobe_format_encoder', ''),
            'stream_encoder': metadata.get('stream_encoder', ''),
            'ID3 TSSE': metadata.get('ID3 TSSE', ''),
            'Exif:ID3:EncoderSettings': metadata.get('Exif:ID3:EncoderSettings', ''),
            'Ffprobe Format Tags': metadata.get('Ffprobe Format Tags', ''),
            'encoder': metadata.get('encoder', ''),
            'format_encoder': metadata.get('format_encoder', ''),
            'encoding_library': metadata.get('encoding_library', ''),
        }
        
        # Check for suspicious encoding libraries
        ai_libraries = ['lavf', 'ffmpeg', 'libav']
        detected = False
        detected_fields = []  # List of all fields where detected
        
        # Check ALL specific encoder fields
        for field_name, field_value in encoder_fields_map.items():
            if field_value:
                field_lower = str(field_value).lower()
                for lib in ai_libraries:
                    if lib in field_lower:
                        detected = True
                        detected_fields.append({
                            'field': field_name,
                            'value': str(field_value)
                        })
                        break  # Move to next field after finding a library
        
        # If not found in specific fields, search in all metadata
        if not detected:
            for key, value in metadata.items():
                if isinstance(value, (str, dict)):
                    value_lower = str(value).lower()
                    for lib in ai_libraries:
                        if lib in value_lower:
                            detected = True
                            detected_fields.append({
                                'field': key,
                                'value': str(value)
                            })
                            break  # Move to next field after finding a library
        
        return {
            'detected': detected,
            'details': {
                'detected_fields': detected_fields if detected else [],
                'libraries_checked': ai_libraries,
            },
            'reasoning_key': 'indicators.encoding_library.reasoning'
        }
