import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { uploadAudioFile, deleteAudioFile } from '../api/audioService';
import DropZone from '../components/audioIngestion/DropZone';
import ProcessingQueue from '../components/audioIngestion/ProcessingQueue';
import AnalysisTips from '../components/audioIngestion/AnalysisTips';
import { useFiles } from '../context/FileContext';
import './AudioIngestion.css';

const AudioIngestion = () => {
	const { t } = useTranslation();
	const { files, addFiles, removeFile: removeFileFromContext } = useFiles();
	const [loading, setLoading] = useState(false);

	const SUPPORTED_FORMATS = ['audio/wav', 'audio/mpeg', 'audio/mp4'];
	const MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024; // 2GB

	const validateFile = (file) => {
		if (!SUPPORTED_FORMATS.includes(file.type)) {
			alert(`${file.name} - ${t('validation.unsupportedFormat')}`);
			return false;
		}
		if (file.size > MAX_FILE_SIZE) {
			alert(`${file.name} - ${t('validation.fileTooLarge')}`);
			return false;
		}
		return true;
	};

	const processFiles = async (filesToProcess) => {
		// Validar: solo permitir 1 archivo a la vez
		if (files.length > 0) {
			alert(t('errors.onlyOneFileAtATime') || 'Se está procesando un archivo. Espera a que termine.');
			return;
		}

		if (filesToProcess.length > 1) {
			alert(t('errors.onlyOneFile') || 'Solo puedes cargar un archivo a la vez.');
			return;
		}

		setLoading(true);
		const validFiles = [];

		for (let file of filesToProcess) {
			if (validateFile(file)) {
				validFiles.push(file);
			}
		}

		if (validFiles.length === 0) {
			setLoading(false);
			return;
		}

		try {
			const newFilesArray = [];
			for (let file of validFiles) {
				const formData = new FormData();
				formData.append('file', file);

				const response = await uploadAudioFile(formData);
				const newFile = {
					id: response.data.id || Date.now(),
					name: file.name,
					progress: 100,
					status: 'ready',
					hash: response.data.hash,
					hashAlgorithm: response.data.hash_algorithm
				};
				newFilesArray.push(newFile);
			}
			addFiles(newFilesArray);
		} catch (error) {
			console.error('Error uploading file:', error);
			alert(t('errors.uploadFailed') || 'Error al cargar el archivo');
		} finally {
			setLoading(false);
		}
	};

	const removeFile = async (fileId) => {
		try {
			// Eliminar archivo del backend
			await deleteAudioFile(fileId);
			// Eliminar del contexto global
			removeFileFromContext(fileId);
		} catch (error) {
			console.error('Error deleting file:', error);
			// Aun así lo removemos del frontend para mejor UX
			removeFileFromContext(fileId);
		}
	};

	return (
		<div className="audio-ingestion">
			<div className="audio-ingestion__header">
					<div className="audio-ingestion__info-group">
						<p className="audio-ingestion__info-label">{t('pages.audioIngestion.supportedFormatsInfo')}</p>
						<p className="audio-ingestion__info-value">{t('pages.audioIngestion.formatsLabel')}</p>
					</div>
					<div className="audio-ingestion__separator"></div>
					<div className="audio-ingestion__info-group">
						<p className="audio-ingestion__info-label">{t('pages.audioIngestion.maxFileSize')}</p>
						<p className="audio-ingestion__info-value">{t('pages.audioIngestion.maxPerFile')}</p>
					</div>
					<div className="audio-ingestion__separator"></div>
					<div className="audio-ingestion__info-group">
						<p className="audio-ingestion__info-label">{t('pages.audioIngestion.analysisMethod')}</p>
						<p className="audio-ingestion__info-value">{t('pages.audioIngestion.analysisMethodLabel')}</p>
					</div>
					<div className="audio-ingestion__separator"></div>
					<div className="audio-ingestion__info-group">
						<p className="audio-ingestion__info-label">{t('pages.audioIngestion.securityLabel')}</p>
						<p className="audio-ingestion__info-value">{t('pages.audioIngestion.encryption')}</p>
					</div>
			</div>

			<div className="audio-ingestion__content">
				<div className="audio-ingestion__main">
					<DropZone onFilesSelected={processFiles} isLoading={loading} hasActiveFile={files.length > 0} />
					<ProcessingQueue files={files} onRemoveFile={removeFile} />
				</div>

				<AnalysisTips />
			</div>
		</div>
	);
};

export default AudioIngestion;
