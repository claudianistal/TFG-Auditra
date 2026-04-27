import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { AlertCircle, Loader, Copy, Check } from 'lucide-react';
import './styles/MetadataTable.css';

const MetadataTable = ({ metadata, loading, error }) => {
	const { t } = useTranslation();
	const [copied, setCopied] = useState(false);

	// Format duration from seconds to HH:MM:SS
	const formatDuration = (seconds) => {
		if (!seconds || seconds === null) return 'N/A';
		const hours = Math.floor(seconds / 3600);
		const minutes = Math.floor((seconds % 3600) / 60);
		const secs = seconds % 60;
		
		if (hours > 0) {
			return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
		}
		return `${minutes}:${secs.toString().padStart(2, '0')}`;
	};

	// Format bitrate from bits/s to kbps
	const formatBitrate = (bitrate) => {
		if (!bitrate || bitrate === null) return 'N/A';
		return `${(bitrate / 1000).toFixed(0)} kbps`;
	};

	// Format sample rate
	const formatSampleRate = (sampleRate) => {
		if (!sampleRate || sampleRate === null) return 'N/A';
		return `${(sampleRate / 1000).toFixed(1)} kHz`;
	};

	// Display loading state
	if (loading) {
		return (
			<div className="metadata-loading">
				<Loader className="metadata-loading__spinner" size={40} />
				<p>{t('components.metadataTable.loading')}</p>
			</div>
		);
	}

	// Display error state
	if (error) {
		return (
			<div className="metadata-error">
				<AlertCircle size={32} />
				<p className="metadata-error__message">{error}</p>
			</div>
		);
	}

	// Display metadata table
	if (!metadata) {
		return null;
	}

	// Utility function to format label from key (snake_case to Title Case)
	const formatLabel = (key) => {
		return key
			.split('_')
			.map(word => word.charAt(0).toUpperCase() + word.slice(1))
			.join(' ');
	};

	// Utility function to format value based on key type
	const formatValue = (key, value) => {
		if (!value && value !== 0) return t('components.metadataTable.notAvailable');

		// Handle arrays (convert to formatted string)
		if (Array.isArray(value)) {
			if (value.length === 0) return t('components.metadataTable.notAvailable');
			// For complex objects in arrays, show a summary
			if (typeof value[0] === 'object') {
				return `[${value.length} items]`;
			}
			return value.join(', ');
		}

		// Handle booleans (React will crash if we try to render true/false directly)
		if (typeof value === 'boolean') {
			return value ? t('components.metadataTable.yes') : t('components.metadataTable.no');
		}

		// Handle objects (convert to formatted string)
		if (typeof value === 'object') {
			try {
				return JSON.stringify(value);
			} catch {
				return t('components.metadataTable.complexObject');
			}
		}

		switch (key) {
			case 'duration':
				return formatDuration(value);
			case 'bitrate':
				return formatBitrate(value);
			case 'sample_rate':
				return formatSampleRate(value);
			default:
				return value;
		}
	};

	// Get all metadata entries dynamically
	const metadataEntries = Object.entries(metadata)
		.filter(([, value]) => value !== undefined && value !== null && value !== '') // Exclude undefined, null, empty values
		.filter(([key]) => {
			// Exclude highly complex nested structures that don't provide user-friendly info
			const complexKeys = ['container_layout', 'atom_structure_error'];
			return !complexKeys.includes(key);
		})
		.map(([key, value]) => ({
			key,
			label: formatLabel(key),
			value,
		}));

	// Handle copy to clipboard
	const handleCopyMetadata = async () => {
		const textToCopy = metadataEntries
			.map(entry => `${entry.label}: ${formatValue(entry.key, entry.value)}`)
			.join('\n');
		
		try {
			await navigator.clipboard.writeText(textToCopy);
			setCopied(true);
			setTimeout(() => setCopied(false), 2000);
		} catch (err) {
			console.error('Failed to copy metadata:', err);
		}
	};

	return (
		<div className="metadata-table-container">
			<div className="metadata-table-header">
				<h3>{t('components.metadataTable.title')}</h3>
				<button 
					className="metadata-copy-btn"
					onClick={handleCopyMetadata}
					title={copied ? t('components.metadataTable.copied') : t('components.metadataTable.copyTooltip')}
				>
					{copied ? (
						<>
							<Check size={18} />
							<span>{t('components.metadataTable.copied')}</span>
						</>
					) : (
						<>
							<Copy size={18} />
							<span>{t('components.metadataTable.copy')}</span>
						</>
					)}
				</button>
			</div>
			<table className="metadata-table">
				<thead>
					<tr>
						<th className="metadata-table__header-property">{t('components.metadataTable.property')}</th>
						<th className="metadata-table__header-value">{t('components.metadataTable.value')}</th>
					</tr>
				</thead>
				<tbody>
					{metadataEntries.map((entry) => (
						<tr key={entry.key} className="metadata-table__row">
							<td className="metadata-table__property">{entry.label}</td>
							<td className="metadata-table__value">
								{formatValue(entry.key, entry.value)}
							</td>
						</tr>
					))}
				</tbody>
			</table>
		</div>
	);
};

export default MetadataTable;
