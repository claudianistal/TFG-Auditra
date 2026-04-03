import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { AlertCircle, Music } from 'lucide-react';
import FileBar from '../components/FileBar';
import BitmapViewer from '../components/BitmapViewer';
import HexDumpViewer from '../components/HexDumpViewer';
import { useFiles } from '../context/FileContext';
import { getPatterns } from '../api/audioService';
import './Common.css';
import './PatternsPage.css';

const PatternsPage = () => {
	const { t } = useTranslation();
	const { files, updateFile } = useFiles();
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);
	const [width, setWidth] = useState(512);

	// Get the currently loaded file (first one in the list)
	const currentFile = files.length > 0 ? files[0] : null;

	const handleAnalyzePatterns = async () => {
		if (!currentFile) {
			setError('No file loaded');
			return;
		}

		// Validate width
		if (width < 128 || width > 2048) {
			setError('Width must be between 128 and 2048 bytes');
			return;
		}

		setLoading(true);
		setError(null);

		try {
			const response = await getPatterns(currentFile.id, width);
			const { image_base64, hex_start, hex_end, total_file_size, width_used } = response.data;

			// Update the file in context with patterns
			updateFile(currentFile.id, {
				patterns: {
					image_base64,
					hex_start,
					hex_end,
					total_file_size,
					width_used,
				},
				patternsLoading: false,
				patternsError: null,
			});
		} catch (err) {
			const errorMessage = err.response?.data?.detail || 'Error analyzing patterns';
			setError(errorMessage);
			updateFile(currentFile.id, {
				patternsError: errorMessage,
				patternsLoading: false,
			});
		} finally {
			setLoading(false);
		}
	};

	// Width presets for easy selection
	const widthPresets = [128, 256, 512, 1024, 2048];

	return (
		<>
			<FileBar />
			<section className="page-card">
				<h3>{t('pages.patterns.title') || 'Pattern Analysis'}</h3>
				<p>
					{t('pages.patterns.description') ||
						'Analyze binary patterns and padding in audio files. Adjust the bitmap width to observe different pattern scales.'}
				</p>

				{/* No file loaded message */}
				{!currentFile && (
					<div className="patterns-no-file">
						<Music size={48} />
						<p>
							{t('pages.patterns.noFileMessage') ||
								'Load a file in the audio ingestion section first.'}
						</p>
					</div>
				)}

				{/* File loaded section */}
				{currentFile && (
					<div className="patterns-section">
						{/* File info and controls */}
						<div className="patterns-controls">
							<div className="patterns-file-info">
								<Music size={20} />
								<span>{currentFile.name}</span>
							</div>

							{/* Width selector */}
							<div className="patterns-width-selector">
								<label htmlFor="width-input">Bitmap Width (bytes):</label>
								<div className="patterns-width-inputs">
									{/* Presets */}
									<div className="patterns-width-presets">
										{widthPresets.map((preset) => (
											<button
												key={preset}
												className={`preset-btn ${width === preset ? 'preset-btn--active' : ''}`}
												onClick={() => setWidth(preset)}
												disabled={loading}
											>
												{preset}
											</button>
										))}
									</div>
									{/* Custom input */}
									<input
										id="width-input"
										type="number"
										min="128"
										max="2048"
										step="128"
										value={width}
										onChange={(e) => setWidth(parseInt(e.target.value) || 512)}
										disabled={loading}
										className="patterns-width-input"
									/>
								</div>
							</div>

							{/* Analyze button */}
							<button
								className={`patterns-analyze-button ${loading ? 'patterns-analyze-button--loading' : ''}`}
								onClick={handleAnalyzePatterns}
								disabled={loading || !currentFile}
							>
								{loading ? 'Analyzing...' : 'Analyze Patterns'}
							</button>
						</div>

						{/* Error message if analysis failed */}
						{error && (
							<div className="patterns-error-banner">
								<AlertCircle size={20} />
								<span>{error}</span>
							</div>
						)}

						{/* Display visualizations if available */}
						{currentFile.patterns && !loading && !error && (
							<div className="patterns-results">
								<BitmapViewer
									imageBase64={currentFile.patterns.image_base64}
									filename={currentFile.name}
									width={currentFile.patterns.width_used}
								/>

								<HexDumpViewer
									hexStart={currentFile.patterns.hex_start}
									hexEnd={currentFile.patterns.hex_end}
									totalFileSize={currentFile.patterns.total_file_size}
								/>
							</div>
						)}

						{/* Loading spinner */}
						{loading && (
							<div className="patterns-loading">
								<div className="spinner"></div>
								<p>Analyzing patterns...</p>
							</div>
						)}
					</div>
				)}
			</section>
		</>
	);
};

export default PatternsPage;
