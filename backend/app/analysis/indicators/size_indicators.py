"""
File size indicators for AI detection.
"""
from typing import Dict, Any
from .base_indicator import BaseIndicator


class FileSizeIndicator(BaseIndicator):
    """Detects anomalies in file size based on bitrate and duration.
    
    Weight: Variable (bajo/medio/alto) - Depends on deviation from expected size.
    Uses formula: Expected size = (bitrate × duration_seconds) / 8
    
    Accounts for lossy vs lossless formats:
    - Lossy (MP3, AAC, Opus): allows ±15% deviation
    - Lossless (WAV, FLAC): allows ±5% deviation
    """
    
    name = "file_size"
    category = "size"
    weight = 30  # Default weight, can vary based on deviation
    description = "Anomalía en tamaño de archivo respecto a bitrate/duración"
    risk_level = "low"  # Default, can vary
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if file size matches expected size based on bitrate × duration.
        """
        try:
            file_size = int(metadata.get('file_size_bytes', 0))
            duration = float(metadata.get('ffprobe_format_duration', 0))
            bitrate = int(metadata.get('ffprobe_streams_0_bit_rate', 0))
            file_format = metadata.get('file_format', '').lower()
            
            if duration == 0 or bitrate == 0 or file_size == 0:
                return {
                    'detected': False,
                    'confidence': 0.0,
                    'details': {
                        'reason': 'Faltan datos: duración, bitrate o tamaño'
                    },
                    'reasoning_key': 'indicators.file_size.reasoning_error'
                }
            
            # Calculate expected size: (bitrate in bps × duration in seconds) / 8 bits per byte
            expected_size = (bitrate * duration) / 8
            
            # Determine deviation tolerance based on format
            # Lossy formats (MP3, AAC, Opus) typically have more variation
            lossy_formats = ['mp3', 'aac', 'm4a', 'opus', 'ogg']
            is_lossy = any(fmt in file_format for fmt in lossy_formats)
            
            # Set tolerance based on format
            if is_lossy:
                tolerance = 0.15  # ±15% for lossy formats
            else:
                tolerance = 0.05  # ±5% for lossless formats (WAV, FLAC)
            
            # Calculate deviation
            deviation = abs(file_size - expected_size) / expected_size if expected_size > 0 else 0
            deviation_percentage = deviation * 100
            
            # Determine if anomaly exists and severity
            detected = deviation > tolerance
            
            # Initialize variables
            risk_level = "low"
            weight = 0
            confidence = 0.0
            reasoning_key = 'indicators.file_size.reasoning_ok'
            
            if detected:
                if deviation_percentage > 30:
                    # Large deviation: HIGH risk
                    risk_level = "high"
                    weight = 50
                    confidence = min(deviation, 1.0)
                    reasoning_key = 'indicators.file_size.reasoning_high_deviation'
                elif deviation_percentage > 20:
                    # Medium deviation: MEDIUM risk
                    risk_level = "medium"
                    weight = 35
                    confidence = 0.7
                    reasoning_key = 'indicators.file_size.reasoning_medium_deviation'
                else:
                    # Small deviation: LOW risk
                    risk_level = "low"
                    weight = 20
                    confidence = 0.5
                    reasoning_key = 'indicators.file_size.reasoning_low_deviation'
            
            return {
                'detected': detected,
                'details': {
                    'file_size': file_size,
                    'expected_size': int(expected_size),
                    'bitrate': bitrate,
                    'duration_seconds': duration,
                    'format': file_format,
                    'is_lossy': is_lossy,
                    'deviation_percentage': round(deviation_percentage, 2),
                    'tolerance_percentage': tolerance * 100,
                },
                'reasoning_key': reasoning_key
            }
            
        except Exception as e:
            return {
                'detected': False,
                'confidence': 0.0,
                'details': {'error': str(e)},
                'reasoning_key': 'indicators.file_size.reasoning_error'
            }
