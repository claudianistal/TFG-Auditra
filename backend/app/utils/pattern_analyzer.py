"""
Pattern analysis module for binary audio file visualization and inspection.

This module provides utilities to:
1. Generate bitmap visualization of file contents (autosimilitude)
2. Extract hex dumps of file start and end bytes (padding detection)
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import base64
import io
from typing import Dict, List, Tuple


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
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise ValueError(f"File not found: {file_path}")
    
    # Read raw bytes
    with open(file_path, 'rb') as f:
        data = f.read()
    
    total_size = len(data)
    
    if total_size == 0:
        raise ValueError("File is empty")
    
    # Calculate dimensions
    height = total_size // width
    
    if height == 0:
        raise ValueError(f"File too small for width {width}. Minimum bytes: {width}")
    
    # Reshape to matrix (truncate if needed)
    data_array = np.frombuffer(data[:width * height], dtype=np.uint8)
    matrix = data_array.reshape((height, width))
    
    # Create figure and render as grayscale bitmap
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)
    
    im = ax.imshow(
        matrix,
        cmap='gray',
        aspect='auto',
        interpolation='nearest',
        vmin=0,
        vmax=255
    )
    
    ax.set_title(f"Binary Content Visualization: {file_path.name}")
    ax.set_xlabel(f"Bytes per row: {width}")
    ax.set_ylabel("Rows (blocks)")
    
    cbar = plt.colorbar(im, ax=ax, label='Byte Value (0-255)')
    
    # Save to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf.getvalue()


def extract_hex_dumps(file_path: str, num_bytes: int = 1024) -> Dict[str, List[str]]:
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
            "hex_end": [list of hex dump lines]
        }
        
    Raises:
        ValueError: If file cannot be read
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise ValueError(f"File not found: {file_path}")
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    if len(data) == 0:
        raise ValueError("File is empty")
    
    # Extract start and end
    start_bytes = data[:num_bytes]
    end_bytes = data[-num_bytes:] if len(data) >= num_bytes else data
    
    hex_start = _format_hex_dump(start_bytes, label="Start of file")
    hex_end = _format_hex_dump(end_bytes, label="End of file", offset=max(0, len(data) - num_bytes))
    
    return {
        "hex_start": hex_start,
        "hex_end": hex_end,
        "total_file_size": len(data),
    }


def _format_hex_dump(data: bytes, label: str = "", offset: int = 0) -> List[str]:
    """
    Format bytes as a classic hex dump with ASCII representation.
    
    Example output:
        00000000: 49 44 33 04 00 00 00 00  07 80 54 49 54 32 00 00  |ID3.......TIT2..|
        00000010: 00 31 00 01 FF FE 00 53  00 6F 00 6E 00 67 20 00  |.1.....S.o.n.g .|
    
    Args:
        data (bytes): Raw bytes to format
        label (str): Optional label for the section
        offset (int): Starting offset for address display
        
    Returns:
        list: Lines of formatted hex dump
    """
    lines = []
    
    if label:
        lines.append(f"\n{label} (offset 0x{offset:08x}):")
        lines.append("-" * 76)
    
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        hex_part = " ".join(f"{byte:02x}" for byte in chunk)
        
        # Add spacing in middle of hex block
        if len(chunk) == 16:
            hex_part = hex_part[:24] + "  " + hex_part[24:]
        
        # ASCII representation
        ascii_part = "".join(
            chr(byte) if 32 <= byte < 127 else "."
            for byte in chunk
        )
        
        addr = offset + i
        line = f"{addr:08x}: {hex_part:<48} |{ascii_part}|"
        lines.append(line)
    
    return lines
