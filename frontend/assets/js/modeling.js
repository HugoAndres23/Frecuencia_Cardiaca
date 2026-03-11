document.addEventListener('DOMContentLoaded', () => {
    const degreeSlider = document.getElementById('degree');
    const degreeValue = document.getElementById('degreeValue');
    const runModelBtn = document.getElementById('runModelBtn');
    const modelType = document.getElementById('modelType');

    // Update degree value display
    degreeSlider.addEventListener('input', (e) => {
        degreeValue.textContent = `Selected: ${e.target.value}`;
    });

    // Run simulation
    runModelBtn.addEventListener('click', async () => {
        const algorithm = modelType.value;
        const degree = degreeSlider.value;

        // Validation
        if (!algorithm) {
            alert('Por favor selecciona un algoritmo de modelado.');
            return;
        }

        // Prepare payload
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
            console.log('Modeling response:', response);
            if (response && response.results) {
                // Display results
                displayResults(response.results, response.metrics);
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

    function displayResults(results, metrics) {
        const canvas = document.getElementById('resultsChart');
        if (!canvas) return;

        // Destroy existing chart if it exists
        if (window.resultsChartInstance) {
            window.resultsChartInstance.destroy();
        }

        const ctx = canvas.getContext('2d');

        // Prepare data for Chart.js
        const labels = results.time_points || [];
        const realData = results.real_values || [];
        const predictedData = results.predicted_values || [];

        console.log('Labels:', labels);
        console.log('Real Data:', realData);
        console.log('Predicted Data:', predictedData);

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
});
