import React from 'react';
import { useTranslation } from 'react-i18next';

const MetadataPage = () => {
	const { t } = useTranslation();

	return (
		<section className="page-card">
			<h3>{t('pages.metadata.title')}</h3>
			<p>{t('pages.metadata.description')}</p>
		</section>
	);
};

export default MetadataPage;
