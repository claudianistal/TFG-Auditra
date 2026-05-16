"""
AI Detection Analyzer - Orchestrates the analysis process.
Runs all indicators and produces a comprehensive analysis report.
"""
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone
from .indicators import INDICATORS
from .scorer import AnalysisScorer


class AIDetectionAnalyzer:
    """
    Main analyzer that orchestrates all indicators and produces analysis results.
    """
    
    def __init__(self):
        """Initialize the analyzer with scorer and indicators."""
        self.scorer = AnalysisScorer()
        self.indicators = INDICATORS
    
    def analyze(self, metadata: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute full analysis on audio file.
        
        Args:
            metadata: Extracted file metadata
            patterns: Pattern analysis results (hex_start, hex_end, etc)
            
        Returns:
            Comprehensive analysis result dictionary
        """
        # Run all indicators
        all_indicators_results = []
        detected_factors = []
        missing_factors = []
        
        for indicator in self.indicators:
            try:
                result = indicator.check(metadata, patterns)
                
                indicator_data = {
                    'name': indicator.name,
                    'display_name': indicator.description,
                    'category': indicator.category,
                    'weight': indicator.weight,
                    'detected': result['detected'],
                    'risk_level': indicator.risk_level,
                    'reasoning_key': result['reasoning_key'],
                    'details': result['details']
                }
                
                all_indicators_results.append(indicator_data)
                
                if result['detected']:
                    detected_factors.append(indicator_data)
                else:
                    missing_factors.append(indicator_data)
            
            except Exception as e:
                # Log error but continue with other indicators
                print(f"Error running indicator {indicator.name}: {str(e)}")
        
        # Calculate score
        risk_score = self.scorer.calculate_score(detected_factors)
        score_interpretation = self.scorer.interpret_score(risk_score)
        
        # Generate conclusions and recommendations
        conclusion = self._generate_conclusion(detected_factors, risk_score)
        recommendations = self._generate_recommendations(detected_factors)
        
        return {
            'risk_score': risk_score,
            'likelihood': score_interpretation['likelihood'],
            'likelihood_description': score_interpretation['description'],
            'score_color': score_interpretation['color'],
            'detected_factors': detected_factors,
            'missing_factors': missing_factors,
            'all_indicators': all_indicators_results,
            'conclusion_key': conclusion,
            'recommendations': recommendations,
            'analysis_date': self._get_iso_timestamp()
        }
    
    def _generate_conclusion(self, detected_factors: List[Dict[str, Any]], risk_score: int) -> str:
        """
        Generate conclusion key for frontend translation based on detected factors.
        Returns i18n key for the conclusion message.
        """
        if not detected_factors:
            return "conclusions.no_indicators"
        
        # Count factors by risk level
        high_risk = [f for f in detected_factors if f['risk_level'] == 'high']
        
        if risk_score < 30:
            return "conclusions.low_risk"
        
        elif risk_score < 60:
            return "conclusions.medium_risk"
        
        else:
            if high_risk:
                return "conclusions.high_risk_critical"
            else:
                return "conclusions.high_risk_multiple"
    
    def _generate_recommendations(self, detected_factors: List[Dict[str, Any]]) -> List[str]:
        """
        Generate actionable recommendations based on findings.
        Returns i18n keys for frontend translation.
        """
        recommendations = []
        
        # Check for specific patterns and recommend actions based on 6 simplified indicators
        if any(f['name'] == 'padding_pattern' for f in detected_factors):
            recommendations.append('recommendations.padding_pattern')
        
        if any(f['name'] == 'timestamp_consistency' for f in detected_factors):
            recommendations.append('recommendations.timestamp_consistency')
        
        if any(f['name'] == 'encoding_library' for f in detected_factors):
            recommendations.append('recommendations.encoding_library')
        
        if any(f['name'] == 'mono_audio' for f in detected_factors):
            recommendations.append('recommendations.mono_audio')
        
        if any(f['name'] == 'codec_consistency' for f in detected_factors):
            recommendations.append('recommendations.codec_consistency')
        
        if any(f['name'] == 'file_size' for f in detected_factors):
            recommendations.append('recommendations.file_size')
        
        if len(detected_factors) > 4:
            recommendations.append('recommendations.multiple_indicators')
        
        if not recommendations:
            recommendations.append('recommendations.no_indicators')
        
        return recommendations
    
    @staticmethod
    def _get_iso_timestamp() -> str:
        """Get current timestamp in ISO format."""
        return datetime.now(timezone.utc).isoformat() + 'Z'
