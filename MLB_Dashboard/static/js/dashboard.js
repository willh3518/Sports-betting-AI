// MLB_Dashboard/static/js/dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    // Show status message
    showStatus("Loading dashboard data...");

    // Load all dashboard data at once
    fetch('/api/dashboard-data')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Hide status message
                hideStatus();

                // Update the dashboard with the data
                updateDashboard(data.data);
            } else {
                showStatus("Error: " + data.error, true);
                console.error('Error loading dashboard data:', data.error);
            }
        })
        .catch(error => {
            showStatus("Error: " + error.message, true);
            console.error('Error fetching dashboard data:', error);
        });
});

function updateDashboard(data) {
    // Update last updated date
    if (data.latest_date) {
        document.getElementById('last-updated').textContent = `(${formatDate(data.latest_date)})`;
    }

    // Update overall metrics
    updateOverallMetrics(data.overall);

    // Update prop type table
    updatePropTypeTable(data.prop_types);

    // Update recent predictions table
    updateRecentPredictions(data.recent_predictions);

    // Create historical performance chart
    createHistoricalChart(data.historical_data);
}

function updateOverallMetrics(overall) {
    if (!overall) return;

    // Update RF accuracy
    const rfAccuracy = overall.rf_accuracy * 100;
    document.getElementById('rf-accuracy').textContent = `${rfAccuracy.toFixed(1)}%`;
    document.getElementById('total-predictions').textContent = overall.total;

    // Update LLM accuracy
    const llmAccuracy = overall.llm_accuracy * 100;
    document.getElementById('llm-accuracy').textContent = `${llmAccuracy.toFixed(1)}%`;
    document.getElementById('total-predictions-llm').textContent = overall.total;

    // Update agreement accuracy
    const agreementAccuracy = overall.agreement_accuracy * 100;
    document.getElementById('agreement-accuracy').textContent = `${agreementAccuracy.toFixed(1)}%`;
    document.getElementById('agreement-count').textContent = overall.agreement_count;
}

function updatePropTypeTable(propTypes) {
    const tableBody = document.getElementById('prop-types-table');
    tableBody.innerHTML = '';

    if (!propTypes || Object.keys(propTypes).length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="3" class="text-center">No prop type data available</td>';
        tableBody.appendChild(row);
        return;
    }

    // Sort prop types by count (descending)
    const sortedPropTypes = Object.entries(propTypes)
        .sort((a, b) => b[1].count - a[1].count);

    sortedPropTypes.forEach(([propType, data]) => {
        const row = document.createElement('tr');

        // Format prop type name for display
        const displayName = propType.replace(/_/g, ' ');

        // Format accuracies with color coding
        const rfAccuracy = data.rf_accuracy * 100;
        const llmAccuracy = data.llm_accuracy * 100;

        row.innerHTML = `
            <td>${displayName} (${data.count})</td>
            <td class="${getAccuracyClass(rfAccuracy)}">${rfAccuracy.toFixed(1)}%</td>
            <td class="${getAccuracyClass(llmAccuracy)}">${llmAccuracy.toFixed(1)}%</td>
        `;

        tableBody.appendChild(row);
    });
}

function getAccuracyClass(accuracy) {
    if (accuracy >= 60) return 'accuracy-high';
    if (accuracy >= 50) return 'accuracy-medium';
    return 'accuracy-low';
}

function updateRecentPredictions(predictions) {
    const tableBody = document.getElementById('recent-predictions-table');
    tableBody.innerHTML = '';

    if (!predictions || predictions.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="6" class="text-center">No recent predictions available</td>';
        tableBody.appendChild(row);
        return;
    }

    predictions.forEach(pred => {
        const row = document.createElement('tr');

        // Determine if prediction was correct
        const predictionText = pred.RF_Prediction === 1 ? 'Over' : 'Under';
        const isCorrect = pred.RF_Correct;

        // Add class based on correctness
        if (isCorrect) {
            row.classList.add('correct-prediction');
        } else {
            row.classList.add('incorrect-prediction');
        }

        row.innerHTML = `
            <td>${pred.Player}</td>
            <td>${pred['Prop Type']}</td>
            <td>${pred['Prop Value']}</td>
            <td>${predictionText}</td>
            <td>${(pred.RF_Confidence * 100).toFixed(0)}%</td>
            <td>${isCorrect ? '✓' : '✗'}</td>
        `;

        tableBody.appendChild(row);
    });
}

function createHistoricalChart(data) {
    if (!data || data.length === 0) return;

    const ctx = document.getElementById('historical-chart').getContext('2d');

    // Sort data by date
    data.sort((a, b) => new Date(a.date) - new Date(b.date));

    // Prepare data for chart
    const dates = data.map(item => formatShortDate(item.date));
    const rfAccuracies = data.map(item => item.rf_accuracy * 100);
    const llmAccuracies = data.map(item => item.llm_accuracy * 100);
    const agreementAccuracies = data.map(item => item.agreement_accuracy * 100);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'RF Accuracy',
                    data: rfAccuracies,
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: false
                },
                {
                    label: 'LLM Accuracy',
                    data: llmAccuracies,
                    backgroundColor: 'rgba(253, 126, 20, 0.1)',
                    borderColor: 'rgba(253, 126, 20, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: false
                },
                {
                    label: 'Agreement Accuracy',
                    data: agreementAccuracies,
                    backgroundColor: 'rgba(25, 135, 84, 0.1)',
                    borderColor: 'rgba(25, 135, 84, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Accuracy (%)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const datasetLabel = context.dataset.label;
                            const value = context.parsed.y.toFixed(1);
                            return `${datasetLabel}: ${value}%`;
                        }
                    }
                }
            }
        }
    });
}

function formatDate(dateStr) {
    // Convert YYYY-MM-DD to more readable format
    if (!dateStr) return '';

    const date = new Date(dateStr);
    const month = date.toLocaleString('default', { month: 'short' });
    const day = date.getDate();
    const year = date.getFullYear();

    return `${month} ${day}, ${year}`;
}

function formatShortDate(dateStr) {
    // Convert YYYY-MM-DD to MM/DD format
    if (!dateStr) return '';

    const date = new Date(dateStr);
    const month = date.getMonth() + 1;
    const day = date.getDate();

    return `${month}/${day}`;
}

function showStatus(message, isError = false) {
    const statusEl = document.getElementById('status-message');
    statusEl.textContent = message;
    statusEl.style.display = 'block';

    if (isError) {
        statusEl.style.backgroundColor = 'rgba(220, 53, 69, 0.9)';
    } else {
        statusEl.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    }
}

function hideStatus() {
    const statusEl = document.getElementById('status-message');
    statusEl.style.display = 'none';
}