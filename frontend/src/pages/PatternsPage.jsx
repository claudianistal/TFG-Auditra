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
	const [activeTab, setActiveTab] = useState('autosimilarity'); // 'autosimilarity' or 'padding'

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
								<label>{t('pages.patterns.resolution') || 'Resolution (bytes per row)'}</label>
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
							</div>

							{/* Analyze button */}
							<button
								className={`patterns-analyze-button ${loading ? 'patterns-analyze-button--loading' : ''}`}
								onClick={handleAnalyzePatterns}
								disabled={loading || !currentFile}
							>
								{loading ? t('pages.patterns.analyzing') || 'Analyzing...' : t('pages.patterns.analyzeButton') || 'Analyze Patterns'}
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
								{/* Tab navigation */}
								<div className="patterns-tabs">
									<button
										className={`patterns-tab ${activeTab === 'autosimilarity' ? 'patterns-tab--active' : ''}`}
										onClick={() => setActiveTab('autosimilarity')}
									>
										{t('pages.patterns.tabs.autosimilarity') || 'Autosimilarity'}
									</button>
									<button
										className={`patterns-tab ${activeTab === 'padding' ? 'patterns-tab--active' : ''}`}
										onClick={() => setActiveTab('padding')}
									>
										{t('pages.patterns.tabs.padding') || 'Padding'}
									</button>
								</div>

								{/* Tab content: Autosimilarity */}
								{activeTab === 'autosimilarity' && (
									<div className="patterns-tab-content">
										<div className="analysis-section analysis-section--bitmap">
											<div className="analysis-section__header">
												<h4>{t('pages.patterns.autosimilarityTitle') || 'Audio Content Visualization'}</h4>
												<p className="analysis-section__description">
													{t('pages.patterns.autosimilarityDesc') || 'Autosimilitude analysis: Grayscale representation of byte values. Patterns reveal the statistical structure and characteristics of the audio data.'}
												</p>
											</div>
											<BitmapViewer
												imageBase64={currentFile.patterns.image_base64}
												filename={currentFile.name}
												width={currentFile.patterns.width_used}
											/>
										</div>
									</div>
								)}

								{/* Tab content: Padding */}
								{activeTab === 'padding' && (
									<div className="patterns-tab-content">
										<div className="analysis-section analysis-section--padding">
											<div className="analysis-section__header">
												<h4>{t('pages.patterns.paddingTitle') || 'Padding & File Boundaries'}</h4>
												<p className="analysis-section__description">
													{t('pages.patterns.paddingDesc') || 'Inspect the first and last 1024 bytes of the file to detect padding (0x00 or 0xFF) that may indicate file manipulation or encoding artifacts.'}
												</p>
											</div>
											<HexDumpViewer
												hexStart={currentFile.patterns.hex_start}
												hexEnd={currentFile.patterns.hex_end}
												totalFileSize={currentFile.patterns.total_file_size}
											/>
										</div>
									</div>
								)}
							</div>
						)}

						{/* Loading spinner */}
						{loading && (
							<div className="patterns-loading">
								<div className="spinner"></div>
								<p>{t('pages.patterns.analyzing') || 'Analyzing patterns...'}</p>
							</div>
						)}
					</div>
				)}
			</section>
		</>
	);
};

export default PatternsPage;
