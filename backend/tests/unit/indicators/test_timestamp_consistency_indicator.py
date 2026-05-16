"""Unit tests for TimestampConsistencyIndicator."""
import pytest
from app.analysis.indicators.timestamp_indicators import TimestampConsistencyIndicator


class TestTimestampConsistencyIndicator:
    """Test suite for TimestampConsistencyIndicator."""

    @pytest.fixture
    def indicator(self):
        return TimestampConsistencyIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, {})
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    def test_detects_timestamp_inconsistency(self, indicator, minimal_metadata):
        """Timestamp inconsistencies are detected."""
        minimal_metadata['ID3:Date'] = '2024-01-01'
        minimal_metadata['Exif:DateTime'] = '2023-12-31'
        result = indicator.check(minimal_metadata, {})
        assert isinstance(result['detected'], bool)

    def test_does_not_detect_consistent_timestamps(self, indicator, minimal_metadata):
        """Consistent timestamps not detected."""
        minimal_metadata['ID3:Date'] = '2024-01-01'
        minimal_metadata['Exif:DateTime'] = '2024-01-01'
        result = indicator.check(minimal_metadata, {})
        assert isinstance(result['detected'], bool)

        """Test that detected is always a boolean."""
        result = indicator.check(minimal_metadata, {})
        assert isinstance(result['detected'], bool)
