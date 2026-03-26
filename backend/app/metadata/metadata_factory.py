from pathlib import Path
from .metadata_mp3 import MP3Extractor
from .metadata_wav import WAVExtractor
from .metadata_m4a import M4AExtractor

class MetadataFactory:
    @staticmethod
    def get_extractor(file_path: str):
        """
        Factory method to instantiate the appropriate extractor.
        Returns a subclass of BaseExtractor.
        """
        ext = Path(file_path).suffix.lower()
        
        # Mapping extensions to their respective forensic extractor classes
        extractors = {
            '.mp3': MP3Extractor,
            '.wav': WAVExtractor,
            '.m4a': M4AExtractor
        }
        
        extractor_class = extractors.get(ext)
        if not extractor_class:
            raise ValueError(f"Extension {ext} is not supported for forensic analysis")
            
        return extractor_class(file_path)