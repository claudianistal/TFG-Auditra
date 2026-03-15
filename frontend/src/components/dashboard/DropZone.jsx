import React, { useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import '../styles/DropZone.css';

const DropZone = ({ onFilesSelected, isLoading }) => {
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
					<h2 className="drop-zone__title">{t('pages.dashboard.dragDrop')}</h2>
				</div>
				
				<p className="drop-zone__description">{t('pages.dashboard.supportedFormats')}</p>

				<div className="drop-zone__buttons">
					<button
						className="btn btn--primary"
						onClick={handleBrowseClick}
						disabled={isLoading}
					>
						{t('pages.dashboard.browseFiles')}
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

				<div className="drop-zone__specs">
					<div className="drop-zone__spec-item">
						<span className="drop-zone__spec-label">{t('pages.dashboard.encryption')}</span>
					</div>
					<div className="drop-zone__spec-item">
						<span className="drop-zone__spec-label">{t('pages.dashboard.chainOfCustody')}</span>
					</div>
					<div className="drop-zone__spec-item">
						<span className="drop-zone__spec-label">{t('pages.dashboard.maxPerFile')}</span>
					</div>
				</div>
			</div>
		</div>
	);
};

export default DropZone;
