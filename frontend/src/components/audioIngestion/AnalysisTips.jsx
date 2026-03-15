import React from 'react';
import { useTranslation } from 'react-i18next';
import '../styles/AnalysisTips.css';

const AnalysisTips = () => {
	const { t } = useTranslation();

	const tips = [
		{
			title: t('pages.audioIngestion.highNoiseDetection'),
			text: t('pages.audioIngestion.highNoiseText'),
		},
		{
			title: t('pages.audioIngestion.batchProcessing'),
			text: t('pages.audioIngestion.batchText'),
		},
	];

	return (
		<aside className="analysis-tips">
			<div className="analysis-tips__header">
				<h3 className="analysis-tips__title">{t('pages.audioIngestion.analysisTips')}</h3>
			</div>

			<div className="analysis-tips__list">
				{tips.map((tip, idx) => (
					<div key={idx} className="analysis-tip">
						<h4 className="analysis-tip__title">{tip.title}</h4>
						<p className="analysis-tip__text">{tip.text}</p>
					</div>
				))}
			</div>
		</aside>
	);
};

export default AnalysisTips;
