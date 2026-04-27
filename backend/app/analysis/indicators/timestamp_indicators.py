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
                'confidence': 0.0,
                'details': {
                    'creation_time': creation_time,
                    'modification_time': modification_time,
                    'reason': 'Timestamps no disponibles'
                },
                'reasoning': 'No se puede verificar consistencia sin timestamps'
            }
        
        # Compare timestamps
        detected = False
        confidence = 0.0
        reason = 'Timestamps consistentes'
        
        # Try string comparison first (assumes ISO format or similar)
        try:
            # If timestamps are strings, do lexicographic comparison (works for ISO 8601)
            if isinstance(creation_time, str) and isinstance(modification_time, str):
                # Timestamps should be: creation_time < modification_time
                if creation_time == modification_time:
                    detected = True
                    confidence = 0.8
                    reason = 'Timestamps de creación y modificación son idénticos'
                elif creation_time > modification_time:
                    detected = True
                    confidence = 0.9
                    reason = 'Timestamp de creación es posterior a modificación'
                else:
                    # creation_time < modification_time, which is normal
                    detected = False
                    confidence = 0.0
                    reason = 'Timestamps consistentes (creación < modificación)'
        except Exception as e:
            # If comparison fails, assume no anomaly
            return {
                'detected': False,
                'confidence': 0.0,
                'details': {
                    'creation_time': creation_time,
                    'modification_time': modification_time,
                    'error': str(e)
                },
                'reasoning': 'Error al comparar timestamps'
            }
        
        return {
            'detected': detected,
            'confidence': confidence,
            'details': {
                'creation_time': creation_time,
                'modification_time': modification_time,
                'relationship': 'identical' if creation_time == modification_time else 'creation_after_modification' if creation_time > modification_time else 'normal'
            },
            'reasoning': reason
        }
