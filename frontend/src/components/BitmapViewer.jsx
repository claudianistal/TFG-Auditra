import React from 'react';
import { useTranslation } from 'react-i18next';
import { AlertCircle } from 'lucide-react';

const BitmapViewer = ({ imageBase64, filename, width }) => {
  const { t } = useTranslation();
  /**
   * BitmapViewer Component
   * 
   * Displays the binary content visualization (autosimilitude bitmap)
   * as a grayscale image.
   */

  if (!imageBase64) {
    return (
      <div className="bitmap-viewer--empty">
        <AlertCircle size={24} />
        <p>{t('pages.patterns.noBitmapData') || 'No bitmap data available'}</p>
      </div>
    );
  }

  return (
    <div className="bitmap-viewer">
      <div className="bitmap-viewer__container">
        <img
          src={`data:image/png;base64,${imageBase64}`}
          alt="Binary content bitmap"
          className="bitmap-viewer__image"
        />
      </div>

      <div className="bitmap-viewer__footer">
        <p className="bitmap-viewer__info">{t('pages.patterns.width') || 'Width'}: {width} {t('pages.patterns.bytesPerRow') || 'bytes per row'}</p>
      </div>
    </div>
  );
};

export default BitmapViewer;
