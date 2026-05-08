/**
 * Utility functions for formatting execution times
 */

/**
 * Format execution time in milliseconds to a human-readable string
 * @param {number} ms - Time in milliseconds
 * @returns {string} Formatted time (e.g., "2.50s" or "150ms")
 */
export function formatExecutionTime(ms) {
  if (ms >= 1000) {
    return (ms / 1000).toFixed(2) + 's';
  }
  return Math.round(ms) + 'ms';
}

/**
 * Calculate and format duration between two timestamps
 * @param {number} startTime - Start time (ms since epoch)
 * @param {number} endTime - End time (ms since epoch)
 * @returns {string} Formatted duration
 */
export function formatDuration(startTime, endTime) {
  const duration = endTime - startTime;
  return formatExecutionTime(duration);
}

/**
 * Calculate and format elapsed time since a start point
 * @param {number} startTime - Start time (ms since epoch)
 * @returns {string} Formatted elapsed time
 */
export function formatElapsedTime(startTime) {
  return formatDuration(startTime, Date.now());
}
