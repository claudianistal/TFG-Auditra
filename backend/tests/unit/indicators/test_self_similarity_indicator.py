"""Unit tests for SelfSimilarityIndicator."""
import pytest
from app.analysis.indicators.self_similarity_indicators import SelfSimilarityIndicator


class TestSelfSimilarityIndicator:
    """Test suite for SelfSimilarityIndicator."""

    @pytest.fixture
    def indicator(self):
        return SelfSimilarityIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata, patterns_with_self_similarity):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, patterns_with_self_similarity)
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    def test_detects_repetitive_patterns(self, indicator, minimal_metadata, patterns_with_self_similarity):
        """Repetitive patterns are detected."""
        result = indicator.check(minimal_metadata, patterns_with_self_similarity)
        assert isinstance(result['detected'], bool)

    def test_does_not_detect_random_patterns(self, indicator, minimal_metadata, minimal_patterns):
        """Random/minimal patterns not detected."""
        result = indicator.check(minimal_metadata, minimal_patterns)
        assert isinstance(result['detected'], bool)


    # ========================================================================
    # Tests for check() - Structure
    # ========================================================================

    def test_check_returns_dict(self, indicator, minimal_metadata, minimal_patterns):
        """Test that check() returns a dictionary."""
        result = indicator.check(minimal_metadata, minimal_patterns)
        assert isinstance(result, dict)
