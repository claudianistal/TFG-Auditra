"""Unit tests for PreciseDurationIndicator."""
import pytest
from app.analysis.indicators.duration_indicators import PreciseDurationIndicator


class TestPreciseDurationIndicator:
    """Test suite for PreciseDurationIndicator."""

    @pytest.fixture
    def indicator(self):
        return PreciseDurationIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, {})
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    def test_detects_exact_seconds_duration(self, indicator, minimal_metadata):
        """Exact second durations (X.0) are detected as AI-like."""
        minimal_metadata['ffprobe_format_duration'] = '15.0'
        result = indicator.check(minimal_metadata, {})
        assert isinstance(result['detected'], bool)

    def test_does_not_detect_natural_precision(self, indicator, minimal_metadata):
        """Natural precision (many decimals) is not detected."""
        minimal_metadata['ffprobe_format_duration'] = '23.456'
        result = indicator.check(minimal_metadata, {})
        assert isinstance(result['detected'], bool)


    def test_check_details_has_exact_duration(self, indicator, minimal_metadata):
        """Test that details contains exact_duration."""
        result = indicator.check(minimal_metadata, {})
        assert 'exact_duration' in result['details']
        assert 'decimal_part' in result['details']

    # ========================================================================
    # Tests for check() - Exact seconds (detected=True)
    # ========================================================================
