import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { AlertCircle, Music, Copy, Check } from 'lucide-react';
import FileBar from '../components/FileBar';
import ConfirmationBanner from '../components/ConfirmationBanner';
import BitmapViewer from '../components/BitmapViewer';
import HexDumpViewer from '../components/HexDumpViewer';
import { useFiles } from '../context/FileContext';
import { getAutosimilarity, getPadding } from '../api/audioService';
import './Common.css';
import './PatternsPage.css';

const PatternsPage = () => {
	const { t } = useTranslation();
	const { files, updateFile } = useFiles();
	const [loading, setLoading] = useState(false);
	const [recalculatingWidth, setRecalculatingWidth] = useState(false);
	const [copiedFeedback, setCopiedFeedback] = useState(false);
	const [error, setError] = useState(null);
	const [width, setWidth] = useState(512);
	const [activeTab, setActiveTab] = useState('autosimilarity'); // 'autosimilarity' or 'padding'
	const [confirmation, setConfirmation] = useState({
		visible: false,
		executionTime: 0,
		type: 'success',
	});

	// Get the currently loaded file (first one in the list)
	const currentFile = files.length > 0 ? files[0] : null;

	// Reset error state when file changes
	useEffect(() => {
		setError(null);
	}, [currentFile?.id]);

	const handleAnalyzePatterns = async () => {
		if (!currentFile) {
			setError(t('pages.patterns.noFileLoaded') || 'No file loaded');
			return;
		}

		setLoading(true);
		setError(null);
		const startTime = Date.now();

		try {
			// Make both requests in parallel
			const [autosimilarityResponse, paddingResponse] = await Promise.all([
				getAutosimilarity(currentFile.id, width),
				getPadding(currentFile.id),
			]);

			const { image_base64, width_used } = autosimilarityResponse.data;
			const { hex_start, hex_end, total_file_size } = paddingResponse.data;

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

			// Show confirmation banner with total execution time
			setConfirmation({
				visible: true,
				executionTime: Date.now() - startTime,
				type: 'success',
			});
		} catch (err) {
			const errorMessage = err.response?.data?.detail || 'Error analyzing patterns';
			setError(errorMessage);
			updateFile(currentFile.id, {
				patternsError: errorMessage,
				patternsLoading: false,
			});

			// Show error confirmation banner
			setConfirmation({
				visible: true,
				executionTime: Date.now() - startTime,
				type: 'error',
			});
		} finally {
			setLoading(false);
		}
	};

	const handleRecalculateAutosimilarity = async (newWidth = null) => {
		if (!currentFile) {
			setError(t('pages.patterns.noFileLoaded') || 'No file loaded');
			return;
		}

		const widthToUse = newWidth !== null ? newWidth : width;

		// Validate width
		if (widthToUse < 128 || widthToUse > 2048) {
			setError(t('pages.patterns.invalidWidth') || 'Width must be between 128 and 2048 bytes');
			return;
		}

		// Update width state if a new width was provided
		if (newWidth !== null) {
			setWidth(newWidth);
		}

		setRecalculatingWidth(true);
		setError(null);
		const startTime = Date.now();

		try {
			const response = await getAutosimilarity(currentFile.id, widthToUse);
			const { image_base64, width_used, execution_time_ms } = response.data;

			// Update only the bitmap, keep hex dumps
			updateFile(currentFile.id, {
				patterns: {
					...currentFile.patterns,
					image_base64,
					width_used,
				},
				patternsLoading: false,
				patternsError: null,
			});

			// Show confirmation banner
			setConfirmation({
				visible: true,
				executionTime: execution_time_ms || Date.now() - startTime,
				type: 'success',
			});
		} catch (err) {
			const errorMessage = err.response?.data?.detail || 'Error recalculating autosimilarity';
			setError(errorMessage);
			updateFile(currentFile.id, {
				patternsError: errorMessage,
				patternsLoading: false,
			});

			// Show error confirmation banner
			setConfirmation({
				visible: true,
				executionTime: Date.now() - startTime,
				type: 'error',
			});
		} finally {
			setRecalculatingWidth(false);
		}
	};

	// Width presets for easy selection
	const widthPresets = [128, 256, 512, 1024, 2048];

	const handleCopyImage = async () => {
		if (!currentFile?.patterns?.image_base64) return;

		try {
			// Decode base64 to blob
			const binaryString = atob(currentFile.patterns.image_base64);
			const bytes = new Uint8Array(binaryString.length);
			for (let i = 0; i < binaryString.length; i++) {
				bytes[i] = binaryString.charCodeAt(i);
			}

			const blob = new Blob([bytes], { type: 'image/png' });
			
			// Copy to clipboard using the Clipboard API
			await navigator.clipboard.write([
				new ClipboardItem({
					'image/png': blob,
				}),
			]);

			// Show feedback
			setCopiedFeedback(true);
			setTimeout(() => setCopiedFeedback(false), 2000);
		} catch (err) {
			console.error('Failed to copy image:', err);
		}
	};

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

							{/* Analyze button */}
							<button
								className={`patterns-analyze-button ${loading ? 'patterns-analyze-button--loading' : ''}`}
								onClick={handleAnalyzePatterns}
							disabled={loading || !currentFile || !!currentFile.patterns}
							>
								{loading ? t('pages.patterns.analyzing') || 'Analyzing...' : t('pages.patterns.analyzeButton') || 'Analyze Patterns'}
							</button>
						</div>
					{/* Confirmation Banner */}
					{confirmation.visible && (
						<ConfirmationBanner
							isVisible={confirmation.visible}
							type={confirmation.type}
							message={
								confirmation.type === 'success'
									? t('components.confirmationBanner.patternsSuccess') || '✓ Pattern analysis completed'
									: t('components.confirmationBanner.patternsError') || '✗ Error analyzing patterns'
							}
							executionTime={confirmation.executionTime}
							onDismiss={() => setConfirmation({ ...confirmation, visible: false })}
						/>
					)}
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

											{/* Width selector - only visible in autosimilarity tab */}
											<div className="patterns-width-selector">
												<label>{t('pages.patterns.resolution') || 'Resolution (bytes per row)'}</label>
												<p className="patterns-width-description">{t('pages.patterns.resolutionDescription') || 'Press the buttons below to change the resolution'}</p>
											<div className="patterns-width-controls">
												<div className="patterns-width-presets">
													{widthPresets.map((preset) => (
														<button
															key={preset}
															className={`preset-btn ${width === preset ? 'preset-btn--active' : ''}`}
														onClick={() => handleRecalculateAutosimilarity(preset)}
															disabled={recalculatingWidth}
														>
															{preset}
														</button>
													))}
												</div>
												<button
													className="btn btn-copy"
													onClick={handleCopyImage}
													disabled={!currentFile?.patterns?.image_base64}
													title={t('pages.patterns.copyImage') || 'Copy image to clipboard'}
												>
													{copiedFeedback ? <Check size={16} /> : <Copy size={16} />}
													{copiedFeedback ? t('pages.patterns.copyImage') || 'Copied!' : t('pages.patterns.copy') || 'Copy'}
												</button>
											</div>
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
