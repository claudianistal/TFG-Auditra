/**
 * Indicator Details Formatter
 * Converts raw technical details from backend into human-readable explanations
 * for end users without technical audio knowledge.
 */

import i18n from '../i18n';

/**
 * Main function to format indicator details
 * @param {string} indicatorName - Name of the indicator (e.g., 'padding_pattern')
 * @param {object} details - Raw details object from backend
 * @returns {array} Array of formatted detail objects with { label, value, explanation }
 */
export function formatIndicatorDetails(indicatorName, details) {
  if (!details || Object.keys(details).length === 0) {
    return [];
  }

  const formatters = {
    padding_pattern: formatPaddingPattern,
    timestamp_consistency: formatTimestampConsistency,
    encoding_library: formatEncodingLibrary,
    mono_audio: formatMonoAudio,
    codec_consistency: formatCodecConsistency,
    file_size: formatFileSize,
    self_similarity: formatSelfSimilarity,
  };

  const formatter = formatters[indicatorName];
  return formatter ? formatter(details) : formatGenericDetails(details);
}

/**
 * Format padding pattern details
 * Shows what repetitive bytes were found at file edges
 */
function formatPaddingPattern(details) {
  const t = i18n.t;
  const result = [];

  // Repetitive bytes at file start
  if (details.patterns_at_start && details.patterns_at_start.length > 0) {
    const patterns = details.patterns_at_start
      .map((p) => `${p.pattern} (${p.consecutive_bytes} bytes)`)
      .join(', ');

    result.push({
      label: t('indicators.padding_pattern.details.bytes_at_start'),
      value: patterns,
      explanation: t('indicators.padding_pattern.details.bytes_at_start_explanation'),
    });
  }

  // Repetitive bytes at file end
  if (details.patterns_at_end && details.patterns_at_end.length > 0) {
    const patterns = details.patterns_at_end
      .map((p) => `${p.pattern} (${p.consecutive_bytes} bytes)`)
      .join(', ');

    result.push({
      label: t('indicators.padding_pattern.details.bytes_at_end'),
      value: patterns,
      explanation: t('indicators.padding_pattern.details.bytes_at_end_explanation'),
    });
  }

  return result;
}

/**
 * Format timestamp consistency details
 * Shows creation vs modification date relationship
 */
function formatTimestampConsistency(details) {
  const t = i18n.t;
  const result = [];

  if (details.creation_time) {
    result.push({
      label: t('indicators.timestamp_consistency.details.creation_time'),
      value: formatDateValue(details.creation_time),
      explanation: null,
    });
  }

  if (details.modification_time) {
    result.push({
      label: t('indicators.timestamp_consistency.details.modification_time'),
      value: formatDateValue(details.modification_time),
      explanation: null,
    });
  }

  if (details.relationship) {
    const relationshipKey = `indicators.timestamp_consistency.details.relationship_${details.relationship}`;
    result.push({
      label: t('indicators.timestamp_consistency.details.relationship'),
      value: t(relationshipKey),
      explanation: t(`${relationshipKey}_explanation`),
    });
  }

  return result;
}

/**
 * Format encoding library details
 * Shows all metadata fields where the encoding library was detected
 */
function formatEncodingLibrary(details) {
  const t = i18n.t;
  const result = [];

  // Show all detected fields
  if (details.detected_fields && Array.isArray(details.detected_fields) && details.detected_fields.length > 0) {
    details.detected_fields.forEach((item) => {
      result.push({
        label: item.field,
        value: item.value.substring(0, 100),
        explanation: null,
      });
    });
  }

  return result;
}

/**
 * Format mono audio details
 * Shows number of channels detected
 */
function formatMonoAudio(details) {
  const t = i18n.t;
  const result = [];

  if (details.channels !== undefined) {
    const channelDisplay = details.channels === 1 
      ? t('indicators.mono_audio.details.mono') 
      : `${details.channels} ${t('indicators.mono_audio.details.channels_plural')}`;
    
    result.push({
      label: t('indicators.mono_audio.details.channels'),
      value: channelDisplay,
      explanation: null, // No explanation for metadata-based indicators
    });
  }

  return result;
}

/**
 * Format codec consistency details
 * Shows codec vs file format mismatch
 */
function formatCodecConsistency(details) {
  const t = i18n.t;
  const result = [];

  if (details.file_format) {
    result.push({
      label: t('indicators.codec_consistency.details.file_format'),
      value: details.file_format.toUpperCase(),
      explanation: null,
    });
  }

  if (details.codec) {
    result.push({
      label: t('indicators.codec_consistency.details.codec_detected'),
      value: details.codec,
      explanation: t('indicators.codec_consistency.details.codec_explanation'),
    });
  }

  if (details.expected_codecs && Array.isArray(details.expected_codecs)) {
    result.push({
      label: t('indicators.codec_consistency.details.expected_codecs'),
      value: details.expected_codecs.join(', ') || t('indicators.codec_consistency.details.unknown'),
      explanation: t('indicators.codec_consistency.details.expected_explanation'),
    });
  }

  return result;
}

/**
 * Format file size details
 * Shows size deviation from expected based on bitrate × duration
 */
function formatFileSize(details) {
  const t = i18n.t;
  const result = [];

  if (details.deviation_percentage !== undefined) {
    const deviation = Math.abs(details.deviation_percentage);
    let severityKey = 'low';
    if (deviation > 30) severityKey = 'high';
    else if (deviation > 20) severityKey = 'medium';

    result.push({
      label: t('indicators.file_size.details.deviation'),
      value: `${deviation.toFixed(2)}%`,
      explanation: t(`indicators.file_size.details.deviation_${severityKey}_explanation`, {
        deviation: deviation.toFixed(2),
      }),
    });
  }

  if (details.file_size && details.expected_size) {
    result.push({
      label: t('indicators.file_size.details.actual_vs_expected'),
      value: `${formatBytes(details.file_size)} vs ${formatBytes(details.expected_size)}`,
      explanation: t('indicators.file_size.details.size_explanation'),
    });
  }

  if (details.duration_seconds !== undefined && details.bitrate !== undefined) {
    result.push({
      label: t('indicators.file_size.details.audio_specs'),
      value: `${details.duration_seconds.toFixed(1)}s @ ${formatBitrate(details.bitrate)}`,
      explanation: t('indicators.file_size.details.specs_explanation'),
    });
  }

  if (details.is_lossy !== undefined) {
    result.push({
      label: t('indicators.file_size.details.compression_type'),
      value: details.is_lossy ? t('indicators.file_size.details.lossy') : t('indicators.file_size.details.lossless'),
      explanation: t('indicators.file_size.details.compression_explanation', {
        type: details.is_lossy ? t('indicators.file_size.details.lossy') : t('indicators.file_size.details.lossless'),
      }),
    });
  }

  return result;
}

/**
 * Format self-similarity details
 * Shows pattern repetition score analysis
 */
function formatSelfSimilarity(details) {
  // No technical details shown - explanation is in the reasoning section
  return [];
}

/**
 * Generic formatter for unknown indicator types
 * Falls back to simple key-value display
 */
function formatGenericDetails(details) {
  return Object.entries(details)
    .filter(([key]) => !key.startsWith('_')) // Skip internal fields
    .map(([key, value]) => ({
      label: formatLabel(key),
      value: formatValue(value),
      explanation: null,
    }));
}

/**
 * Helper: Format a date value
 */
function formatDateValue(dateStr) {
  if (!dateStr) return 'N/A';
  try {
    const date = new Date(dateStr);
    return date.toLocaleString();
  } catch {
    return dateStr;
  }
}

/**
 * Helper: Format bytes to human-readable size
 */
function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(Math.abs(bytes)) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Helper: Format bitrate to human-readable format
 */
function formatBitrate(bitrate) {
  if (!bitrate) return 'N/A';
  if (bitrate >= 1000000) {
    return (bitrate / 1000000).toFixed(1) + ' Mbps';
  }
  if (bitrate >= 1000) {
    return (bitrate / 1000).toFixed(0) + ' kbps';
  }
  return bitrate + ' bps';
}

/**
 * Helper: Format number with thousands separator
 */
function formatNumber(num) {
  return num.toLocaleString();
}

/**
 * Helper: Format key name to readable label
 */
function formatLabel(key) {
  return key
    .replace(/_/g, ' ')
    .replace(/([A-Z])/g, ' $1')
    .trim()
    .split(' ')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Helper: Format any value to string
 */
function formatValue(value) {
  if (typeof value === 'object') {
    return JSON.stringify(value);
  }
  if (typeof value === 'boolean') {
    return value ? 'Yes' : 'No';
  }
  if (typeof value === 'number') {
    return formatNumber(value);
  }
  return String(value || 'N/A');
}
