import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';

const HexDumpViewer = ({ hexStart, hexEnd, totalFileSize }) => {
  const { t } = useTranslation();
  /**
   * HexDumpViewer Component
   * 
   * Displays hex dumps of file start and end bytes in a classic format:
   * ADDRESS: HEX BYTES | ASCII
   * 
   * Useful for inspecting padding (0x00, 0xFF) at file boundaries.
   */

  const [expandedStart, setExpandedStart] = useState(true);
  const [expandedEnd, setExpandedEnd] = useState(true);
  const [copiedStart, setCopiedStart] = useState(false);
  const [copiedEnd, setCopiedEnd] = useState(false);

  const formatBytes = (num) => {
    if (num < 1024) return `${num} B`;
    if (num < 1024 * 1024) return `${(num / 1024).toFixed(2)} KB`;
    return `${(num / (1024 * 1024)).toFixed(2)} MB`;
  };

  const handleCopyHexStart = async () => {
    const textToCopy = hexStart.join('\n');
    try {
      await navigator.clipboard.writeText(textToCopy);
      setCopiedStart(true);
      setTimeout(() => setCopiedStart(false), 2000);
    } catch (err) {
      console.error('Failed to copy hex dump:', err);
    }
  };

  const handleCopyHexEnd = async () => {
    const textToCopy = hexEnd.join('\n');
    try {
      await navigator.clipboard.writeText(textToCopy);
      setCopiedEnd(true);
      setTimeout(() => setCopiedEnd(false), 2000);
    } catch (err) {
      console.error('Failed to copy hex dump:', err);
    }
  };

  return (
    <div className="hex-dump-viewer">
      {/* Start of file section */}
      <div className="hex-dump-section">
        <div className="hex-dump-section__header">
          <div
            className="hex-dump-section__toggle"
            onClick={() => setExpandedStart(!expandedStart)}
          >
            {expandedStart ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </div>
          <h5 onClick={() => setExpandedStart(!expandedStart)}>
            {t('pages.patterns.startOfFile') || 'Start of File'} ({t('pages.patterns.first1024Bytes') || 'First 1024 bytes'})
          </h5>
          <button 
            className="hex-dump-copy-btn"
            onClick={handleCopyHexStart}
            title={copiedStart ? 'Copiado!' : 'Copiar hex dump'}
          >
            {copiedStart ? (
              <>
                <Check size={16} />
                <span>Copiado!</span>
              </>
            ) : (
              <>
                <Copy size={16} />
                <span>Copiar</span>
              </>
            )}
          </button>
        </div>

        {expandedStart && (
          <div className="hex-dump-section__content">
            <pre className="hex-dump-section__pre">
              {hexStart.join('\n')}
            </pre>
          </div>
        )}
      </div>

      {/* End of file section */}
      <div className="hex-dump-section">
        <div className="hex-dump-section__header">
          <div
            className="hex-dump-section__toggle"
            onClick={() => setExpandedEnd(!expandedEnd)}
          >
            {expandedEnd ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </div>
          <h5 onClick={() => setExpandedEnd(!expandedEnd)}>
            {t('pages.patterns.endOfFile') || 'End of File'} ({t('pages.patterns.last1024Bytes') || 'Last 1024 bytes'}) — {t('pages.patterns.total') || 'Total'}: {formatBytes(totalFileSize)}
          </h5>
          <button 
            className="hex-dump-copy-btn"
            onClick={handleCopyHexEnd}
            title={copiedEnd ? 'Copiado!' : 'Copiar hex dump'}
          >
            {copiedEnd ? (
              <>
                <Check size={16} />
                <span>Copiado!</span>
              </>
            ) : (
              <>
                <Copy size={16} />
                <span>Copiar</span>
              </>
            )}
          </button>
        </div>

        {expandedEnd && (
          <div className="hex-dump-section__content">
            <pre className="hex-dump-section__pre">
              {hexEnd.join('\n')}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default HexDumpViewer;
