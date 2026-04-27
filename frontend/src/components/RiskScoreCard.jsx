import React from 'react';
import { AlertCircle } from 'lucide-react';

const RiskScoreCard = ({ score, likelihood, color, percentile }) => {
	return (
		<div className={`risk-score-card risk-score-card--${color}`}>
			<div className="risk-score-card__content">
				<h4 className="risk-score-card__title">Puntuación General</h4>
				
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
						<span className="risk-score-card__label">Riesgo:</span>
						<span className={`risk-score-card__value risk-score-card__value--${color}`}>
							{likelihood === 'bajo' && 'Bajo'}
							{likelihood === 'medio' && 'Medio'}
							{likelihood === 'alto' && 'Alto'}
						</span>
					</div>
					<div className="risk-score-card__percentile">
						<span className="risk-score-card__label">Percentil:</span>
						<span className="risk-score-card__value">{percentile}</span>
					</div>
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
