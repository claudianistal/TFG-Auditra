"""Unit tests for MonoAudioIndicator."""
import pytest
from app.analysis.indicators.audio_indicators import MonoAudioIndicator


class TestMonoAudioIndicator:
    """Test suite for MonoAudioIndicator."""

    @pytest.fixture
    def indicator(self):
        return MonoAudioIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, {})
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    def test_detects_mono_audio(self, indicator, minimal_metadata):
        """Mono (1 channel) is detected."""
        minimal_metadata['ffprobe_streams_0_channels'] = 1
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is True

    def test_does_not_detect_stereo_audio(self, indicator, minimal_metadata):
        """Stereo (2 channels) is not detected."""
        minimal_metadata['ffprobe_streams_0_channels'] = 2
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is False




    # ========================================================================
    # Tests for check() - Missing or invalid data
    # ========================================================================

    def test_check_with_missing_channels_field(self, indicator, minimal_metadata):
        """Test check when channels field is missing."""
        del minimal_metadata['ffprobe_streams_0_channels']
        result = indicator.check(minimal_metadata, {})
        # Should handle gracefully, default to 0 (not mono)
        assert result['detected'] is False
