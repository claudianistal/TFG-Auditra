import React, { useState, useEffect } from 'react';
import { Music } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import './styles/FileBar.css';
import { useFiles } from '../context/FileContext';
import { getAudioUrl } from '../api/audioService';
import AudioPlayer from './AudioPlayer';

const FileBar = () => {
	const { t } = useTranslation();
	const { files } = useFiles();
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

	if (files.length === 0) {
		return null;
	}

	return (
		<div className="file-bar">
			<div className="file-bar__header">
				<span className="file-bar__title">{t('components.fileBar.loadedFile')}</span>
				<span className="file-bar__count">{files.length}</span>
			</div>
			<div className="file-bar__list">
				{files.map((file) => (
					<div key={file.id} className="file-bar__item">
						<div className="file-bar__header-row">
							<Music className="file-bar__icon" size={18} strokeWidth={2} />
							<span className="file-bar__name">{file.name}</span>
							{file.progress !== 100 && (
								<span className="file-bar__progress">
									{file.progress}%
								</span>
							)}
						</div>
						<div className="file-bar__player">
							{audioUrls[file.id] && (
								<AudioPlayer audioFile={audioUrls[file.id]} showFileName={false} />
							)}
						</div>
					</div>
				))}
			</div>
		</div>
	);
};

export default FileBar;
