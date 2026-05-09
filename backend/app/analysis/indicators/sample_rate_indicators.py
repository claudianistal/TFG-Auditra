from typing import Dict, Any
from .base_indicator import BaseIndicator

class SampleRateIndicator(BaseIndicator):
    """
    Detects sample rates typically used by IA models.
    AI models often export audio at 16kHz or 24kHz to optimize resources, 
    whereas commercial or physically recorded audio uses 44.1kHz or 48kHz.
    """
    
    name = "sample_rate_anomaly"
    category = "audio"
    weight = 25
    description = "Anomalía en tasa de muestreo (Sample Rate)"
    risk_level = "medium"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        # Extract the sample rate from ffprobe metadata
        sample_rate_str = metadata.get('ffprobe_streams_0_sample_rate', '0')
        
        try:
            sample_rate = int(sample_rate_str)
        except ValueError:
            return {
                'detected': False, 
                'details': {}, 
                'reasoning_key': 'indicators.sample_rate.error'
            }

        # 16000 Hz, 22050 Hz, and 24000 Hz are very common in raw AI (TTS) outputs.
        # 32000 Hz and 40000 Hz are the standard outputs for RVC (Voice Cloning) vocoders.
        ai_sample_rates = [16000, 22050, 24000, 32000, 40000]
        detected = sample_rate in ai_sample_rates
        
        return {
            'detected': detected,
            'details': {
                'sample_rate': sample_rate,
                'typical_ai_rates': ai_sample_rates
            },
            'reasoning_key': 'indicators.sample_rate.reasoning' if detected else 'indicators.ok'
        }