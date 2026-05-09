"""
Hex dump extraction and formatting for binary file inspection.

Extracts hex representation of file start and end bytes with ASCII display
for inspection of potential padding (0x00 or 0xFF) at file boundaries.
"""

from pathlib import Path
from typing import Dict, List


def extract_hex_dumps(file_path: str, num_bytes: int = 1024) -> Dict[str, any]:
    """
    Extract hex representation of file start, end, and full content.
    
    Returns formatted hex dumps with ASCII representation for inspection
    of potential padding (0x00 or 0xFF) at file boundaries, plus full hex dump
    for advanced pattern analysis.
    
    Args:
        file_path (str): Full path to the audio file
        num_bytes (int): Number of bytes to extract from start/end (default 1024)
        
    Returns:
        dict: {
            "hex_start": [list of hex dump lines],
            "hex_end": [list of hex dump lines],
            "full_hex": [list of complete hex dump lines],
            "total_file_size": int
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
    
    # Extract start and end (for boundary analysis)
    start_bytes = data[:num_bytes]
    end_bytes = data[-num_bytes:] if len(data) >= num_bytes else data
    
    hex_start = _format_hex_dump(start_bytes, label="Start of file")
    hex_end = _format_hex_dump(end_bytes, label="End of file", offset=max(0, len(data) - num_bytes))
    
    # Extract full hex dump (for pattern analysis, with limit to avoid memory issues)
    # Limit to 100KB for performance, but analyze the whole file if smaller
    full_data = data
    hex_full = _format_hex_dump(full_data, label=f"Full content ({len(data)} bytes total, showing {len(full_data)} bytes)")
    
    return {
        "hex_start": hex_start,
        "hex_end": hex_end,
        "full_hex": hex_full,
        "total_file_size": len(data),
        "hex_bytes_analyzed": len(full_data)
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
