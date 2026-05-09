"""
Analysis scorer - Calculates AI likelihood score based on detected indicators.
"""
from typing import List, Dict, Any


class AnalysisScorer:
    """
    Encapsulates scoring logic for AI detection analysis.
    Uses an Additive Penalty System capped at 100 for maximum forensic transparency.
    """
    
    MAX_SCORE = 100
    MIN_SCORE = 0
    
    def calculate_score(self, detected_factors: List[Dict[str, Any]]) -> int:
        """
        Calculate total risk score based on detected factors using additive scoring.
        
        This method is transparent and defensible in forensic contexts:
        Each detected anomaly adds its weight (penalty) to the total score.
        If the sum exceeds 100, it is capped at 100.
        
        Args:
            detected_factors: List of detected indicator results
            
        Returns:
            int: Risk score from 0-100
        """
        if not detected_factors:
            return self.MIN_SCORE

        # Sumar los pesos de todos los factores detectados
        total_penalty = sum(factor.get('weight', 0) for factor in detected_factors)
        
        # Topar la puntuación al máximo permitido (100)
        final_score = min(total_penalty, self.MAX_SCORE)
        
        return max(final_score, self.MIN_SCORE)
    
    def interpret_score(self, score: int) -> Dict[str, str]:
        """
        Interpret a risk score into human-readable categories.
        
        Args:
            score: Risk score (0-100)
            
        Returns:
            Dictionary with 'likelihood' and 'description'
        """
        if score < 30:
            return {
                'likelihood': 'bajo',
                'description': 'Bajo riesgo de generación por IA',
                'color': 'green'
            }
        elif score < 60:
            return {
                'likelihood': 'medio',
                'description': 'Riesgo medio de generación por IA',
                'color': 'yellow'
            }
        else:
            return {
                'likelihood': 'alto',
                'description': 'Alto riesgo de generación por IA',
                'color': 'red'
            }