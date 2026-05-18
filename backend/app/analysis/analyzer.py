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
        
        found_indicators = []
        
        # Check for specific patterns and recommend actions for all indicators
        indicator_mappings = [
            ('padding_pattern', 'recommendations.padding_pattern'),
            ('timestamp_consistency', 'recommendations.timestamp_consistency'),
            ('encoding_library', 'recommendations.encoding_library'),
            ('mono_audio', 'recommendations.mono_audio'),
            ('codec_consistency', 'recommendations.codec_consistency'),
            ('file_size', 'recommendations.file_size'),
            ('self_similarity', 'recommendations.self_similarity'),
            ('sample_rate_anomaly', 'recommendations.sample_rate_anomaly'),
            ('atypical_bitrate', 'recommendations.atypical_bitrate'),
            ('precise_duration', 'recommendations.precise_duration'),
        ]
        
        for indicator_name, recommendation_key in indicator_mappings:
            if any(f.get('name') == indicator_name for f in detected_factors):
                recommendations.append(recommendation_key)
                found_indicators.append(indicator_name)

        if len(detected_factors) > 4:
            recommendations.append('recommendations.multiple_indicators')

        if not recommendations:
            recommendations.append('recommendations.no_indicators')
        
        return recommendations
    
    @staticmethod
    def _get_iso_timestamp() -> str:
        """Get current timestamp in ISO 8601 format with Z suffix."""
        # Generate UTC timestamp and format it correctly for JavaScript Date parsing
        utc_now = datetime.now(timezone.utc)
        # Format: 2026-05-18T12:34:56.789Z (JavaScript compatible)
        return utc_now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
