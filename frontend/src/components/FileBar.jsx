import React from 'react';
import { Music } from 'lucide-react';
import './styles/FileBar.css';
import { useFiles } from '../context/FileContext';

const FileBar = () => {
	const { files } = useFiles();

	if (files.length === 0) {
		return null;
	}

	return (
		<div className="file-bar">
			<div className="file-bar__header">
				<span className="file-bar__title">Archivos cargados</span>
				<span className="file-bar__count">{files.length}</span>
			</div>
			<div className="file-bar__list">
				{files.map((file) => (
					<div key={file.id} className="file-bar__item" title={file.name}>
						<Music className="file-bar__icon" size={18} strokeWidth={2} />
						<span className="file-bar__name">{file.name}</span>
						{file.progress !== 100 && (
							<span className="file-bar__progress">
								{file.progress}%
							</span>
						)}
					</div>
				))}
			</div>
		</div>
	);
};

export default FileBar;
