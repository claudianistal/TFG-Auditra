"""
Bitmap visualization of binary audio file content.

Reads raw bytes and creates grayscale image visualization where each pixel
represents one byte value (0-255). This reveals patterns in audio data.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import io


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
