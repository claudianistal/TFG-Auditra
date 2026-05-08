import React, { useState, useEffect } from 'react';
import { Trash2, Copy } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { getAudioUrl } from '../../api/audioService';
import '../styles/ProcessingQueue.css';
import AudioPlayer from '../AudioPlayer';

const ProcessingQueue = ({ files, onRemoveFile }) => {
	const { t } = useTranslation();
	const [audioUrls, setAudioUrls] = useState({});

	// Load audio URLs for each file
    useEffect(() => {
        const activeUrls = [];

        const loadAudioUrls = async () => {
            
            const urls = {};
            
            await Promise.all(files.map(async (file) => {
                try {
                    const url = await getAudioUrl(file.id);
                    urls[file.id] = url;
                    if (url) activeUrls.push(url); 
                } catch (error) {
                    console.error(`Error loading audio URL for file ${file.id}:`, error);
                    urls[file.id] = null;
                }
            }));
            
            setAudioUrls(urls);
        };

        if (files.length > 0) {
            loadAudioUrls();
        }

        // Cleanup: revoke blob URLs on unmount or when files change
        return () => {
           
            activeUrls.forEach(url => {
                URL.revokeObjectURL(url);
            });
        };
    }, [files]);

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
						<div className="queue-item__header">
							<span className="queue-item__name">{file.name}</span>
							<button
								className="queue-item__remove"
								onClick={() => onRemoveFile(file.id)}
								title="Remove file"
								aria-label="Eliminar archivo"
							>
								<Trash2 size={18} strokeWidth={2} />
							</button>
						</div>
						
						<div className="queue-item__player">
								{audioUrls[file.id] && (
									<AudioPlayer audioFile={audioUrls[file.id]} showFileName={false} />
								)}
						</div>

						<div className="queue-item__details queue-item__details--expanded">
							<div className="queue-item__detail-row">
								<span className="queue-item__label">Hash ({file.hashAlgorithm || 'SHA-256'}):</span>
								<span className="queue-item__hash">{file.hash}</span>
								<button
									className="queue-item__copy-hash"
									onClick={() => navigator.clipboard.writeText(file.hash)}
									title="Copy hash"
									aria-label="Copiar hash"
								>
									<Copy size={16} strokeWidth={2} />
								</button>
							</div>
							
						</div>
					</div>
				))}
			</div>
		</div>
	);
};

export default ProcessingQueue;
