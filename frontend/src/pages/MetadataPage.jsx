import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { AlertCircle, Music } from 'lucide-react';
import FileBar from '../components/FileBar';
import ConfirmationBanner from '../components/ConfirmationBanner';
import MetadataTable from '../components/MetadataTable';
import { useFiles } from '../context/FileContext';
import { getMetadata } from '../api/audioService';
import './Common.css';
import './MetadataPage.css';

const MetadataPage = () => {
	const { t } = useTranslation();
	const { files, updateFile } = useFiles();
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);
	const [analyzed, setAnalyzed] = useState(false);
	const [confirmation, setConfirmation] = useState({
		visible: false,
		executionTime: 0,
		type: 'success',
	});

	// Get the currently loaded file (first one in the list)
	const currentFile = files.length > 0 ? files[0] : null;

	// Reset analyzed state when file changes
	useEffect(() => {
		setAnalyzed(false);
		setError(null);
	}, [currentFile?.id]);

	const handleAnalyzeMetadata = async () => {
		if (!currentFile) {
			setError(t('pages.metadata.noFileLoaded') || 'No file loaded');
			return;
		}

		setLoading(true);
		setError(null);
		const startTime = Date.now();

		try {
			const response = await getMetadata(currentFile.id);
			const { metadata, execution_time_ms } = response.data;

			// Update the file in context with metadata
			updateFile(currentFile.id, {
				metadata,
				metadataLoading: false,
				metadataError: null,
			});

			// Mark as analyzed after successful analysis
			setAnalyzed(true);

			// Show confirmation banner
			setConfirmation({
				visible: true,
				executionTime: execution_time_ms || Date.now() - startTime,
				type: 'success',
			});
		} catch (err) {
			const errorMessage = err.response?.data?.detail || 'Error extracting metadata';
			setError(errorMessage);
			updateFile(currentFile.id, {
				metadataError: errorMessage,
				metadataLoading: false,
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

	return (
		<>
			<FileBar />
			<section className="page-card">
				<h3>{t('pages.metadata.title')}</h3>
				<p>{t('pages.metadata.description')}</p>

				{/* No file loaded message */}
				{!currentFile && (
					<div className="metadata-no-file">
						<Music size={48} />
						<p>{t('pages.metadata.noFileMessage') || 'Carga un archivo en la sección de \'Cargar Audio\' primero.'}</p>
					</div>
				)}

				{/* File loaded section */}
				{currentFile && (
					<div className="metadata-section">
						<div className="metadata-file-info">
							<div className="metadata-file-name">
								<Music size={20} />
								<span>{currentFile.name}</span>
							</div>
						<button
							className={'metadata-analyze-button ' + (loading ? 'metadata-analyze-button--loading' : '')}
							onClick={handleAnalyzeMetadata}
							disabled={loading || analyzed}
						>
							{loading ? t('pages.metadata.analyzing') || 'Analyzing...' : t('pages.metadata.analyzeButton') || 'Analyze Metadata'}
						</button>
						</div>

						{/* Confirmation Banner */}
						{confirmation.visible && (
							<ConfirmationBanner
								isVisible={confirmation.visible}
								type={confirmation.type}
								message={
									confirmation.type === 'success'
										? t('components.confirmationBanner.metadataSuccess') || '✓ Metadata analysis completed'
										: t('components.confirmationBanner.metadataError') || '✗ Error analyzing metadata'
								}
								executionTime={confirmation.executionTime}
								onDismiss={() => setConfirmation({ ...confirmation, visible: false })}
							/>
						)}

						{/* Error message if extraction failed */}
						{error && (
							<div className="metadata-error-banner">
								<AlertCircle size={20} />
								<span>{error}</span>
							</div>
						)}

						{/* Display metadata table if available */}
						{currentFile.metadata && !loading && !error && (
							<MetadataTable
								metadata={currentFile.metadata}
								loading={false}
								error={null}
							/>
						)}

						{/* Show loading spinner if fetching */}
						{loading && <MetadataTable metadata={null} loading={true} error={null} />}
					</div>
				)}
			</section>
		</>
	);
};

export default MetadataPage;
