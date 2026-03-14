import React from 'react';
import { useTranslation } from 'react-i18next';
import './Common.css'

const Dashboard = () => {
	const { t } = useTranslation();

	return (
		<section className="page-card">
			<h3>{t('pages.dashboard.title')}</h3>
			<p>{t('pages.dashboard.description')}</p>
		</section>
	);
};

export default Dashboard;