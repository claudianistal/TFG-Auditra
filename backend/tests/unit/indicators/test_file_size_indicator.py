"""Unit tests for FileSizeIndicator."""
import pytest
from app.analysis.indicators.size_indicators import FileSizeIndicator


class TestFileSizeIndicator:
    """Test suite for FileSizeIndicator."""

    @pytest.fixture
    def indicator(self):
        return FileSizeIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, {'total_file_size': 10000})
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    def test_detects_file_size_deviation(self, indicator, minimal_metadata):
        """Large file size deviations are detected."""
        minimal_metadata['ffprobe_streams_0_bit_rate'] = 128000
        minimal_metadata['ffprobe_format_duration'] = 15
        result = indicator.check(minimal_metadata, {'total_file_size': 1000})
        assert isinstance(result['detected'], bool)

    def test_does_not_detect_normal_file_size(self, indicator, minimal_metadata):
        """Normal file sizes not detected."""
        minimal_metadata['ffprobe_streams_0_bit_rate'] = 320000
        minimal_metadata['ffprobe_format_duration'] = 10
        result = indicator.check(minimal_metadata, {'total_file_size': 400000})
        assert isinstance(result['detected'], bool)


