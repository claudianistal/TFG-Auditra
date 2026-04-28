"""
Self-similarity indicators for AI detection.
Detects structural self-similarity at multiple resolutions.
Based on bitmap visualization concept: if the same patterns appear at the same
row positions across different byte widths (128, 256, 512, 1024, 2048),
it indicates structural repetition typical of AI-generated audio.
"""
import re
import numpy as np
from typing import Dict, Any, List, Tuple
from .base_indicator import BaseIndicator


class SelfSimilarityIndicator(BaseIndicator):
    """
    Detects structural self-similarity by analyzing byte patterns at multiple resolutions.
    
    Concept: If we reshape the byte stream at different widths,
    and the same patterns appear in the same relative row positions, it indicates
    repetitive structure typical of AI-generated audio.
    
    Natural audio: Random/varied byte patterns → different visual structure at each width
    AI audio: Structured/repetitive patterns → similar visual structure at each width
    
    """
    
    name = "self_similarity"
    category = "structure"
    weight = 70
    description = "Patrones de autosimilitud detectados en datos"
    risk_level = "high"
    

    # Minimum threshold: If more than 5% of the file consists of self-similar blocks, flag it.
    MIN_SELF_SIMILAR_RATIO = 0.05 
    # Test multiple resolutions like bitmap visualization does
    TEST_WIDTHS = [128, 256, 512, 1024, 2048]
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the self-similarity structural analysis on the provided hex dump.        
        """
        # Get hex dump data
        raw_hex = patterns.get('full_hex', [])
        
        if not raw_hex:
            # Fallback: combine start and end
            hex_start = patterns.get('hex_start', [])
            hex_end = patterns.get('hex_end', [])
            
            raw_hex = []
            if isinstance(hex_start, list):
                raw_hex.extend(hex_start)
            elif hex_start:
                raw_hex = [hex_start]
            
            if isinstance(hex_end, list):
                raw_hex.extend(hex_end)
            elif hex_end:
                raw_hex.append(hex_end)
        
        if not raw_hex:
            return self._empty_result()
        
        # Extract raw bytes from the hex strings
        byte_list = self._extract_bytes_from_hexdump(raw_hex)
        
        if len(byte_list) < 128:
            return self._empty_result()
        
        # Analyze self-similarity through multi-resolution matrix comparison
        self_similarity_score = self._analyze_multi_resolution_patterns(byte_list)
        
        # Determine detection and calculate confidence
        detected = self_similarity_score > self.MIN_SELF_SIMILAR_RATIO
        confidence = min(self_similarity_score * 1.5, 1.0)
        
        return {
            'detected': detected,
            'confidence': confidence,
            'details': {
                'self_similarity_score': round(self_similarity_score, 3),
                'threshold': self.MIN_SELF_SIMILAR_RATIO,
                'bytes_analyzed': len(byte_list),
                'interpretation': 'Data compressibility analysis - repetitive patterns detected'
            },
            'reasoning_key': 'indicators.self_similarity.reasoning'
        }
    
    def _analyze_multi_resolution_patterns(self, byte_list: List[int]) -> float:
        """
        Detects self-similarity by evaluating a 2D matrix representation of the bytes 
        at various spatial resolutions.
        
        It calculates the proportion of rows that are anomalously identical to their 
        preceding row, allowing for minor variations (noise/dithering).
        
        Args:
            byte_list: List of integer byte values (0-255).
            
        Returns:
            float: The highest ratio of anomalous self-similar rows found across all tested widths.
        """
        if not byte_list or len(byte_list) < max(self.TEST_WIDTHS):
            return 0.0
            
        byte_array = np.array(byte_list, dtype=np.uint8)
        best_anomaly_ratio = 0.0
        
        for width in self.TEST_WIDTHS:
            if len(byte_array) < width * 3:
                continue
                
            num_rows = len(byte_array) // width
            # Recreate the 2D matrix used in the PNG bitmap visualization
            matrix = byte_array[:num_rows * width].reshape((num_rows, width))
            
            # Compare the entire matrix shifted by one row (Row N vs. Row N-1).
            # This yields a boolean matrix of exact byte-to-byte matches.
            matches_matrix = (matrix[1:] == matrix[:-1])
            
            # Sum the matches per row (axis 1).
            # matches_per_row will contain integer values ranging from 0 to 'width'.
            matches_per_row = np.sum(matches_matrix, axis=1)
            
            # Calculate the similarity percentage of each row relative to the previous one.
            # In purely natural, high-entropy audio, this ratio averages roughly 0.0039 (1/256).
            row_similarity_ratio = matches_per_row / width
            
            # A row is classified as a "self-similarity band" if over 50% of its 
            # bytes perfectly match the corresponding positions in the preceding row.
            anomalous_rows = np.sum(row_similarity_ratio > 0.50)
            
            # Calculate the overall percentage of the file comprised of these anomalous bands.
            total_comparisons = num_rows - 1
            file_anomaly_ratio = anomalous_rows / total_comparisons
            
            # Retain the resolution (width) that reveals the highest degree of structural repetition.
            best_anomaly_ratio = max(best_anomaly_ratio, file_anomaly_ratio)
            
        return best_anomaly_ratio
    
    def _extract_bytes_from_hexdump(self, raw_input: Any) -> List[int]:
        """
        Parses and extracts raw byte values from various hex dump formats.
        Robustly handles structural artifacts such as address columns and ASCII representations.
        
        Args:
            raw_input: Raw hex dump string or list of strings.
            
        Returns:
            List[int]: Cleaned sequence of integer byte values.
        """
        if not raw_input:
            return []
        
        if isinstance(raw_input, list):
            raw_input = '\n'.join(raw_input)
        
        clean_bytes = []
        lines = raw_input.splitlines()
        
        for line in lines:
            if ':' in line:
                # Remove address column
                parts = line.split(':', 1)[1]
                if '|' in parts:
                    # Remove ASCII representation
                    parts = parts.split('|')[0]
            else:
                parts = line
            
            # Extract all hex pairs
            hex_pairs = re.findall(r'[0-9a-fA-F]{2}', parts)
            clean_bytes.extend([int(pair, 16) for pair in hex_pairs])
        
        return clean_bytes
    
    def _empty_result(self) -> Dict[str, Any]:
        return {
            'detected': False,
            'confidence': 0.0,
            'details': {},
            'reasoning_key': 'indicators.self_similarity.reasoning'
        }
