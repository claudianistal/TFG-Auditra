import React from 'react';
import { useTranslation } from 'react-i18next';
import '../styles/ProcessingQueue.css';

const ProcessingQueue = ({ files, onRemoveFile }) => {
	const { t } = useTranslation();

	if (files.length === 0) return null;

	return (
		<div className="processing-queue">
			<div className="processing-queue__header">
				<h3 className="processing-queue__title">{t('pages.audioIngestion.processingQueue')}</h3>
				<span className="processing-queue__badge">
					{files.length} {t('pages.audioIngestion.active')}
				</span>
			</div>

			<div className="processing-queue__list">
				{files.map((file) => (
					<div key={file.id} className="queue-item">
						<div className="queue-item__info">
							<span className="queue-item__icon">▶</span>
							<span className="queue-item__name">{file.name}</span>
						</div>
						<div className="queue-item__progress-bar">
							<div
								className="queue-item__progress"
								style={{ width: `${file.progress}%` }}
							></div>
						</div>
						<span className="queue-item__percent">{file.progress}%</span>
						<button
							className="queue-item__remove"
							onClick={() => onRemoveFile(file.id)}
							title="Remove file"
						>
							×
						</button>
					</div>
				))}
			</div>
		</div>
	);
};

export default ProcessingQueue;
