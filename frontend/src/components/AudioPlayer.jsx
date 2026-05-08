import React, { useRef, useState, useEffect } from 'react';
import './AudioPlayer.css';
import { Play, Pause, Volume2, VolumeX } from 'lucide-react';

/**
 * AudioPlayer Component
 * 
 * A basic HTML5 audio player with play/pause, volume control, and smooth 60fps progress bar.
 * Uses native HTML5 <audio> element with no external dependencies.
 * 
 * Props:
 *   - audioFile: string (URL) or File object - the audio source
 *   - showFileName: boolean - whether to display filename (default: true)
 */
const AudioPlayer = ({ audioFile, showFileName = true }) => {
  const audioRef = useRef(null);
  const playAnimationRef = useRef(); // Referencia para controlar la animación a 60fps
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [fileName, setFileName] = useState('Audio');

  // Handle audio file source
  useEffect(() => {
    if (!audioFile || !audioRef.current) return;

    if (typeof audioFile === 'string') {
      // URL-based source
      audioRef.current.src = audioFile;
    } else if (audioFile instanceof File) {
      // File object - create object URL
      const url = URL.createObjectURL(audioFile);
      audioRef.current.src = url;
      setFileName(audioFile.name);
      return () => URL.revokeObjectURL(url);
    }
  }, [audioFile]);

  // Update volume when changed
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = isMuted ? 0 : volume;
    }
  }, [volume, isMuted]);

  // Limpiar la animación si el componente se desmonta
  useEffect(() => {
    return () => {
      if (playAnimationRef.current) {
        cancelAnimationFrame(playAnimationRef.current);
      }
    };
  }, []);

  const formatTime = (seconds) => {
    if (!seconds || isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  // Función para actualizar el progreso a 60 FPS
  const updateProgress = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
      playAnimationRef.current = requestAnimationFrame(updateProgress);
    }
  };

  const togglePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
        cancelAnimationFrame(playAnimationRef.current); // Parar animación
      } else {
        audioRef.current.play();
        playAnimationRef.current = requestAnimationFrame(updateProgress); // Iniciar animación a 60fps
      }
      setIsPlaying(!isPlaying);
    }
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const handleProgressChange = (e) => {
    const newTime = parseFloat(e.target.value);
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  const handleVolumeChange = (e) => {
    setVolume(parseFloat(e.target.value));
  };

  const handleAudioEnded = () => {
    setIsPlaying(false);
    cancelAnimationFrame(playAnimationRef.current); // Detener la animación cuando acaba
  };

  // Cálculos para el rellenado dinámico de las barras
  const progressPercent = duration ? (currentTime / duration) * 100 : 0;
  const volumePercent = isMuted ? 0 : volume * 100;

  return (
    <div className="audio-player">
      <audio
        ref={audioRef}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={handleAudioEnded}
      />

      <div className="audio-player__container">
        {/* Play/Pause button */}
        <button
          className="audio-player__button audio-player__button--play"
          onClick={togglePlayPause}
          title={isPlaying ? 'Pause' : 'Play'}
        >
          {isPlaying ? <Pause size={20} /> : <Play size={20} />}
        </button>

        {/* Progress bar */}
        <div className="audio-player__progress-wrapper">
          <input
            type="range"
            min="0"
            max={duration || 0}
            step="any"
            value={currentTime}
            onChange={handleProgressChange}
            className="audio-player__progress"
            style={{ '--progress-width': `${progressPercent}%` }}
          />
        </div>

        {/* Time display */}
        <span className="audio-player__time">
          {formatTime(currentTime)} / {formatTime(duration)}
        </span>

        {/* Volume control */}
        <div className="audio-player__volume-control">
          <button
            className="audio-player__button audio-player__button--mute"
            onClick={toggleMute}
            title={isMuted ? 'Unmute' : 'Mute'}
          >
            {isMuted ? <VolumeX size={18} /> : <Volume2 size={18} />}
          </button>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={isMuted ? 0 : volume}
            onChange={handleVolumeChange}
            className="audio-player__volume"
            style={{ '--volume-width': `${volumePercent}%` }}
          />
        </div>
      </div>

      {/* Optional filename display */}
      {showFileName && fileName && (
        <div className="audio-player__filename">
          {fileName}
        </div>
      )}
    </div>
  );
};

export default AudioPlayer;