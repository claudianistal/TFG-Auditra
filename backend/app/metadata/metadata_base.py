import json
import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from app.utils.file_handler import get_binary_path

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

    def _get_subprocess_flags(self):
        """Evita que se abra una ventana de consola negra en Windows (PyInstaller --windowed)"""
        return getattr(subprocess, 'CREATE_NO_WINDOW', 0)

    def _run_exiftool(self) -> Dict[str, Any]:
        """Executes ExifTool to get all metadata tags in JSON format."""
        try:
            exe_path = get_binary_path("exiftool.exe")
            result = subprocess.run(
                [exe_path, "-json", "-G", str(self.file_path)],
                capture_output=True, text=True, shell=False, check=True,
                creationflags=self._get_subprocess_flags(),
                stdin=subprocess.DEVNULL
            )
            data = json.loads(result.stdout)
            return {f"exif:{k}": v for k, v in data[0].items()} if data else {}
        except subprocess.CalledProcessError as e:
            return {"exif_error": f"Command Failed: {e.stderr}"}
        except Exception as e:
            return {"exif_error": str(e)}

    def _run_ffprobe(self) -> Dict[str, Any]:
        """Executes FFprobe to analyze the audio stream profile."""
        try:
            exe_path = get_binary_path("ffprobe.exe")
            cmd = [
                exe_path, "-v", "quiet", "-print_format", "json",
                "-show_format", "-show_streams", str(self.file_path)
            ]
            result = subprocess.run(
                cmd, capture_output=True, text=True, shell=False, check=True,
                creationflags=self._get_subprocess_flags(),
                stdin=subprocess.DEVNULL
            )
            data = json.loads(result.stdout)
            
            flattened_data = {}
            for section_key, section_value in data.items():
                if isinstance(section_value, dict):
                    for k, v in section_value.items():
                        flattened_data[f"ffprobe_{section_key}_{k}"] = v
                elif isinstance(section_value, list) and len(section_value) > 0 and isinstance(section_value[0], dict):
                    # Usually "streams" is a list of dicts. We flatten the first stream.
                    for k, v in section_value[0].items():
                        flattened_data[f"ffprobe_{section_key}_0_{k}"] = v
                else:
                    flattened_data[f"ffprobe_{section_key}"] = section_value
                    
            return flattened_data
        except subprocess.CalledProcessError as e:
            return {"ffprobe_error": f"Command Failed: {e.stderr}"}
        except Exception as e:
            return {"ffprobe_error": str(e)}

    @abstractmethod
    def extract_specific_metadata(self) -> Dict[str, Any]:
        """
        Abstract method to be implemented by format-specific extractors.
        Should return raw metadata as found in the file structure.
        """
        pass

    def get_all_metadata(self) -> Dict[str, Any]:
        """
        Combines filesystem, internal, ExifTool and FFprobe metadata.
        Values are NOT filtered to preserve potential forensic anomalies (nulls/empty strings).
        """
        file_info = self.get_file_info()
        audio_info = self.extract_specific_metadata()
        exif_info = self._run_exiftool()
        ffprobe_info = self._run_ffprobe()
        
        return {**file_info, **audio_info, **exif_info, **ffprobe_info}