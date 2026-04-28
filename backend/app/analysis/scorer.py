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
        Calculate total risk score based on detected factors using asymptotic probability.
        
        This method prevents score dilution when high-weight indicators are found alongside
        many un-triggered low-weight indicators. A single highly confident, high-weight
        indicator will push the score significantly towards 100.
        
        Args:
            detected_factors: List of detected indicator results
            
        Returns:
            int: Risk score from 0-100
        """
        if not detected_factors:
            return self.MIN_SCORE

        not_ai_probability = 1.0
        
        for factor in detected_factors:
            weight = factor.get('weight', 0)
            
            # Calculate the individual probability factor (0.0 to 1.0)
            # Only detected factors contribute, using their weight directly
            indicator_prob = weight / 100.0
            
            # Cap at 0.99 to ensure a single indicator never forces an absolute 100
            # unless we explicitly want it to. It allows multiple strong indicators 
            # to stack asymptotically.
            indicator_prob = min(indicator_prob, 0.99)
            
            # Multiply the probabilities that the audio is NOT AI
            not_ai_probability *= (1.0 - indicator_prob)
            
        # The final score is the inverse probability scaled to MAX_SCORE
        final_score = int(self.MAX_SCORE * (1.0 - not_ai_probability))
        
        return max(min(final_score, self.MAX_SCORE), self.MIN_SCORE)
    
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
    