import wave
from mutagen.wave import WAVE
from .metadata_base import BaseExtractor
from typing import Dict, Any

class WAVExtractor(BaseExtractor):
    def extract_specific_metadata(self) -> Dict[str, Any]:
        raw_data = {}
        
        # Approach 1: Use Mutagen for RIFF Info chunks and potential appended ID3 tags
        try:
            audio = WAVE(str(self.file_path))
            for key, value in audio.items():
                raw_data[f"RIFF_{key}"] = str(value)
        except:
            pass

        # Approach 2: Native wave module for authoritative header analysis
        try:
            with wave.open(str(self.file_path), 'rb') as w:
                params = w.getparams()
                raw_data.update({
                    'wav_channels': params.nchannels,
                    'wav_sample_width_bytes': params.sampwidth,
                    'wav_frame_rate': params.framerate,
                    'wav_n_frames': params.nframes,
                    'wav_compression_type': params.comptype,
                    'wav_compression_name': params.compname
                })
        except Exception as e:
            raw_data["wav_header_error"] = str(e)

        return raw_data