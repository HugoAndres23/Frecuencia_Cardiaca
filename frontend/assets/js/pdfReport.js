document.addEventListener('DOMContentLoaded', () => {
	const generatePdfBtn = document.getElementById('generatePdfBtn');
	const datasetSelect = document.getElementById('datasetSelect');
	const activitySelect = document.getElementById('activitySelect');
	const degreeSlider = document.getElementById('degree');
	const modelType = document.getElementById('modelType');

	if (!generatePdfBtn) {
		return;
	}

	generatePdfBtn.addEventListener('click', async () => {
		const dataset = datasetSelect?.value;
		const activity = activitySelect?.value;
		const degree = parseInt(degreeSlider?.value || '2', 10);

		if (!dataset) {
			alert('Selecciona un dataset antes de generar el reporte.');
			return;
		}

		if (!activity) {
			alert('Selecciona una actividad antes de generar el reporte.');
			return;
		}

		const algorithms = Array.from(modelType.options).map((option) => option.value);
		const payload = {
			filename: dataset,
			activity,
			degree,
			algorithms
		};

		try {
			generatePdfBtn.disabled = true;
			generatePdfBtn.textContent = 'Generando reporte...';

			const response = await fetch(`${API_BASE}/report/pdf`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(payload)
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}));
				throw new Error(errorData.detail || 'No se pudo generar el PDF');
			}

			const blob = await response.blob();
			const url = URL.createObjectURL(blob);
			const link = document.createElement('a');
			link.href = url;
			link.download = `reporte_${dataset.replace('.csv', '')}.pdf`;
			document.body.appendChild(link);
			link.click();
			link.remove();
			URL.revokeObjectURL(url);

			generatePdfBtn.textContent = 'PDF generado';
		} catch (error) {
			alert(`Error generando PDF: ${error.message}`);
			generatePdfBtn.textContent = 'Generar reporte PDF';
		} finally {
			generatePdfBtn.disabled = false;
			setTimeout(() => {
				generatePdfBtn.textContent = '📄 Generar reporte PDF';
			}, 1500);
		}
	});
});
