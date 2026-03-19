import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { AlertCircle, Music } from 'lucide-react';
import FileBar from '../components/FileBar';
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

	// Get the currently loaded file (first one in the list)
	const currentFile = files.length > 0 ? files[0] : null;

	const handleAnalyzeMetadata = async () => {
		if (!currentFile) {
			setError('No file loaded');
			return;
		}

		setLoading(true);
		setError(null);

		try {
			const response = await getMetadata(currentFile.id);
			const { metadata } = response.data;

			// Update the file in context with metadata
			updateFile(currentFile.id, {
				metadata,
				metadataLoading: false,
				metadataError: null,
			});
		} catch (err) {
			const errorMessage = err.response?.data?.detail || 'Error extracting metadata';
			setError(errorMessage);
			updateFile(currentFile.id, {
				metadataError: errorMessage,
				metadataLoading: false,
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
						<p>{t('pages.metadata.noFileMessage') || 'Carga un archivo en la sección de ingesta de audio primero.'}</p>
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
								disabled={loading}
							>
								{loading ? 'Analizando...' : 'Analizar Metadatos'}
							</button>
						</div>

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
