import React from 'react';
import { AlertCircle, Loader } from 'lucide-react';
import './styles/MetadataTable.css';

const MetadataTable = ({ metadata, loading, error }) => {
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
				<p>Extrayendo metadatos...</p>
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
		if (!value && value !== 0) return 'N/A';

		// Handle arrays (convert to formatted string)
		if (Array.isArray(value)) {
			if (value.length === 0) return 'N/A';
			// For complex objects in arrays, show a summary
			if (typeof value[0] === 'object') {
				return `[${value.length} items]`;
			}
			return value.join(', ');
		}

		// Handle objects (convert to formatted string)
		if (typeof value === 'object') {
			try {
				return JSON.stringify(value);
			} catch {
				return '[Complex Object]';
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

	return (
		<div className="metadata-table-container">
			<table className="metadata-table">
				<thead>
					<tr>
						<th className="metadata-table__header-property">Propiedad</th>
						<th className="metadata-table__header-value">Valor</th>
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
