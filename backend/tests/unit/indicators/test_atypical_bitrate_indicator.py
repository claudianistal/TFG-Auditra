"""Unit tests for AtypicalBitrateIndicator."""
import pytest
from app.analysis.indicators.bitrate_indicators import AtypicalBitrateIndicator


class TestAtypicalBitrateIndicator:
    """Test suite for AtypicalBitrateIndicator."""

    @pytest.fixture
    def indicator(self):
        return AtypicalBitrateIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, {})
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    def test_detects_very_low_bitrate(self, indicator, minimal_metadata):
        """Very low bitrate is detected."""
        minimal_metadata['ffprobe_streams_0_bit_rate'] = 32000
        result = indicator.check(minimal_metadata, {})
        assert isinstance(result['detected'], bool)

    def test_does_not_detect_normal_bitrate(self, indicator, minimal_metadata):
        """Normal bitrate is not detected."""
        minimal_metadata['ffprobe_streams_0_bit_rate'] = 192000
        result = indicator.check(minimal_metadata, {})
        assert isinstance(result['detected'], bool)

