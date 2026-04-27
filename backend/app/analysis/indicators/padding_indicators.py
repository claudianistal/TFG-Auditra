"""
Padding pattern indicators for AI detection.
This is one of the most important indicators for detecting AI-generated audio.
"""
from typing import Dict, Any
from .base_indicator import BaseIndicator


class PaddingPatternIndicator(BaseIndicator):
    """Detects suspicious padding patterns at file start/end.
    
    Weight: 85 (ALTO) - Padding is a strong indicator of AI-generated audio.
    Checks for zero byte sequences (0x00) and excessive padding percentages.
    """
    
    name = "padding_pattern"
    category = "padding"
    weight = 85
    description = "Patrón de relleno sospechoso detectado"
    risk_level = "high"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check for suspicious padding patterns at start and end of file.
        AI-generated audio often has padding with repetitive bytes (zeros).
        """
        hex_start = patterns.get('hex_start', [])
        hex_end = patterns.get('hex_end', [])
        total_file_size = patterns.get('total_file_size', 1)
        
        # Convert lists to strings if needed
        if isinstance(hex_start, list):
            hex_start = '\n'.join(hex_start)
        if isinstance(hex_end, list):
            hex_end = '\n'.join(hex_end)
        
        # Count zero bytes at start and end
        zeros_start = self._count_consecutive_zeros(hex_start)
        zeros_end = self._count_consecutive_zeros(hex_end)
        total_zeros = zeros_start + zeros_end
        
        # Calculate percentage
        padding_percentage = (total_zeros / total_file_size * 100) if total_file_size > 0 else 0
        
        # Detect if padding is suspicious
        # Either: >100 consecutive zeros OR >3% total padding
        detected = zeros_start > 100 or zeros_end > 100 or padding_percentage > 3
        
        return {
            'detected': detected,
            'confidence': min(padding_percentage / 10, 1.0) if padding_percentage > 0 else 0.0,
            'details': {
                'zeros_at_start': zeros_start,
                'zeros_at_end': zeros_end,
                'total_padding_bytes': total_zeros,
                'padding_percentage': round(padding_percentage, 2),
                'total_file_size': total_file_size
            },
            'reasoning_key': 'indicators.padding_pattern.reasoning'
        }
    
    @staticmethod
    def _count_consecutive_zeros(hex_string: str) -> int:
        """Count consecutive zero bytes (0x00) in hex string."""
        if not hex_string:
            return 0
        
        # Clean hex string: remove spaces and newlines, convert to lowercase
        hex_clean = hex_string.replace(' ', '').replace('\n', '').lower()
        
        # Count consecutive zero bytes (each zero byte is "00" in hex)
        zero_count = 0
        max_consecutive = 0
        
        for i in range(0, len(hex_clean) - 1, 2):
            byte = hex_clean[i:i+2]
            if byte == '00':
                zero_count += 1
                max_consecutive = max(max_consecutive, zero_count)
            else:
                zero_count = 0
        
        return max_consecutive
