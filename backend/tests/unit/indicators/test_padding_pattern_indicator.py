"""Unit tests for PaddingPatternIndicator."""
import pytest
from app.analysis.indicators.padding_indicators import PaddingPatternIndicator


class TestPaddingPatternIndicator:
    """Test suite for PaddingPatternIndicator."""

    @pytest.fixture
    def indicator(self):
        return PaddingPatternIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, {'padding_bytes': []})
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    def test_detects_padding_with_fixture(self, indicator, minimal_metadata, patterns_with_padding):
        """Detects padding when using patterns fixture."""
        result = indicator.check(minimal_metadata, patterns_with_padding)
        assert result['detected'] is True

    def test_does_not_detect_minimal_patterns(self, indicator, minimal_metadata, minimal_patterns):
        """No detection with minimal patterns."""
        result = indicator.check(minimal_metadata, minimal_patterns)
        assert result['detected'] is False
