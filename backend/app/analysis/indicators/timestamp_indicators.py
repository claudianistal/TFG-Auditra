"""
Timestamp indicators for AI detection.
"""
from typing import Dict, Any
from .base_indicator import BaseIndicator


class TimestampConsistencyIndicator(BaseIndicator):
    """Detects timestamp inconsistencies or anomalies.
    
    Weight: 20 (BAJO) - Checks creation vs modification dates.
    AI-generated files may have identical or suspicious timestamps.
    """
    
    name = "timestamp_consistency"
    category = "timestamp"
    weight = 20
    description = "Inconsistencia en timestamps de creación/modificación"
    risk_level = "low"
    
    def check(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if creation timestamp is before modification timestamp.
        If they are identical or creation is after modification, it's suspicious.
        """
        creation_time = metadata.get('file_creation_time', '')
        modification_time = metadata.get('file_modification_time', '')
        
        # If either timestamp is missing, we can't determine inconsistency
        if not creation_time or not modification_time:
            return {
                'detected': False,
                'details': {
                    'creation_time': creation_time,
                    'modification_time': modification_time,
                    'reason': 'Timestamps no disponibles'
                },
                'reasoning_key': 'indicators.timestamp_consistency.reasoning_missing'
            }
        
        # Compare timestamps
        detected = False
        reasoning_key = 'indicators.timestamp_consistency.reasoning_ok'
        
        # Try string comparison first (assumes ISO format or similar)
        try:
            # If timestamps are strings, do lexicographic comparison (works for ISO 8601)
            if isinstance(creation_time, str) and isinstance(modification_time, str):
                # Timestamps should be: creation_time < modification_time
                if creation_time == modification_time:
                    detected = True
                    reasoning_key = 'indicators.timestamp_consistency.reasoning_identical'
                elif creation_time > modification_time:
                    detected = True
                    reasoning_key = 'indicators.timestamp_consistency.reasoning_reversed'
                else:
                    # creation_time < modification_time, which is normal
                    detected = False
                    reasoning_key = 'indicators.timestamp_consistency.reasoning_ok'
        except Exception as e:
            # If comparison fails, assume no anomaly
            return {
                'detected': False,
                'details': {
                    'creation_time': creation_time,
                    'modification_time': modification_time,
                    'error': str(e)
                },
                'reasoning_key': 'indicators.timestamp_consistency.reasoning_error'
            }
        
        return {
            'detected': detected,
            'details': {
                'creation_time': creation_time,
                'modification_time': modification_time,
                'relationship': 'identical' if creation_time == modification_time else 'creation_after_modification' if creation_time > modification_time else 'normal'
            },
            'reasoning_key': reasoning_key
        }
