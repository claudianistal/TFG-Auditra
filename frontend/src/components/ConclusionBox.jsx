import React from 'react';
import { AlertTriangle, Info, CheckCircle } from 'lucide-react';

const ConclusionBox = ({ riskScore, likelihood, conclusion, recommendations }) => {
	const iconMap = {
		'bajo': <CheckCircle size={32} className="conclusion-box__icon--low" />,
		'medio': <AlertTriangle size={32} className="conclusion-box__icon--medium" />,
		'alto': <AlertTriangle size={32} className="conclusion-box__icon--high" />
	};

	const titleMap = {
		'bajo': 'Bajo Riesgo',
		'medio': 'Riesgo Medio',
		'alto': 'Alto Riesgo'
	};

	return (
		<div className={`conclusion-box conclusion-box--${likelihood}`}>
			<div className="conclusion-box__header">
				{iconMap[likelihood]}
				<h3 className="conclusion-box__title">
					{titleMap[likelihood]}
				</h3>
			</div>

			<p className="conclusion-box__conclusion">
				{conclusion}
			</p>

			{recommendations && recommendations.length > 0 && (
				<div className="conclusion-box__recommendations">
					<h4 className="conclusion-box__rec-title">
						<Info size={18} />
						Recomendaciones
					</h4>
					<ul className="conclusion-box__rec-list">
						{recommendations.map((rec, idx) => (
							<li key={idx} className="conclusion-box__rec-item">
								{rec}
							</li>
						))}
					</ul>
				</div>
			)}

			<div className="conclusion-box__footer">
				<div className="conclusion-box__score-info">
					<span className="conclusion-box__label">Puntuación Final:</span>
					<span className={`conclusion-box__score conclusion-box__score--${likelihood}`}>
						{riskScore}/100
					</span>
				</div>
			</div>
		</div>
	);
};

export default ConclusionBox;
