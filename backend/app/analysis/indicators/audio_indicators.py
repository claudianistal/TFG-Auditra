"""
Audio channel indicators for AI detection.
"""
from typing import Dict, Any
from .base_indicator import BaseIndicator


class MonoAudioIndicator(BaseIndicator):
    """Detects mono audio which is uncommon in natural recordings.
    
    Weight: 40 (MEDIO) - Mono audio is often used in AI speech synthesis.
    """
    
    name = "mono_audio"
    category = "audio"
    weight = 40
    description = "Audio en mono detectado"
    risk_level = "medium"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if audio is mono. AI-generated speech is often mono.
        """
        channels = metadata.get('ffprobe_streams_0_channels', 0)
        detected = channels == 1
        
        return {
            'detected': detected,
            'details': {'channels': channels},
            'reasoning_key': 'indicators.mono_audio.reasoning'
        }
