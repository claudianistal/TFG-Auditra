import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import '../styles/ProcessingQueue.css';

const ProcessingQueue = ({ files, onRemoveFile }) => {
	const { t } = useTranslation();
	const [expandedFileId, setExpandedFileId] = useState(null);

	if (files.length === 0) return null;

	const toggleExpand = (fileId) => {
		setExpandedFileId(expandedFileId === fileId ? null : fileId);
	};

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
						<div className="queue-item__header">
							<div className="queue-item__info">
								<button
									className="queue-item__expand"
									onClick={() => toggleExpand(file.id)}
									title="Show details"
								>
									{expandedFileId === file.id ? '▼' : '▶'}
								</button>
								<span className="queue-item__name">{file.name}</span>
							</div>
							<button
								className="queue-item__remove"
								onClick={() => onRemoveFile(file.id)}
								title="Remove file"
							>
								×
							</button>
						</div>
						<div className="queue-item__progress-bar">
							<div
								className="queue-item__progress"
								style={{ width: `${file.progress}%` }}
							></div>
						</div>
						<span className="queue-item__percent">{file.progress}%</span>

						{expandedFileId === file.id && (
							<div className="queue-item__details">
								<div className="queue-item__detail-row">
									<span className="queue-item__label">Hash ({file.hashAlgorithm || 'SHA-256'}):</span>
									<span className="queue-item__hash">{file.hash}</span>
									<button
										className="queue-item__copy-hash"
										onClick={() => navigator.clipboard.writeText(file.hash)}
										title="Copy hash"
									>
										📋
									</button>
								</div>
							</div>
						)}
					</div>
				))}
			</div>
		</div>
	);
};

export default ProcessingQueue;
