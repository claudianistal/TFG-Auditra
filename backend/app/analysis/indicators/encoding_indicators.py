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
        # Collect all metadata values to search
        all_values = []
        
        # Add specific encoder fields
        encoder_fields = [
            metadata.get('Exif:Encoding Library', ''),
            metadata.get('Ffprobe_format_encoder', ''),
            metadata.get('stream_encoder', ''),
            metadata.get('ID3 TSSE', ''),
            metadata.get('Exif:ID3:EncoderSettings', ''),
            metadata.get('Ffprobe Format Tags', ''),
            metadata.get('encoder', ''),
            metadata.get('format_encoder', ''),
            metadata.get('encoding_library', ''),
        ]
        
        all_values.extend([str(f) for f in encoder_fields if f])
        
        # Search in ALL metadata values
        for key, value in metadata.items():
            if isinstance(value, (str, dict)):
                all_values.append(str(value).lower())
        
        # Join all values into searchable string
        encoder_info = ' '.join(all_values).lower()
        
        # Check for suspicious encoding libraries
        ai_libraries = ['lavf', 'ffmpeg', 'libav']
        detected = any(lib in encoder_info for lib in ai_libraries)
        
        return {
            'detected': detected,
            'confidence': 0.95 if detected else 0.0,
            'details': {
                'encoder_found': encoder_info[:200],
                'libraries_checked': ai_libraries,
            },
            'reasoning_key': 'indicators.encoding_library.reasoning'
        }
