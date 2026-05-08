import React, { useEffect, useState } from 'react';
import './ConfirmationBanner.css';
import { CheckCircle, AlertCircle } from 'lucide-react';

/**
 * ConfirmationBanner Component
 * 
 * Displays a success or error confirmation message with execution time.
 * Auto-dismisses after 5 seconds with a fade-out animation.
 * 
 * Props:
 *   - isVisible: boolean - whether to show the banner
 *   - type: 'success' | 'error' - type of message
 *   - message: string - the message to display
 *   - executionTime: number - time in milliseconds
 *   - onDismiss: function - callback when banner dismisses (optional)
 *   - autoDismissTime: number - time in ms before auto-dismiss (default: 5000)
 */
const ConfirmationBanner = ({
  isVisible,
  type = 'success',
  message,
  executionTime,
  onDismiss,
  autoDismissTime = 5000,
}) => {
  const [shouldShow, setShouldShow] = useState(isVisible);
  const [isAnimatingOut, setIsAnimatingOut] = useState(false);

  useEffect(() => {
    if (!isVisible) {
      setShouldShow(false);
      setIsAnimatingOut(false);
      return;
    }

    setShouldShow(true);
    setIsAnimatingOut(false);

    const dismissTimer = setTimeout(() => {
      setIsAnimatingOut(true);
      setTimeout(() => {
        setShouldShow(false);
        if (onDismiss) onDismiss();
      }, 300);
    }, autoDismissTime);

    return () => clearTimeout(dismissTimer);
  }, [isVisible, onDismiss, autoDismissTime]);

  if (!shouldShow) return null;

  const formatExecutionTime = (ms) => {
    if (ms >= 1000) {
      return (ms / 1000).toFixed(2) + 's';
    }
    return Math.round(ms) + 'ms';
  };

  return (
    <div
      className={`confirmation-banner confirmation-banner--${type} ${
        isAnimatingOut ? 'confirmation-banner--fade-out' : ''
      }`}
      role="alert"
      aria-live="polite"
    >
      <div className="confirmation-banner__content">
        <span className="confirmation-banner__icon">
          {type === 'success' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
        </span>
        <span className="confirmation-banner__message">
          {message}
          {executionTime !== undefined && (
            <span className="confirmation-banner__time">
              ({formatExecutionTime(executionTime)})
            </span>
          )}
        </span>
      </div>
    </div>
  );
};

export default ConfirmationBanner;
