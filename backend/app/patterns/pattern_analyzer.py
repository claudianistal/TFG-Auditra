"""
Pattern analysis for binary audio file visualization and inspection.

Provides utilities for:
1. Bitmap visualization of file contents (autosimilitude detection)
2. Hex dump extraction of file boundaries (padding detection)
"""

from .bitmap import generate_bitmap as _generate_bitmap
from .hex_dump import extract_hex_dumps as _extract_hex_dumps


class PatternAnalyzer:
    """
    Analyzer for binary patterns in audio files.
    
    Provides static methods for generating bitmap visualizations and
    extracting hex dumps for forensic inspection of audio file contents.
    """
    
    @staticmethod
    def generate_bitmap(file_path: str, width: int = 512) -> bytes:
        """
        Generate a bitmap visualization of audio file binary content.
        
        Reads the file as raw bytes, reshapes into a matrix, and creates
        a grayscale image where each pixel represents one byte value (0-255).
        This visualization reveals patterns in the audio data (autosimilitude).
        
        Args:
            file_path (str): Full path to the audio file
            width (int): Width of the bitmap in bytes (default 512)
            
        Returns:
            bytes: PNG image data (can be encoded to base64 for JSON)
            
        Raises:
            ValueError: If file is too small or cannot be read
        """
        return _generate_bitmap(file_path, width)
    
    @staticmethod
    def extract_hex_dumps(file_path: str, num_bytes: int = 1024) -> dict:
        """
        Extract hex representation of file start and end bytes.
        
        Returns formatted hex dumps with ASCII representation for inspection
        of potential padding (0x00 or 0xFF) at file boundaries.
        
        Args:
            file_path (str): Full path to the audio file
            num_bytes (int): Number of bytes to extract from start/end (default 1024)
            
        Returns:
            dict: {
                "hex_start": [list of hex dump lines],
                "hex_end": [list of hex dump lines],
                "total_file_size": int
            }
            
        Raises:
            ValueError: If file cannot be read
        """
        return _extract_hex_dumps(file_path, num_bytes)
