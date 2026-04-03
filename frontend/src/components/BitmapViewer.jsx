import React from 'react';
import { Download, AlertCircle } from 'lucide-react';

const BitmapViewer = ({ imageBase64, filename, width }) => {
  /**
   * BitmapViewer Component
   * 
   * Displays the binary content visualization (autosimilitude bitmap)
   * as a grayscale image and provides download functionality.
   */

  if (!imageBase64) {
    return (
      <div className="bitmap-viewer--empty">
        <AlertCircle size={24} />
        <p>No bitmap data available</p>
      </div>
    );
  }

  const handleDownload = () => {
    // Decode base64 to binary
    const binaryString = atob(imageBase64);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    // Create blob and download
    const blob = new Blob([bytes], { type: 'image/png' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `pattern_${filename}_${width}px.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bitmap-viewer">
      <div className="bitmap-viewer__header">
        <h4>Binary Content Visualization</h4>
        <p className="bitmap-viewer__subtitle">
          Grayscale representation of byte values (0-255) | Width: {width} bytes
        </p>
      </div>

      <div className="bitmap-viewer__container">
        <img
          src={`data:image/png;base64,${imageBase64}`}
          alt="Binary content bitmap"
          className="bitmap-viewer__image"
        />
      </div>

      <div className="bitmap-viewer__footer">
        <button className="btn btn-primary" onClick={handleDownload}>
          <Download size={18} />
          Download PNG
        </button>
      </div>
    </div>
  );
};

export default BitmapViewer;
