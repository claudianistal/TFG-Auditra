import React from 'react';
import { useTranslation } from 'react-i18next';
import { AlertCircle, Clock } from 'lucide-react';

const RiskScoreCard = ({ score, likelihood, color, analysisDate }) => {
	const { t } = useTranslation();
	
	const formatAnalysisDateTime = (isoDate) => {
		if (!isoDate) return null;
		try {
			const date = new Date(isoDate);
			// Extract UTC components without timezone conversion
			const year = date.getUTCFullYear();
			const month = String(date.getUTCMonth() + 1).padStart(2, '0');
			const day = String(date.getUTCDate()).padStart(2, '0');
			const hours = String(date.getUTCHours()).padStart(2, '0');
			const minutes = String(date.getUTCMinutes()).padStart(2, '0');
			const seconds = String(date.getUTCSeconds()).padStart(2, '0');
			
			const formattedDate = `${day}/${month}/${year}`;
			const formattedTime = `${hours}:${minutes}:${seconds}`;
			
			return { date: formattedDate, time: formattedTime };
		} catch (e) {
			return null;
		}
	};
	
	const dateTimeInfo = formatAnalysisDateTime(analysisDate);
	return (
		<div className={`risk-score-card risk-score-card--${color}`}>
			<div className="risk-score-card__content">
				<h4 className="risk-score-card__title">{t('components.riskScoreCard.title')}</h4>
				
				<div className="risk-score-card__score-display">
					<div className="risk-score-card__score-number">{score}</div>
					<div className="risk-score-card__score-divider">/</div>
					<div className="risk-score-card__score-max">100</div>
				</div>

				<div className="risk-score-card__bar-container">
					<div 
						className={`risk-score-card__bar risk-score-card__bar--${color}`}
						style={{ width: `${score}%` }}
					/>
				</div>

				<div className="risk-score-card__info">
					<div className="risk-score-card__likelihood">
						<span className="risk-score-card__label">{t('components.riskScoreCard.riskLabel')}</span>
						<span className={`risk-score-card__value risk-score-card__value--${color}`}>
							{likelihood === 'bajo' && t('components.conclusionBox.lowRisk')}
							{likelihood === 'medio' && t('components.conclusionBox.mediumRisk')}
							{likelihood === 'alto' && t('components.conclusionBox.highRisk')}
						</span>
					</div>
					
					{dateTimeInfo && (
						<div className="risk-score-card__analysis-date">
							<Clock size={14} />
							<span className="risk-score-card__date-value">{dateTimeInfo.date} {dateTimeInfo.time} <span className="risk-score-card__utc-label">UTC</span></span>
						</div>
					)}
				</div>
			</div>

			<div className={`risk-score-card__icon risk-score-card__icon--${color}`}>
				{color === 'green' && '✓'}
				{color === 'yellow' && '⚠'}
				{color === 'red' && '✕'}
			</div>
		</div>
	);
};

export default RiskScoreCard;
