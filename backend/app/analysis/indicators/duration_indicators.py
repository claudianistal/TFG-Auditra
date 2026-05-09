from typing import Dict, Any
from .base_indicator import BaseIndicator

class PreciseDurationIndicator(BaseIndicator):
    """
    Looks for mathematically "perfect" durations (e.g., 15.000s or 30.500s).
    Human recordings have irregular durations, but synthetic generations 
    or automated programmatic cuts usually have exact boundaries in seconds.
    """
    
    name = "precise_duration"
    category = "format"
    weight = 15
    description = "Duración truncada o matemáticamente exacta"
    risk_level = "low"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        duration_str = metadata.get('ffprobe_format_duration', '0')
        
        try:
            duration = float(duration_str)
        except ValueError:
            return {
                'detected': False, 
                'details': {}, 
                'reasoning_key': 'indicators.precise_duration.error'
            }

        if duration <= 0:
            return {
                'detected': False, 
                'details': {}, 
                'reasoning_key': 'indicators.precise_duration.no_data'
            }

        # Extract the decimal part (e.g., 15.000 -> 0.0, 30.500 -> 0.5)
        decimal_part = duration % 1.0
        
        # Round to 6 decimal places to prevent Python floating point anomalies
        clean_decimal = round(decimal_part, 6)
        
        # Strict exact matching (no margins allowed)
        is_exact_second = (clean_decimal == 0.0) or (clean_decimal == 1.0)
        is_exact_half_second = (clean_decimal == 0.5)
        
        detected = is_exact_second or is_exact_half_second
        
        return {
            'detected': detected,
            'details': {
                'exact_duration': round(duration, 4),
                'decimal_part': clean_decimal
            },
            'reasoning_key': 'indicators.precise_duration.reasoning' if detected else 'indicators.ok'
        }