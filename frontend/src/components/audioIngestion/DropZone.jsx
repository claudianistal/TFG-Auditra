import React, { useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import '../styles/DropZone.css';

const DropZone = ({ onFilesSelected, isLoading, hasActiveFile }) => {
	const { t } = useTranslation();
	const [dragActive, setDragActive] = useState(false);
	const fileInputRef = useRef(null);

	const handleDrag = (e) => {
		e.preventDefault();
		e.stopPropagation();
		if (e.type === 'dragenter' || e.type === 'dragover') {
			setDragActive(true);
		} else if (e.type === 'dragleave') {
			setDragActive(false);
		}
	};

	const handleDrop = (e) => {
		e.preventDefault();
		e.stopPropagation();
		setDragActive(false);
		const files = e.dataTransfer.files;
		onFilesSelected(files);
	};

	const handleBrowseClick = () => {
		fileInputRef.current?.click();
	};

	const handleFileInputChange = (e) => {
		const files = e.target.files;
		if (files) {
			onFilesSelected(files);
			// Reset input file para permitir seleccionar el mismo archivo nuevamente
			e.target.value = '';
		}
	};

	return (
		<div
			className={`drop-zone ${dragActive ? 'drop-zone--active' : ''}`}
			onDragEnter={handleDrag}
			onDragLeave={handleDrag}
			onDragOver={handleDrag}
			onDrop={handleDrop}
		>
			<div className="drop-zone__content">
				<div className="drop-zone__header">
					<h2 className="drop-zone__title">{t('pages.audioIngestion.dragDrop')}</h2>
				</div>

				<p className="drop-zone__info">{t('pages.audioIngestion.uploadInfo')}</p>
				
				<div className="drop-zone__buttons">
					<button
						className="btn btn--primary"
						onClick={handleBrowseClick}
						disabled={isLoading || hasActiveFile}
					>
						{t('pages.audioIngestion.browseFiles')}
					</button>
				</div>

				<input
					ref={fileInputRef}
					type="file"
					multiple
					accept=".wav,.mp3,.flac,.aiff"
					onChange={handleFileInputChange}
					style={{ display: 'none' }}
				/>
			</div>
		</div>
	);
};

export default DropZone;
