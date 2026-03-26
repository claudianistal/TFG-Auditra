from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class BaseExtractor(ABC):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def get_file_info(self) -> Dict[str, Any]:
        """
        Extracts basic filesystem metadata. 
        Crucial for verifying timestamps and file sizes in a forensic context.
        """
        stats = self.file_path.stat()
        return {
            'file_name': self.file_path.name,
            'file_size_bytes': stats.st_size,
            'file_size_mb': round(stats.st_size / (1024 * 1024), 2),
            'file_extension': self.file_path.suffix.lower(),
            'filesystem_modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
            'filesystem_created': datetime.fromtimestamp(stats.st_ctime).isoformat(),
        }

    @abstractmethod
    def extract_specific_metadata(self) -> Dict[str, Any]:
        """
        Abstract method to be implemented by format-specific extractors.
        Should return raw metadata as found in the file structure.
        """
        pass

    def get_all_metadata(self) -> Dict[str, Any]:
        """
        Combines filesystem and audio-specific metadata.
        Values are NOT filtered to preserve potential forensic anomalies (nulls/empty strings).
        """
        file_info = self.get_file_info()
        audio_info = self.extract_specific_metadata()
        
        return {**file_info, **audio_info}