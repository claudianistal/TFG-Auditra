import React, { useState } from 'react';
import { ChevronDown, AlertCircle, CheckCircle } from 'lucide-react';

const IndicatorsGrid = ({ detectedFactors, missingFactors }) => {
	const [expandedId, setExpandedId] = useState(null);

	const toggleExpanded = (factorName) => {
		setExpandedId(expandedId === factorName ? null : factorName);
	};

	const IndicatorItem = ({ factor, isDetected }) => {
		const isExpanded = expandedId === factor.name;
		const riskColor = 
			factor.risk_level === 'high' ? 'high' :
			factor.risk_level === 'medium' ? 'medium' :
			'low';

		return (
			<div 
				className={`indicator-item indicator-item--${isDetected ? 'detected' : 'missing'}`}
				onClick={() => isDetected && toggleExpanded(factor.name)}
			>
				<div className="indicator-item__header">
					<div className="indicator-item__status">
						{isDetected ? (
							<AlertCircle size={20} className="indicator-item__icon--detected" />
						) : (
							<CheckCircle size={20} className="indicator-item__icon--missing" />
						)}
					</div>

					<div className="indicator-item__info">
						<div className="indicator-item__title">{factor.display_name}</div>
						<div className="indicator-item__meta">
							<span className={`indicator-item__risk indicator-item__risk--${riskColor}`}>
								{factor.risk_level.toUpperCase()}
							</span>
							<span className="indicator-item__weight">Peso: {factor.weight}</span>
							{isDetected && (
								<span className="indicator-item__confidence">
									Confianza: {Math.round(factor.confidence * 100)}%
								</span>
							)}
						</div>
					</div>

					{isDetected && (
						<div className="indicator-item__expand">
							<ChevronDown 
								size={20} 
								className={isExpanded ? 'expanded' : ''}
							/>
						</div>
					)}
				</div>

				{isDetected && isExpanded && (
					<div className="indicator-item__details">
						<p className="indicator-item__reasoning">
							<strong>Razón:</strong> {factor.reasoning}
						</p>
						{Object.keys(factor.details).length > 0 && (
							<div className="indicator-item__technical">
								<strong>Detalles técnicos:</strong>
								<ul>
									{Object.entries(factor.details).map(([key, value]) => (
										<li key={key}>
											<span className="indicator-item__detail-key">{key}:</span>
											<span className="indicator-item__detail-value">
												{typeof value === 'object' ? JSON.stringify(value) : String(value)}
											</span>
										</li>
									))}
								</ul>
							</div>
						)}
					</div>
				)}
			</div>
		);
	};

	return (
		<div className="indicators-grid">
			<div className="indicators-section">
				<h4 className="indicators-section__title indicators-section__title--detected">
					Indicadores Detectados ({detectedFactors.length})
				</h4>
				<div className="indicators-list">
					{detectedFactors.length > 0 ? (
						detectedFactors.map((factor) => (
							<IndicatorItem 
								key={factor.name} 
								factor={factor} 
								isDetected={true}
							/>
						))
					) : (
						<div className="indicators-empty">
							<CheckCircle size={24} />
							<p>No se detectaron indicadores sospechosos</p>
						</div>
					)}
				</div>
			</div>

			<div className="indicators-section">
				<h4 className="indicators-section__title indicators-section__title--missing">
					Indicadores No Detectados ({missingFactors.length})
				</h4>
				<div className="indicators-list">
					{missingFactors.length > 0 ? (
						missingFactors.map((factor) => (
							<IndicatorItem 
								key={factor.name} 
								factor={factor} 
								isDetected={false}
							/>
						))
					) : (
						<div className="indicators-empty">
							<AlertCircle size={24} />
							<p>Se detectaron todos los indicadores</p>
						</div>
					)}
				</div>
			</div>
		</div>
	);
};

export default IndicatorsGrid;
