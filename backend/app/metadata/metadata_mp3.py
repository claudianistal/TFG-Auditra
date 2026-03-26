from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from .metadata_base import BaseExtractor
from typing import Dict, Any

class MP3Extractor(BaseExtractor):
    def extract_specific_metadata(self) -> Dict[str, Any]:
        raw_data = {}
        
        # Extract ALL ID3 frames with their original identifiers (e.g., TIT2, TPE1, TXXX)
        try:
            tags = ID3(str(self.file_path))
            for frame_id in tags.keys():
                frame_value = tags[frame_id]
                # Storing with ID3_ prefix to distinguish from filesystem metadata
                raw_data[f"ID3_{frame_id}"] = str(frame_value)
        except Exception as e:
            raw_data["id3_extraction_error"] = str(e)

        # Extract technical audio stream properties
        try:
            audio = MP3(str(self.file_path))
            if audio.info:
                for attr in dir(audio.info):
                    # Filter out private methods and callable properties
                    if not attr.startswith('_') and not callable(getattr(audio.info, attr)):
                        raw_data[f"stream_{attr}"] = getattr(audio.info, attr)
        except:
            pass
        
        return raw_data