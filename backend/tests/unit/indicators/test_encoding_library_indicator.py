"""Unit tests for EncodingLibraryIndicator."""
import pytest
from app.analysis.indicators.encoding_indicators import EncodingLibraryIndicator


class TestEncodingLibraryIndicator:
    """Test suite for EncodingLibraryIndicator class."""

    @pytest.fixture
    def indicator(self):
        return EncodingLibraryIndicator()

    def test_returns_required_structure(self, indicator, minimal_metadata):
        """Check result has required keys."""
        result = indicator.check(minimal_metadata, {})
        assert set(result.keys()) == {'detected', 'details', 'reasoning_key'}

    # Detección: Librerías sospechosas (FFmpeg, Lavf)
    def test_detects_ffmpeg_mp3(self, indicator, minimal_metadata):
        """Detecta FFmpeg encoder en MP3 (típico de IA)."""
        minimal_metadata['ffprobe_format_format_name'] = 'mp3'
        minimal_metadata['Exif:Encoding Library'] = 'FFmpeg/libavformat'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is True

    def test_detects_lavf_m4a(self, indicator, minimal_metadata):
        """Detecta Lavf encoder en M4A."""
        minimal_metadata['ffprobe_format_format_name'] = 'm4a'
        minimal_metadata['Ffprobe_format_encoder'] = 'Lavf/58.76.100'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is True

    def test_detects_libav_wav(self, indicator, minimal_metadata):
        """Detecta libav encoder en WAV."""
        minimal_metadata['ffprobe_format_format_name'] = 'wav'
        minimal_metadata['Ffprobe_format_encoder'] = 'libavcodec'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is True

    # No detección: Librerías normales
    def test_does_not_detect_audacity_mp3(self, indicator, minimal_metadata):
        """Audacity encoder en MP3 es normal."""
        minimal_metadata['ffprobe_format_format_name'] = 'mp3'
        minimal_metadata['Exif:Encoding Library'] = 'Audacity'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is False

    def test_does_not_detect_apple_m4a(self, indicator, minimal_metadata):
        """Apple encoder en M4A es normal."""
        minimal_metadata['ffprobe_format_format_name'] = 'm4a'
        minimal_metadata['Ffprobe_format_encoder'] = 'aac'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is False

    def test_does_not_detect_standard_wav(self, indicator, minimal_metadata):
        """Encoder estándar en WAV."""
        minimal_metadata['ffprobe_format_format_name'] = 'wav'
        minimal_metadata['Ffprobe_format_encoder'] = 'pcm'
        result = indicator.check(minimal_metadata, {})
        assert result['detected'] is False

