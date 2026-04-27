"""
Indicators package - Central registry of AI detection indicators.

Simplified to 6 key metrics:
1. Encoding Library (weight: 90) - Lavf/FFmpeg detection
2. Audio Channels (weight: 40) - Mono audio detection
3. Padding Pattern (weight: 85) - Zero padding detection
4. Timestamp Consistency (weight: 20) - Creation vs modification date
5. Codec Consistency (weight: 20) - Codec matches format
6. File Size (weight: variable) - Bitrate × duration verification
"""
from .encoding_indicators import EncodingLibraryIndicator
from .audio_indicators import MonoAudioIndicator
from .padding_indicators import PaddingPatternIndicator
from .timestamp_indicators import TimestampConsistencyIndicator
from .codec_indicators import CodecConsistencyIndicator
from .size_indicators import FileSizeIndicator

# Central registry of indicators - simplified to 6 key metrics
INDICATORS = [
    # ALTA PRIORITY (weight 85+)
    PaddingPatternIndicator(),          # weight: 85
    EncodingLibraryIndicator(),         # weight: 90
    
    # MEDIA PRIORITY (weight 40)
    MonoAudioIndicator(),               # weight: 40
    
    # BAJA PRIORITY (weight 20)
    TimestampConsistencyIndicator(),    # weight: 20
    CodecConsistencyIndicator(),        # weight: 20
    
    # VARIABLE PRIORITY
    FileSizeIndicator(),                # weight: 20-50 (depends on deviation)
]

__all__ = [
    'EncodingLibraryIndicator',
    'MonoAudioIndicator',
    'PaddingPatternIndicator',
    'TimestampConsistencyIndicator',
    'CodecConsistencyIndicator',
    'FileSizeIndicator',
    'INDICATORS',
]
