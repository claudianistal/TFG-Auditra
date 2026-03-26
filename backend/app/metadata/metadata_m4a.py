import struct
from mutagen.mp4 import MP4
from .metadata_base import BaseExtractor
from typing import Dict, Any

class M4AExtractor(BaseExtractor):
    def extract_specific_metadata(self) -> Dict[str, Any]:
        raw_data = {}

        # 1. High-level Metadata (iTunes Atoms) via Mutagen
        try:
            audio = MP4(str(self.file_path))
            for atom_key, value in audio.items():
                raw_data[f"MPEG4_tag_{atom_key}"] = str(value)
            
            if audio.info:
                for attr in dir(audio.info):
                    if not attr.startswith('_') and not callable(getattr(audio.info, attr)):
                        raw_data[f"stream_{attr}"] = getattr(audio.info, attr)
        except Exception as e:
            raw_data["mpeg4_parsing_error"] = str(e)

        # 2. Binary Atom Structure Analysis
        # Essential for detecting 'moov' vs 'mdat' order (Forensic indicator)
        try:
            raw_data["container_layout"] = self._parse_atoms()
        except Exception as e:
            raw_data["atom_structure_error"] = str(e)

        return raw_data

    def _parse_atoms(self) -> list:
        """
        Linearly scans the file to map top-level MPEG-4 boxes.
        Standard iPhone recordings usually place 'moov' after 'mdat'.
        """
        atoms = []
        file_size = self.file_path.stat().st_size
        
        with open(self.file_path, 'rb') as f:
            offset = 0
            while offset < file_size:
                f.seek(offset)
                header = f.read(8)
                if len(header) < 8:
                    break
                
                # Unpack 4 bytes for size and decode 4 bytes for type (ASCII)
                size = struct.unpack('>I', header[0:4])[0]
                atom_type = header[4:8].decode('ascii', errors='ignore')
                
                # Handle 64-bit large atoms (co64)
                if size == 1:
                    size = struct.unpack('>Q', f.read(8))[0]
                elif size == 0: 
                    # Extends to the end of the file
                    size = file_size - offset

                atoms.append({
                    "atom": atom_type,
                    "offset_hex": hex(offset),
                    "size_bytes": size
                })
                
                if size <= 0: break
                offset += size
                
        return atoms