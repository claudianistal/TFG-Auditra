"""
Padding pattern indicators for AI detection.
This is one of the most important indicators for detecting AI-generated audio.
"""
import re
from typing import Dict, Any, List
from .base_indicator import BaseIndicator


class PaddingPatternIndicator(BaseIndicator):
    """Detects suspicious padding patterns throughout the file.
    
    Weight: 85 (ALTO) - Padding is a strong indicator of AI-generated audio.
    Checks for exact repetitive byte sequences (0x00, 0xFF, 0xAA, etc.) 
    and excessive padding percentages.
    """
    
    name = "padding_pattern"
    category = "padding"
    weight = 85
    description = "Patrón de relleno sospechoso detectado"
    risk_level = "high"
    
  
    MIN_CONSECUTIVE_BYTES = 70
    MIN_PADDING_PERCENTAGE = 3
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze exact padding patterns across the ENTIRE file.
        """
        # 1. Extract the full hex dump from patterns (already formatted as a list of lines)
        full_hex_raw = patterns.get('full_hex', "")
        total_file_size = patterns.get('total_file_size', 1)

        # 2. Extract the clean list of bytes (0-255)
        bytes_full = self._extract_bytes_from_hexdump(full_hex_raw)

        # 3. Search for exact sequences (without normalizations or alterations)
        patterns_found = self._find_consecutive_in_list(bytes_full)

        # 4. Calculate total padding bytes and percentage
        total_padding_bytes = sum(p['count'] for p in patterns_found)
        padding_percentage = (total_padding_bytes / total_file_size * 100) if total_file_size > 0 else 0
        
        max_pattern = max((p['count'] for p in patterns_found), default=0)

        # 5. Detection logic
        detected = (max_pattern >= self.MIN_CONSECUTIVE_BYTES or 
                    padding_percentage > self.MIN_PADDING_PERCENTAGE)

        return {
            'detected': detected,
            'details': {
                'max_consecutive_sequence': max_pattern,
                'total_repetitive_bytes': total_padding_bytes,
                'padding_percentage': round(padding_percentage, 2),
                'total_file_size': total_file_size,
                'top_patterns': [
                    {'pattern': f'0x{p["byte"]:02x}', 'consecutive_bytes': p['count']}
                    for p in patterns_found[:5]
                ]
            },
            'reasoning_key': 'indicators.padding_pattern.reasoning' if detected else 'indicators.ok'
        }

    def _extract_bytes_from_hexdump(self, raw_input: Any) -> List[int]:
        """
        Cleans hexdump input by extracting only the central hex byte values.
        """
        if not raw_input:
            return []
        
        if isinstance(raw_input, list):
            raw_input = '\n'.join(raw_input)

        clean_bytes = []
        lines = raw_input.splitlines()

        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)[1]
                if '|' in parts:
                    parts = parts.split('|')[0]
                
                hex_pairs = re.findall(r'[0-9a-fA-F]{2}', parts)
                for pair in hex_pairs:
                    clean_bytes.append(int(pair, 16))
            else:
                hex_pairs = re.findall(r'[0-9a-fA-F]{2}', line)
                for pair in hex_pairs:
                    clean_bytes.append(int(pair, 16))
        
        return clean_bytes

    def _find_consecutive_in_list(self, byte_list: List[int]) -> List[Dict[str, Any]]:
        """
        Identifies exact sequences of identical consecutive bytes.
        No normalization. Pure byte-to-byte comparison.
        """
        if not byte_list:
            return []

        patterns = {}
        current_byte = byte_list[0]
        current_count = 1

        for i in range(1, len(byte_list)):
            if byte_list[i] == current_byte:
                current_count += 1
            else:
                if current_count >= self.MIN_CONSECUTIVE_BYTES:
                    patterns[current_byte] = max(patterns.get(current_byte, 0), current_count)
                
                current_byte = byte_list[i]
                current_count = 1
        
        if current_count >= self.MIN_CONSECUTIVE_BYTES:
            patterns[current_byte] = max(patterns.get(current_byte, 0), current_count)

        result = [{'byte': b, 'count': c} for b, c in patterns.items()]
        return sorted(result, key=lambda x: x['count'], reverse=True)