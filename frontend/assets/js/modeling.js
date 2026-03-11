document.addEventListener('DOMContentLoaded', () => {
    const degreeSlider = document.getElementById('degree');
    const degreeValue = document.getElementById('degreeValue');
    const runModelBtn = document.getElementById('runModelBtn');
    const modelType = document.getElementById('modelType');

    degreeSlider.addEventListener('input', (e) => {
        degreeValue.textContent = `Selected: ${e.target.value}`;
    });

    runModelBtn.addEventListener('click', async () => {
        const algorithm = modelType.value;
        const degree = degreeSlider.value;

        if (!algorithm) {
            alert('Por favor selecciona un algoritmo de modelado.');
            return;
        }

        const payload = {
            model_type: algorithm,
            degree: algorithm === 'polynomial' ? parseInt(degree) : 1,
            activity: 'reposo',
            filename: 'dataset.csv'
        };
        
        try {
            runModelBtn.disabled = true;
            runModelBtn.textContent = '⏳ Simulando...';

            const response = await post('/model/train', payload);
            if (response && response.results) {
                displayResults(response.results);
                displayMetrics(response);
                runModelBtn.textContent = '✓ Simulación Completada';
            } else {
                alert('Falló la simulación.');
                runModelBtn.textContent = '▶ Correr Simulación';
            }
        } catch (error) {
            console.error('Error corriendo la simulación:', error);
            alert('Error: ' + error.message);
            runModelBtn.textContent = '▶ Correr Simulación';
        } finally {
            runModelBtn.disabled = false;
        }
    });

    function displayResults(results) {
        const canvas = document.getElementById('resultsChart');
        if (!canvas) return;

        if (window.resultsChartInstance) {
            window.resultsChartInstance.destroy();
        }

        const ctx = canvas.getContext('2d');

        const labels = results.time_points || [];
        const realData = results.real_values || [];
        const predictedData = results.predicted_values || [];

        window.resultsChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Datos Reales',
                        data: realData,
                        borderColor: '#374151',
                        backgroundColor: 'rgba(55, 65, 81, 0.08)',
                        borderWidth: 2,
                        pointRadius: 3,
                        pointBackgroundColor: '#374151',
                        fill: true,
                        tension: 0.1
                    },
                    {
                        label: 'Regresión del Modelo',
                        data: predictedData,
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.08)',
                        borderWidth: 3,
                        pointRadius: 4,
                        pointBackgroundColor: '#2563eb',
                        fill: true,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Frecuencia Cardíaca (BPM)',
                            color: '#111827'
                        },
                        ticks: {
                            color: '#4b5563'
                        },
                        grid: {
                            color: '#e5e7eb'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#4b5563'
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    function displayMetrics(response) {
        const panel = document.getElementById('metricsPanel');
        const metrics = response.metrics;

        document.getElementById('res-time').textContent =
            response.training_time.toFixed(4) + ' s';

        document.getElementById('res-algorithm').textContent =
            response.degree
                ? `${response.algorithm} (grado ${response.degree})`
                : response.algorithm;

        document.getElementById('res-mae').textContent  = metrics.mae.toFixed(4);
        document.getElementById('res-mse').textContent  = metrics.mse.toFixed(4);
        document.getElementById('res-rmse').textContent = metrics.rmse.toFixed(4);
        document.getElementById('res-r2').textContent   = metrics.r2_score.toFixed(4);

        panel.style.display = 'flex';
    }
});
