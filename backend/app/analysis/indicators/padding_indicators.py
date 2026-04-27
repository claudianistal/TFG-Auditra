"""
Padding pattern indicators for AI detection.
This is one of the most important indicators for detecting AI-generated audio.
"""
import re
from typing import Dict, Any, List
from .base_indicator import BaseIndicator


class PaddingPatternIndicator(BaseIndicator):
    """Detects suspicious padding patterns at file start/end.
    
    Weight: 85 (ALTO) - Padding is a strong indicator of AI-generated audio.
    Checks for repetitive byte sequences (0x00, 0xFF, 0xAA, etc.) and excessive padding percentages.
    Improved to detect ANY repeated byte pattern, not just zeros.
    """
    
    name = "padding_pattern"
    category = "padding"
    weight = 85
    description = "Patrón de relleno sospechoso detectado"
    risk_level = "high"
    
    # Minimum threshold for consecutive bytes to consider as padding
    MIN_CONSECUTIVE_BYTES = 100
    # Minimum percentage of file that should be padding to flag as suspicious
    MIN_PADDING_PERCENTAGE = 3
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze padding patterns at the beginning and end of the file.
        
        Args:
            metadata: Dict containing file metadata.
            patterns: Dict containing 'hex_start', 'hex_end', and 'total_file_size'.
            
        Returns:
            Dict with detection results, confidence, and detailed pattern breakdown.
        """
        # Retrieve input data
        hex_start_raw = patterns.get('hex_start', "")
        hex_end_raw = patterns.get('hex_end', "")
        total_file_size = patterns.get('total_file_size', 1)

        # 1. Extract clean byte lists from potential hexdump formats (handles offsets and ASCII)
        bytes_start = self._extract_bytes_from_hexdump(hex_start_raw)
        bytes_end = self._extract_bytes_from_hexdump(hex_end_raw)

        # 2. Analyze consecutive sequences in the cleaned byte streams
        patterns_start = self._find_consecutive_in_list(bytes_start)
        patterns_end = self._find_consecutive_in_list(bytes_end)

        # 3. Calculate metrics
        total_padding_bytes = sum(p['count'] for p in patterns_start + patterns_end)
        padding_percentage = (total_padding_bytes / total_file_size * 100) if total_file_size > 0 else 0
        
        max_pattern_start = max((p['count'] for p in patterns_start), default=0)
        max_pattern_end = max((p['count'] for p in patterns_end), default=0)

        # 4. Detection logic
        # Flag if: single sequence exceeds threshold OR total padding is excessive
        detected = (max_pattern_start > self.MIN_CONSECUTIVE_BYTES or 
                    max_pattern_end > self.MIN_CONSECUTIVE_BYTES or 
                    padding_percentage > self.MIN_PADDING_PERCENTAGE)

        return {
            'detected': detected,
            'confidence': min(padding_percentage / 10, 1.0) if padding_percentage > 0 else 0.0,
            'details': {
                # Legacy compatibility fields
                'padding_at_start': max_pattern_start, 
                'padding_at_end': max_pattern_end,
                'total_padding_bytes': total_padding_bytes,
                'padding_percentage': round(padding_percentage, 2),
                'total_file_size': total_file_size,
                # Detailed pattern analysis
                'patterns_at_start': [
                    {'pattern': f'0x{p["byte"]:02x}', 'consecutive_bytes': p['count']}
                    for p in patterns_start
                ],
                'patterns_at_end': [
                    {'pattern': f'0x{p["byte"]:02x}', 'consecutive_bytes': p['count']}
                    for p in patterns_end
                ]
            },
            'reasoning_key': 'indicators.padding_pattern.reasoning'
        }

    def _extract_bytes_from_hexdump(self, raw_input: Any) -> List[int]:
        """
        Cleans hexdump input by extracting only the central hex byte values.
        It strips memory offsets (e.g., 0001fd2d:) and ASCII representations.
        
        Args:
            raw_input: String or list of strings representing the hex dump.
            
        Returns:
            List of integers representing the raw bytes.
        """
        if not raw_input:
            return []
        
        if isinstance(raw_input, list):
            raw_input = '\n'.join(raw_input)

        clean_bytes = []
        lines = raw_input.splitlines()

        for line in lines:
            # Process lines with hexdump format (Offset: Bytes | ASCII)
            if ':' in line:
                # Extract part after the offset
                parts = line.split(':', 1)[1]
                # Strip the ASCII section if present
                if '|' in parts:
                    parts = parts.split('|')[0]
                
                # Find all 2-character hex pairs (00-FF)
                hex_pairs = re.findall(r'[0-9a-fA-F]{2}', parts)
                for pair in hex_pairs:
                    clean_bytes.append(int(pair, 16))
            else:
                # Fallback for plain hex strings or malformed lines
                hex_pairs = re.findall(r'[0-9a-fA-F]{2}', line)
                for pair in hex_pairs:
                    clean_bytes.append(int(pair, 16))
        
        return clean_bytes

    def _find_consecutive_in_list(self, byte_list: List[int]) -> List[Dict[str, Any]]:
        """
        Identifies sequences of identical consecutive bytes in a byte list.
        
        Args:
            byte_list: List of integers (bytes) to analyze.
            
        Returns:
            List of dicts with 'byte' and 'count', sorted by count descending.
        """
        if not byte_list:
            return []

        patterns = {}
        if not byte_list:
            return []
            
        current_byte = byte_list[0]
        current_count = 1

        for i in range(1, len(byte_list)):
            if byte_list[i] == current_byte:
                current_count += 1
            else:
                # Store the maximum count found for this specific byte
                if current_count >= self.MIN_CONSECUTIVE_BYTES:
                    patterns[current_byte] = max(patterns.get(current_byte, 0), current_count)
                
                current_byte = byte_list[i]
                current_count = 1
        
        # Handle the last group in the list
        if current_count >= self.MIN_CONSECUTIVE_BYTES:
            patterns[current_byte] = max(patterns.get(current_byte, 0), current_count)

        # Format and sort results
        result = [{'byte': b, 'count': c} for b, c in patterns.items()]
        return sorted(result, key=lambda x: x['count'], reverse=True)