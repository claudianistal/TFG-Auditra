import React, { createContext, useContext, useState, useEffect } from 'react';

const FileContext = createContext();

export const FileProvider = ({ children }) => {
	const [files, setFiles] = useState([]);
	const [isInitialized, setIsInitialized] = useState(false);

	// Cargar archivos de localStorage al montar
	useEffect(() => {
		try {
			const storedFiles = localStorage.getItem('uploadedFiles');
			if (storedFiles) {
				const parsedFiles = JSON.parse(storedFiles);
				setFiles(parsedFiles);
			}
		} catch (error) {
			console.error('Error loading files from localStorage:', error);
		} finally {
			setIsInitialized(true);
		}
	}, []);

	// Guardar archivos en localStorage cada vez que cambian
	useEffect(() => {
		if (isInitialized) {
			try {
				localStorage.setItem('uploadedFiles', JSON.stringify(files));
			} catch (error) {
				console.error('Error saving files to localStorage:', error);
			}
		}
	}, [files, isInitialized]);

	const addFiles = (newFiles) => {
		setFiles((prev) => [...prev, ...newFiles]);
	};

	const removeFile = (fileId) => {
		setFiles((prev) => prev.filter((f) => f.id !== fileId));
	};

	const updateFile = (fileId, updates) => {
		setFiles((prev) =>
			prev.map((f) => (f.id === fileId ? { ...f, ...updates } : f))
		);
	};

	const clearAll = () => {
		setFiles([]);
	};

	const value = {
		files,
		addFiles,
		removeFile,
		updateFile,
		clearAll,
		isInitialized,
	};

	return <FileContext.Provider value={value}>{children}</FileContext.Provider>;
};

export const useFiles = () => {
	const context = useContext(FileContext);
	if (!context) {
		throw new Error('useFiles debe ser usado dentro de un FileProvider');
	}
	return context;
};
