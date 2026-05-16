"""Unit tests for CodecConsistencyIndicator."""
import pytest
from app.analysis.indicators.codec_indicators import CodecConsistencyIndicator


class TestCodecConsistencyIndicator:
    """Test suite for CodecConsistencyIndicator."""

    @pytest.fixture
    def indicator(self):
        return CodecConsistencyIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, {})
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    def test_detects_codec_mismatch_mp3(self, indicator, minimal_metadata):
        """Codec mismatch detected."""
        minimal_metadata['file_format'] = 'mp3'
        minimal_metadata['ffprobe_streams_0_codec_name'] = 'aac'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is True

    def test_does_not_detect_matching_codec_mp3(self, indicator, minimal_metadata):
        """Matching codec not detected."""
        minimal_metadata['file_format'] = 'mp3'
        minimal_metadata['ffprobe_streams_0_codec_name'] = 'mp3'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is False

    def test_does_not_detect_matching_codec_wav(self, indicator, minimal_metadata):
        """Matching codec not detected."""
        minimal_metadata['file_format'] = 'wav'
        minimal_metadata['ffprobe_streams_0_codec_name'] = 'pcm_s16le'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is False
        
    def test_detects_codec_mismatch_wav(self, indicator, minimal_metadata):
        """Codec mismatch detected."""
        minimal_metadata['file_format'] = 'wav'
        minimal_metadata['ffprobe_streams_0_codec_name'] = 'mp3'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is True
    
    def test_detects_codec_mismatch_m4a(self, indicator, minimal_metadata):
        """Codec mismatch detected."""
        minimal_metadata['file_format'] = 'm4a'
        minimal_metadata['ffprobe_streams_0_codec_name'] = 'mp3'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is True


    def test_does_not_detect_matching_codec_m4a(self, indicator, minimal_metadata):
        """Matching codec not detected."""
        minimal_metadata['file_format'] = 'm4a'
        minimal_metadata['ffprobe_streams_0_codec_name'] = 'aac'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is False

