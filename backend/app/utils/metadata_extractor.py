"""Metadata extraction utilities for audio files (MP3, M4A, WAV)."""
import os
import wave
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime
from mutagen.id3 import ID3
from mutagen.mp4 import MP4
from mutagen.wave import WAVE


def extract_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from an audio file.
    
    Detects file format and delegates to appropriate extraction function.
    Also includes file information (size, modification date, format, etc).
    
    Args:
        file_path (str): Path to the audio file
        
    Returns:
        Dict[str, Any]: Dictionary with ALL available metadata and file info.
                       Only includes fields with actual values (filters out None/null).
                       
    Raises:
        ValueError: If file format not supported or file is corrupted
        FileNotFoundError: If file doesn't exist
    """
    file_path_obj = Path(file_path)
    
    if not file_path_obj.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file information
    file_stat = file_path_obj.stat()
    file_info = {
        'file_name': file_path_obj.name,
        'file_size': file_stat.st_size,
        'file_size_mb': round(file_stat.st_size / (1024 * 1024), 2),
        'file_format': file_path_obj.suffix.lower().replace('.', '').upper(),
        'file_modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
    }
    
    # Get audio metadata based on format
    ext = file_path_obj.suffix.lower()
    
    if ext == '.mp3':
        metadata = _extract_mp3_metadata(str(file_path_obj))
    elif ext == '.m4a':
        metadata = _extract_m4a_metadata(str(file_path_obj))
    elif ext == '.wav':
        metadata = _extract_wav_metadata(str(file_path_obj))
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    
    # Merge file info with audio metadata
    all_metadata = {**file_info, **metadata}
    
    # Filter out None/null values - only return fields that have actual data
    cleaned_metadata = {
        key: value for key, value in all_metadata.items() 
        if value is not None and value != ""
    }
    
    return cleaned_metadata


def _extract_mp3_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from MP3 file using mutagen.
    
    MP3 metadata is stored in ID3 tags. Extracts ALL available ID3 frames.
    
    Args:
        file_path (str): Path to the MP3 file
        
    Returns:
        Dict[str, Any]: Dictionary with ALL available metadata fields
    """
    metadata = {}
    
    # ID3 frame mappings: frame_id -> display_name
    id3_mappings = {
        'TIT2': 'title',
        'TIT1': 'content_group_description',
        'TIT3': 'subtitle',
        'TPE1': 'artist',
        'TPE2': 'album_artist',
        'TPE3': 'conductor',
        'TPE4': 'remixer',
        'TALB': 'album',
        'TCON': 'genre',
        'TDRC': 'year',
        'TDRL': 'release_date',
        'TPOS': 'part_of_set',
        'TRCK': 'track_number',
        'TCOM': 'composer',
        'TEXT': 'lyricist',
        'TPUB': 'publisher',
        'COMM': 'comment',
        'USLT': 'unsynchronized_lyrics',
        'TOFN': 'original_filename',
        'TOLY': 'original_lyricist',
        'TOPE': 'original_artist',
        'TORY': 'original_release_year',
        'TENC': 'encoded_by',
        'TBPM': 'bpm',
        'TCOP': 'copyright',
        'TDEN': 'encoding_time',
        'TKEY': 'initial_key',
        'TLAN': 'language',
        'TLEN': 'length',
        'TMED': 'media_type',
        'TMCL': 'musician_credits',
        'TXXX': 'user_defined',
    }
    
    try:
        id3 = ID3(file_path)
        
        # Extract all ID3 frames
        for frame_id, value in id3.items():
            # Map frame ID to normalized name
            display_name = id3_mappings.get(frame_id[:4], frame_id.lower())
            
            # Extract value safely
            if hasattr(value, 'text') and value.text:
                metadata[display_name] = str(value.text[0]) if value.text else None
            else:
                metadata[display_name] = str(value) if value else None
                
    except Exception as e:
        # No ID3 tags found
        pass
    
    # Always extract audio properties
    try:
        from mutagen.mp3 import MP3
        audio = MP3(file_path)
        if audio.info:
            info = audio.info
            metadata['duration'] = int(audio.info.length) if audio.info.length else None
            metadata['bitrate'] = info.bitrate
            metadata['sample_rate'] = info.sample_rate
            metadata['channels'] = info.channels
            
            # Extract ALL available attributes from info object dynamically
            for attr in dir(info):
                if not attr.startswith('_'):  # Skip private attributes
                    try:
                        value = getattr(info, attr)
                        # Skip methods and properties that return None
                        if not callable(value) and value is not None:
                            attr_key = attr.lower().replace(' ', '_')
                            if attr_key not in metadata:  # Don't override existing
                                metadata[attr_key] = value
                    except:
                        pass
    except Exception as e:
        pass
    
    return metadata


def _extract_m4a_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from M4A (ALAC, AAC) file using mutagen.
    
    M4A metadata is stored in iTunes-compatible atoms. Extracts ALL available atoms.
    
    Args:
        file_path (str): Path to the M4A file
        
    Returns:
        Dict[str, Any]: Dictionary with ALL available metadata fields
    """
    metadata = {}
    
    # iTunes atom mappings: atom_name -> display_name
    itunes_mappings = {
        '\xa9nam': 'title',
        '\xa9ART': 'artist',
        'aART': 'album_artist',
        '\xa9alb': 'album',
        '\xa9gen': 'genre',
        '\xa9day': 'year',
        '\xa9wrt': 'composer',
        '\xa9cmt': 'comment',
        'trkn': 'track_number',
        'disk': 'disc_number',
        '\xa9lyr': 'lyrics',
        '\xa9too': 'encoded_by',
        'cprt': 'copyright',
        'tmpo': 'bpm',
        '\xa9grp': 'grouping',
        'purd': 'purchase_date',
        'pusd': 'purchase_seller',
    }
    
    try:
        audio = MP4(file_path)
        
        # Extract all MP4 atoms
        for atom_name, value in audio.items():
            # Map atom name to normalized name
            display_name = itunes_mappings.get(atom_name, atom_name.replace('\xa9', '').lower())
            
            # Extract value safely
            if isinstance(value, list) and value:
                if isinstance(value[0], bytes):
                    metadata[display_name] = value[0].decode('utf-8', errors='ignore')
                else:
                    metadata[display_name] = str(value[0])
            else:
                metadata[display_name] = str(value) if value else None
            
        # Extract audio info
        if audio.info:
            info = audio.info
            metadata['duration'] = int(audio.info.length) if audio.info.length else None
            metadata['bitrate'] = info.bitrate
            metadata['sample_rate'] = info.sample_rate
            metadata['channels'] = info.channels
            
            # Extract ALL available attributes from info object dynamically
            for attr in dir(info):
                if not attr.startswith('_'):  # Skip private attributes
                    try:
                        value = getattr(info, attr)
                        # Skip methods and properties that return None
                        if not callable(value) and value is not None:
                            attr_key = attr.lower().replace(' ', '_')
                            if attr_key not in metadata:  # Don't override existing
                                metadata[attr_key] = value
                    except:
                        pass
            
    except Exception as e:
        pass
    
    return metadata


def _extract_wav_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from WAV file.
    
    WAV files can have metadata in:
    - LIST-INFO chunks (native WAV metadata)
    - ID3v2 tags (appended to WAV)
    - Plus standard audio properties
    
    Uses multiple approaches to extract ALL available metadata.
    
    Args:
        file_path (str): Path to the WAV file
        
    Returns:
        Dict[str, Any]: Dictionary with ALL available metadata fields
    """
    metadata = {}
    
    # Approach 1: Try mutagen.WAVE for ID3 tags and LIST-INFO
    try:
        audio = WAVE(file_path)
        
        # Extract all available frames from WAVE
        for key, value in audio.items():
            # Normalize key
            display_key = key.lower() if isinstance(key, str) else str(key).lower()
            
            # Extract value
            if hasattr(value, 'text') and value.text:
                metadata[display_key] = str(value.text[0]) if value.text else None
            else:
                metadata[display_key] = str(value) if value else None
        
        # Extract ALL available audio properties from mutagen info object
        if audio.info:
            info = audio.info
            
            # Standard properties
            metadata['duration'] = int(audio.info.length) if audio.info.length else None
            metadata['bitrate'] = info.bitrate
            metadata['sample_rate'] = info.sample_rate
            metadata['channels'] = info.channels
            
            # Extract ALL attributes from info object dynamically
            for attr in dir(info):
                if not attr.startswith('_'):  # Skip private attributes
                    try:
                        value = getattr(info, attr)
                        # Skip methods and properties that return None
                        if not callable(value) and value is not None:
                            attr_key = attr.lower().replace(' ', '_')
                            if attr_key not in metadata:  # Don't override existing
                                metadata[attr_key] = value
                    except:
                        pass
            
    except Exception as e:
        pass
    
    # Approach 2: Use wave module for reliable audio info (most important for WAV)
    try:
        with wave.open(file_path, 'rb') as wav_file:
            n_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            framerate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            compression_type = wav_file.getcomptype()
            
            # Set/override audio properties (wave module is authoritative for WAV)
            metadata['channels'] = n_channels if n_channels else None
            metadata['sample_rate'] = framerate if framerate else None
            metadata['duration'] = int(n_frames // framerate) if framerate > 0 else None
            metadata['bit_depth'] = (sample_width * 8) if sample_width else None
            metadata['compression_type'] = compression_type if compression_type != 'NONE' else None
            metadata['frame_count'] = n_frames
            metadata['sample_width_bytes'] = sample_width
            
            # Calculate bitrate: channels * sample_width * 8 (bits) * sample_rate
            if all([n_channels, sample_width, framerate]):
                metadata['bitrate'] = n_channels * sample_width * 8 * framerate
                
    except Exception as e:
        pass
    
    # Approach 3: Try ID3 directly on the file (in case it's appended like MP3)
    try:
        id3 = ID3(file_path)
        
        id3_mappings = {
            'TIT2': 'title',
            'TPE1': 'artist',
            'TALB': 'album',
            'TCON': 'genre',
            'TDRC': 'year',
            'TRCK': 'track_number',
            'TCOM': 'composer',
            'COMM': 'comment',
        }
        
        for frame_id, value in id3.items():
            display_name = id3_mappings.get(frame_id[:4], frame_id.lower())
            if hasattr(value, 'text') and value.text:
                metadata[display_name] = str(value.text[0]) if value.text else None
            else:
                metadata[display_name] = str(value) if value else None
                
    except Exception as e:
        pass
    
    return metadata

