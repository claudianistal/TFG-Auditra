"""
Indicators package - Central registry of AI detection indicators.
"""
from .encoding_indicators import EncodingLibraryIndicator
from .audio_indicators import MonoAudioIndicator
from .padding_indicators import PaddingPatternIndicator
from .timestamp_indicators import TimestampConsistencyIndicator
from .codec_indicators import CodecConsistencyIndicator
from .size_indicators import FileSizeIndicator
from .self_similarity_indicators import SelfSimilarityIndicator

# Central registry of indicators - simplified to 7 key metrics
INDICATORS = [
    # ALTA PRIORITY (weight 85+)
    EncodingLibraryIndicator(),         # weight: 90
    PaddingPatternIndicator(),          # weight: 85
    
    # ALTA-MEDIA PRIORITY (weight 70-75)
    SelfSimilarityIndicator(),          # weight: 70
    
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
    'SelfSimilarityIndicator',
    'INDICATORS',
]
