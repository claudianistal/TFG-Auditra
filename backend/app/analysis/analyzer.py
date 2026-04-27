"""
AI Detection Analyzer - Orchestrates the analysis process.
Runs all indicators and produces a comprehensive analysis report.
"""
from typing import Dict, Any, List, Tuple
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
                    'confidence': result['confidence'],
                    'risk_level': indicator.risk_level,
                    'reasoning': result['reasoning'],
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
            'score_percentile': self.scorer.get_score_percentile(risk_score),
            'detected_factors': detected_factors,
            'missing_factors': missing_factors,
            'all_indicators': all_indicators_results,
            'conclusion': conclusion,
            'recommendations': recommendations,
            'analysis_date': self._get_iso_timestamp()
        }
    
    def _generate_conclusion(self, detected_factors: List[Dict[str, Any]], risk_score: int) -> str:
        """
        Generate a human-readable conclusion based on detected factors.
        """
        if not detected_factors:
            return "No se detectaron indicadores de generación por IA. " \
                   "Este audio parece ser una grabación auténtica."
        
        # Count factors by risk level
        high_risk = [f for f in detected_factors if f['risk_level'] == 'high']
        medium_risk = [f for f in detected_factors if f['risk_level'] == 'medium']
        
        if risk_score < 30:
            return "El análisis indica un bajo riesgo de generación por IA. " \
                   "Aunque se detectaron algunos indicadores menores, no hay evidencia concluyente " \
                   "de procesamiento artificial."
        
        elif risk_score < 60:
            factors_desc = self._format_factors_for_conclusion(detected_factors[:3])
            return f"El análisis indica un riesgo medio de generación por IA. " \
                   f"Se detectaron varios indicadores sospechosos: {factors_desc}. " \
                   f"Se recomienda un análisis más profundo."
        
        else:
            if high_risk:
                critical = [f['display_name'] for f in high_risk[:2]]
                critical_desc = " y ".join(critical)
                return f"El análisis indica un alto riesgo de generación por IA. " \
                       f"Se detectaron indicadores críticos: {critical_desc}. " \
                       f"Este audio muy probablemente fue generado por herramientas de síntesis o IA."
            else:
                factors_desc = self._format_factors_for_conclusion(detected_factors[:3])
                return f"El análisis indica un alto riesgo de generación por IA. " \
                       f"Múltiples indicadores sugieren procesamiento artificial: {factors_desc}."
    
    def _generate_recommendations(self, detected_factors: List[Dict[str, Any]]) -> List[str]:
        """
        Generate actionable recommendations based on findings.
        """
        recommendations = []
        
        # Check for specific patterns and recommend actions
        if any(f['name'].startswith('zero_padding') for f in detected_factors):
            recommendations.append(
                "El relleno con ceros detectado es un indicador fuerte. "
                "Considere analizar archivos de la misma fuente para confirmar un patrón."
            )
        
        if any(f['name'] == 'format_mismatch' for f in detected_factors):
            recommendations.append(
                "Se detectó una inconsistencia de formato. "
                "El archivo puede haber sido manipulado o reempaquetado. Verifique la integridad."
            )
        
        if any(f['name'] == 'lavf_detected' for f in detected_factors):
            recommendations.append(
                "Se detectó FFmpeg/Lavf. Si bien es una herramienta legítima, "
                "también es usada en herramientas de síntesis. Analice junto con otros indicadores."
            )
        
        if any(f['name'] == 'mono_audio' for f in detected_factors):
            recommendations.append(
                "El audio mono es menos común en grabaciones naturales. "
                "Típico en síntesis de voz o procesamiento automatizado."
            )
        
        if len(detected_factors) > 5:
            recommendations.append(
                "Se detectaron múltiples indicadores. Le recomendamos obtener una segunda opinión "
                "mediante análisis con otras herramientas de detección de deepfakes."
            )
        
        if not recommendations:
            recommendations.append(
                "El audio no presenta indicadores típicos de generación por IA. "
                "Sin embargo, las técnicas de IA evolucionan constantemente."
            )
        
        return recommendations
    
    @staticmethod
    def _format_factors_for_conclusion(factors: List[Dict[str, Any]]) -> str:
        """Format factors for inclusion in conclusion text."""
        if not factors:
            return "indicadores no especificados"
        
        names = [f['display_name'].lower() for f in factors[:3]]
        if len(names) == 1:
            return names[0]
        elif len(names) == 2:
            return f"{names[0]} y {names[1]}"
        else:
            return ", ".join(names[:-1]) + f" y {names[-1]}"
    
    @staticmethod
    def _get_iso_timestamp() -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
