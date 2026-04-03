import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { ChevronDown, ChevronUp } from 'lucide-react';

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

  const formatBytes = (num) => {
    if (num < 1024) return `${num} B`;
    if (num < 1024 * 1024) return `${(num / 1024).toFixed(2)} KB`;
    return `${(num / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="hex-dump-viewer">
      {/* Start of file section */}
      <div className="hex-dump-section">
        <div
          className="hex-dump-section__header"
          onClick={() => setExpandedStart(!expandedStart)}
        >
          <div className="hex-dump-section__toggle">
            {expandedStart ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </div>
          <h5>{t('pages.patterns.startOfFile') || 'Start of File'} ({t('pages.patterns.first1024Bytes') || 'First 1024 bytes'})</h5>
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
        <div
          className="hex-dump-section__header"
          onClick={() => setExpandedEnd(!expandedEnd)}
        >
          <div className="hex-dump-section__toggle">
            {expandedEnd ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </div>
          <h5>{t('pages.patterns.endOfFile') || 'End of File'} ({t('pages.patterns.last1024Bytes') || 'Last 1024 bytes'}) — {t('pages.patterns.total') || 'Total'}: {formatBytes(totalFileSize)}</h5>
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
