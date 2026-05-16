"""Unit tests for AIDetectionAnalyzer module."""
import pytest
from app.analysis.analyzer import AIDetectionAnalyzer


class TestAIDetectionAnalyzer:
    """Test suite for AIDetectionAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Create a fresh analyzer instance."""
        return AIDetectionAnalyzer()

    def test_analyze_returns_dict_with_required_keys(self, analyzer, minimal_metadata, minimal_patterns):
        """Analyze returns dict with all required keys."""
        result = analyzer.analyze(minimal_metadata, minimal_patterns)
        required_keys = {
            'risk_score', 'likelihood', 'likelihood_description', 'score_color',
            'detected_factors', 'missing_factors', 'all_indicators',
            'conclusion_key', 'recommendations', 'analysis_date'
        }
        assert set(result.keys()) == required_keys

    def test_analyze_risk_score_in_valid_range(self, analyzer, minimal_metadata, minimal_patterns):
        """Risk score is always between 0 and 100."""
        result = analyzer.analyze(minimal_metadata, minimal_patterns)
        assert isinstance(result['risk_score'], int)
        assert 0 <= result['risk_score'] <= 100

    def test_analyze_detected_plus_missing_equals_all(self, analyzer, minimal_metadata, minimal_patterns):
        """detected + missing indicators = all indicators."""
        result = analyzer.analyze(minimal_metadata, minimal_patterns)
        detected_count = len(result['detected_factors'])
        missing_count = len(result['missing_factors'])
        total_count = len(result['all_indicators'])
        assert detected_count + missing_count == total_count

    def test_analyze_ai_generated_has_detected_factors(self, analyzer, ai_generated_metadata, patterns_with_padding):
        """AI-generated audio detection produces detected factors."""
        result = analyzer.analyze(ai_generated_metadata, patterns_with_padding)
        assert len(result['detected_factors']) > 0
        assert result['risk_score'] > 30

    def test_analyze_natural_audio_low_risk(self, analyzer, natural_audio_metadata, minimal_patterns):
        """Natural audio has low risk score."""
        result = analyzer.analyze(natural_audio_metadata, minimal_patterns)
        assert result['risk_score'] < 70

    def test_analyze_recommendations_generated(self, analyzer, ai_generated_metadata, patterns_with_padding):
        """Recommendations are generated for detected factors."""
        result = analyzer.analyze(ai_generated_metadata, patterns_with_padding)
        if len(result['detected_factors']) > 0:
            assert isinstance(result['recommendations'], list)
            assert len(result['recommendations']) > 0


    def test_full_analysis_with_ai_metadata_produces_high_score(self, analyzer, ai_generated_metadata, patterns_with_padding):
        """Integration test: AI metadata should produce elevated risk score."""
        result = analyzer.analyze(ai_generated_metadata, patterns_with_padding)
        # AI metadata + padding patterns should result in high risk
        assert result['risk_score'] >= 30
        assert result['likelihood'] in ['medio', 'alto']

    def test_full_analysis_with_natural_metadata_produces_low_score(self, analyzer, natural_audio_metadata, minimal_patterns):
        """Integration test: Natural audio metadata should produce low risk score."""
        result = analyzer.analyze(natural_audio_metadata, minimal_patterns)
        # Natural metadata should result in low/medium risk
        assert result['risk_score'] < 60
        assert result['likelihood'] in ['bajo', 'medio']

    def test_analyze_result_is_consistent(self, analyzer, minimal_metadata, minimal_patterns):
        """Test that multiple calls with same input produce same result."""
        result1 = analyzer.analyze(minimal_metadata, minimal_patterns)
        result2 = analyzer.analyze(minimal_metadata, minimal_patterns)
        # Results should be identical
        assert result1['risk_score'] == result2['risk_score']
        assert result1['likelihood'] == result2['likelihood']
        assert len(result1['all_indicators']) == len(result2['all_indicators'])
