import React from 'react';
import { useTranslation } from 'react-i18next';
import FileBar from '../components/FileBar';
import './Common.css'

const MetadataPage = () => {
	const { t } = useTranslation();

	return (
		<>
			<FileBar />
			<section className="page-card">
				<h3>{t('pages.metadata.title')}</h3>
				<p>{t('pages.metadata.description')}</p>
			</section>
		</>
	);
};

export default MetadataPage;
