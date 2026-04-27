"""
Analysis scorer - Calculates AI likelihood score based on detected indicators.
"""
from typing import List, Dict, Any


class AnalysisScorer:
    """
    Encapsulates scoring logic for AI detection analysis.
    Converts detected indicators into a unified risk score (0-100).
    """
    
    MAX_SCORE = 100
    MIN_SCORE = 0
    
    def calculate_score(self, detected_factors: List[Dict[str, Any]]) -> int:
        """
        Calculate total risk score based on detected factors.
        
        Uses weighted sum: each factor contributes (weight * confidence).
        The higher the score, the higher the likelihood of AI generation.
        
        Args:
            detected_factors: List of detected indicator results
            
        Returns:
            int: Risk score from 0-100
        """
        total_score = 0
        
        for factor in detected_factors:
            weight = factor.get('weight', 0)
            confidence = factor.get('confidence', 0.0)
            
            # Contribution = weight * confidence
            contribution = weight * confidence
            total_score += contribution
        
        # Maximum possible score is when all weights sum with confidence=1
        # We use a fixed max of 237 (sum of all indicator weights)
        max_possible_score = 237
        
        # Normalize to 0-100 range
        if max_possible_score > 0:
            normalized_score = (total_score / max_possible_score) * self.MAX_SCORE
        else:
            normalized_score = 0
        
        # Cap at MAX_SCORE
        final_score = min(int(normalized_score), self.MAX_SCORE)
        
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
    
    def get_score_percentile(self, score: int) -> str:
        """
        Get human-readable description of score percentile.
        """
        if score <= 20:
            return "Muy bajo"
        elif score <= 40:
            return "Bajo"
        elif score <= 60:
            return "Medio"
        elif score <= 80:
            return "Alto"
        else:
            return "Muy alto"
