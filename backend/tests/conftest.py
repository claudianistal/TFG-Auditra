"""
Pytest configuration and shared fixtures for analysis module tests.
"""
import pytest
from typing import Dict, Any, List


# ============================================================================
# METADATA FIXTURES
# ============================================================================

@pytest.fixture
def minimal_metadata() -> Dict[str, Any]:
    """Minimal valid metadata dictionary."""
    return {
        'file_size_bytes': 1000000,
        'file_format': 'mp3',
        'ffprobe_format_duration': 10.0,
        'ffprobe_streams_0_bit_rate': 128000,
        'ffprobe_streams_0_channels': 2,
        'ffprobe_streams_0_codec_name': 'mp3',
        'ffprobe_streams_0_sample_rate': 44100,
        'Exif:Encoding Library': '',
        'Ffprobe_format_encoder': '',
        'ID3 TSSE': '',
    }


@pytest.fixture
def ai_generated_metadata() -> Dict[str, Any]:
    """Metadata with characteristics typical of AI-generated audio."""
    return {
        'file_size_bytes': 500000,
        'file_format': 'mp3',
        'ffprobe_format_duration': 15.000,  # Exact second
        'ffprobe_streams_0_bit_rate': 32000,  # Very low bitrate (TTS/API typical)
        'ffprobe_streams_0_channels': 1,  # Mono (common in AI)
        'ffprobe_streams_0_codec_name': 'mp3',
        'ffprobe_streams_0_sample_rate': 16000,  # AI-typical sample rate
        'Exif:Encoding Library': 'Lavf/FFmpeg',  # Suspicious encoder
        'Ffprobe_format_encoder': 'Lavf56.40.101',
        'ID3 TSSE': 'Lavf/FFmpeg 4.2.4',
        'stream_encoder': 'ffmpeg',
    }


@pytest.fixture
def natural_audio_metadata() -> Dict[str, Any]:
    """Metadata of naturally recorded audio."""
    return {
        'file_size_bytes': 5000000,
        'file_format': 'wav',
        'ffprobe_format_duration': 23.456,  # Irregular duration
        'ffprobe_streams_0_bit_rate': 1411000,  # CD-quality WAV
        'ffprobe_streams_0_channels': 2,
        'ffprobe_streams_0_codec_name': 'pcm_s16le',
        'ffprobe_streams_0_sample_rate': 44100,
        'Exif:Encoding Library': 'Audacity 3.2.0',
        'Ffprobe_format_encoder': 'pcm',
        'ID3 TSSE': '',
    }


@pytest.fixture
def m4a_metadata() -> Dict[str, Any]:
    """Metadata for M4A audio file."""
    return {
        'file_size_bytes': 800000,
        'file_format': 'm4a',
        'ffprobe_format_duration': 30.5,
        'ffprobe_streams_0_bit_rate': 128000,
        'ffprobe_streams_0_channels': 2,
        'ffprobe_streams_0_codec_name': 'aac',
        'ffprobe_streams_0_sample_rate': 48000,
        'Exif:Encoding Library': '',
        'Ffprobe_format_encoder': 'Apple CoreAudio AAC encoder',
        'ffprobe_format_format_name': 'm4a',
    }


@pytest.fixture
def edge_case_metadata() -> Dict[str, Any]:
    """Metadata with edge cases: missing or extreme values."""
    return {
        'file_size_bytes': 0,
        'file_format': '',
        'ffprobe_format_duration': None,
        'ffprobe_streams_0_bit_rate': 0,
        'ffprobe_streams_0_channels': 0,
        'ffprobe_streams_0_codec_name': '',
        'ffprobe_streams_0_sample_rate': 0,
        'Exif:Encoding Library': None,
    }


# ============================================================================
# PATTERNS FIXTURES (HEX DUMP DATA)
# ============================================================================

@pytest.fixture
def minimal_patterns() -> Dict[str, Any]:
    """Minimal valid patterns dictionary."""
    return {
        'full_hex': '00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F',
        'hex_start': '00 01 02 03 04 05 06 07',
        'hex_end': '08 09 0A 0B 0C 0D 0E 0F',
        'total_file_size': 1000000,
    }


@pytest.fixture
def patterns_with_padding() -> Dict[str, Any]:
    """Patterns containing excessive padding (0x00, 0xFF sequences)."""
    # Simulates 100 consecutive 0x00 bytes (> MIN_CONSECUTIVE_BYTES=70)
    padding_hex = ' '.join(['00'] * 100)
    return {
        'full_hex': f"{padding_hex} FF 01 02 03 04 05",
        'hex_start': '00 ' * 50,
        'hex_end': '00 ' * 50,
        'total_file_size': 1000000,
    }


@pytest.fixture
def patterns_with_self_similarity() -> Dict[str, Any]:
    """Patterns with repetitive byte sequences (self-similarity)."""
    # Create a pattern that repeats: AA BB CC DD
    repeating_pattern = ' '.join(['AA', 'BB', 'CC', 'DD'] * 100)
    return {
        'full_hex': repeating_pattern,
        'hex_start': 'AA BB CC DD ' * 50,
        'hex_end': 'AA BB CC DD ' * 50,
        'total_file_size': 1000000,
    }


@pytest.fixture
def empty_patterns() -> Dict[str, Any]:
    """Patterns with empty/null values."""
    return {
        'full_hex': '',
        'hex_start': [],
        'hex_end': [],
        'total_file_size': 0,
    }


@pytest.fixture
def complex_hex_dump_with_addresses() -> Dict[str, Any]:
    """Realistic hex dump with address column and ASCII representation."""
    hex_dump = """00000000: FF FB 90 64 49 6E 66 6F 00 00 00 0F 00 00 00 1A  |.........I.nf...|
00000010: 00 00 00 24 00 00 00 14 00 00 00 23 00 00 1E 7F  |...$......#.....|
00000020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  |................|
00000030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  |................|"""
    return {
        'full_hex': hex_dump,
        'hex_start': '00000000: FF FB 90 64 49 6E 66 6F',
        'hex_end': '00000030: 00 00 00 00 00 00 00 00',
        'total_file_size': 50000,
    }


# ============================================================================
# INDICATOR RESULTS FIXTURES
# ============================================================================

@pytest.fixture
def detected_indicator() -> Dict[str, Any]:
    """A single detected indicator result."""
    return {
        'name': 'test_indicator',
        'display_name': 'Test Indicator',
        'category': 'test',
        'weight': 30,
        'detected': True,
        'risk_level': 'medium',
        'reasoning_key': 'indicators.test.reasoning',
        'details': {'test_detail': 'value'},
    }


@pytest.fixture
def not_detected_indicator() -> Dict[str, Any]:
    """A single non-detected indicator result."""
    return {
        'name': 'test_indicator',
        'display_name': 'Test Indicator',
        'category': 'test',
        'weight': 30,
        'detected': False,
        'risk_level': 'low',
        'reasoning_key': 'indicators.test.reasoning',
        'details': {},
    }


@pytest.fixture
def high_risk_indicator() -> Dict[str, Any]:
    """High-risk detected indicator."""
    return {
        'name': 'padding_pattern',
        'display_name': 'Suspicious Padding',
        'category': 'padding',
        'weight': 85,
        'detected': True,
        'risk_level': 'high',
        'reasoning_key': 'indicators.padding_pattern.reasoning',
        'details': {
            'max_consecutive_sequence': 150,
            'total_repetitive_bytes': 5000,
            'padding_percentage': 5.2,
        },
    }


# ============================================================================
# SCORE FIXTURES
# ============================================================================

@pytest.fixture
def low_risk_score_factors() -> List[Dict[str, Any]]:
    """Factors that result in low risk score (<30)."""
    return [
        {
            'name': 'mono_audio',
            'weight': 15,
            'detected': True,
            'risk_level': 'low',
            'details': {'channels': 1},
        }
    ]


@pytest.fixture
def medium_risk_score_factors() -> List[Dict[str, Any]]:
    """Factors that result in medium risk score (30-59)."""
    return [
        {
            'name': 'mono_audio',
            'weight': 15,
            'detected': True,
            'risk_level': 'low',
            'details': {},
        },
        {
            'name': 'encoding_library',
            'weight': 40,
            'detected': True,
            'risk_level': 'medium',
            'details': {},
        },
    ]


@pytest.fixture
def high_risk_score_factors() -> List[Dict[str, Any]]:
    """Factors that result in high risk score (>=60)."""
    return [
        {
            'name': 'encoding_library',
            'weight': 40,
            'detected': True,
            'risk_level': 'medium',
            'details': {},
        },
        {
            'name': 'padding_pattern',
            'weight': 50,
            'detected': True,
            'risk_level': 'high',
            'details': {},
        },
        {
            'name': 'mono_audio',
            'weight': 15,
            'detected': True,
            'risk_level': 'low',
            'details': {},
        },
    ]


@pytest.fixture
def multiple_high_risk_factors() -> List[Dict[str, Any]]:
    """Multiple high-risk factors that exceed 100."""
    return [
        {'name': 'encoding_library', 'weight': 40, 'detected': True, 'risk_level': 'medium', 'details': {}},
        {'name': 'padding_pattern', 'weight': 50, 'detected': True, 'risk_level': 'high', 'details': {}},
        {'name': 'self_similarity', 'weight': 70, 'detected': True, 'risk_level': 'high', 'details': {}},
    ]


# ============================================================================
# ANALYSIS RESULTS FIXTURES
# ============================================================================

@pytest.fixture
def mock_analysis_result() -> Dict[str, Any]:
    """Mock complete analysis result."""
    return {
        'risk_score': 45,
        'likelihood': 'medio',
        'likelihood_description': 'Riesgo medio de generación por IA',
        'score_color': 'yellow',
        'detected_factors': [
            {
                'name': 'mono_audio',
                'display_name': 'Audio en mono',
                'category': 'audio',
                'weight': 15,
                'detected': True,
                'risk_level': 'low',
                'reasoning_key': 'indicators.mono_audio.reasoning',
                'details': {'channels': 1},
            }
        ],
        'missing_factors': [],
        'all_indicators': [],
        'conclusion_key': 'conclusions.medium_risk',
        'recommendations': ['recommendations.mono_audio'],
        'analysis_date': '2026-05-16T12:00:00Z',
    }
