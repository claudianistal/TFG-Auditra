from typing import Dict, Any
from .base_indicator import BaseIndicator

class AtypicalBitrateIndicator(BaseIndicator):
    """
    Detects unusually low or atypical bitrates commonly used by AI and TTS APIs.
    Cloud-based generation models often compress output audio to very low bitrates 
    (e.g., 24 kbps, 32 kbps, 48 kbps) to save server bandwidth and reduce latency.
    This indicator dynamically adjusts its threshold based on whether the audio 
    container is lossy (MP3/M4A) or lossless (WAV).
    """
    
    name = "atypical_bitrate"
    category = "encoding"
    weight = 15 
    description = "Tasa de bits (Bitrate) anormalmente baja o atípica"
    risk_level = "low"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        # Extract the bit rate from ffprobe metadata (in bits per second)
        bitrate_str = metadata.get('ffprobe_streams_0_bit_rate', '0')
        
        # Extract the file format to determine compression type
        file_format = metadata.get('ffprobe_format_format_name', '').lower()
        print(file_format)
        
        try:
            bitrate = int(bitrate_str)
        except ValueError:
            return {
                'detected': False, 
                'details': {}, 
                'reasoning_key': 'indicators.atypical_bitrate.error'
            }

        if bitrate <= 0:
            return {
                'detected': False, 
                'details': {}, 
                'reasoning_key': 'indicators.atypical_bitrate.no_data'
            }

        # Convert to kilobits per second (kbps) for easier evaluation
        kbps = bitrate / 1000
        
        # Determine if the format relies on lossy compression
        is_lossy = any(fmt in file_format for fmt in ['mp3', 'm4a'])
        
        # Apply dynamic thresholds based on the encoding format
        if is_lossy:
            # MP3/M4A: < 48 kbps is a strong indicator of TTS voice synthesis 
            # designed to minimize payload size over network APIs.
            is_suspicious = 0 < kbps <= 48
            threshold = 48
        else:
            # WAV (PCM): An uncompressed 16kHz Mono file yields exactly 256 kbps.
            # If a WAV is under 300 kbps, it strongly implies a low sample rate 
            # typical of baseline AI models. (Standard CD-quality WAV is ~1411 kbps).
            is_suspicious = 0 < kbps <= 300
            threshold = 300
        
        return {
            'detected': is_suspicious,
            'details': {
                'format_type': 'lossy' if is_lossy else 'lossless',
                'bitrate_kbps': round(kbps, 2),
                'threshold_kbps': threshold
            },
            'reasoning_key': 'indicators.atypical_bitrate.reasoning' if is_suspicious else 'indicators.ok'
        }