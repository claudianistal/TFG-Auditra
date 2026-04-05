"""
Pattern analysis module for binary audio file visualization and inspection.

Provides utilities to:
1. Generate bitmap visualization of file contents (autosimilitude)
2. Extract hex dumps of file start and end bytes (padding detection)
"""

from .pattern_analyzer import PatternAnalyzer

__all__ = ["PatternAnalyzer"]
