"""
Audio codec indicators for AI detection.
"""
from typing import Dict, Any
from .base_indicator import BaseIndicator


class CodecConsistencyIndicator(BaseIndicator):
    """Detects if audio codec matches the file format.
    
    Weight: 20 (BAJO) - Codec mismatches indicate anomalies.
    Verifies codec is correct for the file extension.
    """
    
    name = "codec_consistency"
    category = "codec"
    weight = 20
    description = "Codec incorrecto o inconsistente con el formato del archivo"
    risk_level = "low"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if codec matches the file format/extension.
        """
        file_format = metadata.get('file_format', '').lower()
        codec = metadata.get('ffprobe_streams_0_codec_name', '').lower()
        
        if not file_format or not codec:
            return {
                'detected': False,
                'confidence': 0.0,
                'details': {
                    'file_format': file_format,
                    'codec': codec,
                    'reason': 'Formato o codec no disponibles'
                },
                'reasoning': 'No se puede verificar consistencia sin información de formato/codec'
            }
        
        # Define expected codecs for each format
        format_codec_map = {
            'mp3': ['mp3', 'libmp3lame'],
            'wav': ['pcm_s16le', 'pcm_s24le', 'pcm_s32le', 'pcm_s8'],
            'm4a': ['aac'],
            'mp4': ['aac'],
            'flac': ['flac'],
            'ogg': ['vorbis', 'opus'],
            'opus': ['opus'],
            'aac': ['aac'],
        }
        
        # Get expected codecs for this format
        expected_codecs = format_codec_map.get(file_format.split('.')[-1] if '.' in file_format else file_format, [])
        
        # Check if codec matches
        detected = False
        if expected_codecs:
            detected = codec not in expected_codecs
        
        return {
            'detected': detected,
            'confidence': 0.8 if detected else 0.0,
            'details': {
                'file_format': file_format,
                'codec': codec,
                'expected_codecs': expected_codecs,
            },
            'reasoning_key': 'indicators.codec_consistency.reasoning_mismatch' if detected else 'indicators.codec_consistency.reasoning_ok'
        }
