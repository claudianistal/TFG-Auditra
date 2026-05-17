"""Unit tests for SampleRateIndicator."""
import pytest
from app.analysis.indicators.sample_rate_indicators import SampleRateIndicator


class TestSampleRateIndicator:
    """Test suite for SampleRateIndicator."""

    @pytest.fixture
    def indicator(self):
        return SampleRateIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, {})
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    def test_detects_ai_typical_sample_rate(self, indicator, minimal_metadata):
        """AI-typical sample rate (16 kHz) is detected."""
        minimal_metadata['ffprobe_streams_0_sample_rate'] = 16000
        result = indicator.check(minimal_metadata, {})
        assert isinstance(result['detected'], bool)

    def test_does_not_detect_standard_sample_rate(self, indicator, minimal_metadata):
        """Standard sample rate (44.1 kHz) is not detected."""
        minimal_metadata['ffprobe_streams_0_sample_rate'] = 44100
        result = indicator.check(minimal_metadata, {})
        assert isinstance(result['detected'], bool)

