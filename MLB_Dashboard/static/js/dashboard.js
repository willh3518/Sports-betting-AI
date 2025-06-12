// MLB_Dashboard/static/js/dashboard.js

document.addEventListener('DOMContentLoaded', function() {
    showStatus("Loading dashboard data...");

    fetch('/api/dashboard-data')
        .then(r => {
            if (!r.ok) throw new Error(`HTTP error! Status: ${r.status}`);
            return r.json();
        })
        .then(r => {
            if (r.success) {
                hideStatus();
                updateDashboard(r.data);
            } else {
                showStatus("Error: " + r.error, true);
                console.error('Error loading data:', r.error);
            }
        })
        .catch(e => {
            showStatus("Error: " + e.message, true);
            console.error('Fetch error:', e);
        });
});

function updateDashboard(data) {
    // backward‐compat hidden span
    if (data.latest_date) {
        const lu = document.getElementById('last-updated');
        if (lu) lu.textContent = `(${formatDate(data.latest_date)})`;
    }

    // show the date under "Last Night’s Performance"
    if (data.latest_date) {
        const ln = document.getElementById('last-night-date');
        if (ln) ln.textContent = formatDate(data.latest_date);
    }

    updateOverallMetrics(data.overall);
    updatePropTypeTable(data.prop_types);
    updateRecentPredictions(data.recent_predictions);
    updateHistoricalTable(data.historical_data);
    try {
        createHistoricalChart(data.historical_data);
    } catch (err) {
        console.error('Chart error:', err);
    }
}

function updateOverallMetrics(o) {
    if (!o) return;
    document.getElementById('rf-accuracy').textContent       = `${(o.rf_accuracy*100).toFixed(1)}%`;
    document.getElementById('total-predictions').textContent = o.total;
    document.getElementById('llm-accuracy').textContent      = `${(o.llm_accuracy*100).toFixed(1)}%`;
    document.getElementById('total-predictions-llm').textContent = o.total;
    document.getElementById('agreement-accuracy').textContent    = `${(o.agreement_accuracy*100).toFixed(1)}%`;
    document.getElementById('agreement-count').textContent       = o.agreement_count;
}

function updatePropTypeTable(pt) {
    const tb = document.getElementById('prop-types-table');
    tb.innerHTML = '';
    if (!pt || !Object.keys(pt).length) {
        tb.innerHTML = '<tr><td colspan="3" class="text-center">No prop type data available</td></tr>';
        return;
    }
    Object.entries(pt)
          .sort((a,b) => b[1].count - a[1].count)
          .forEach(([name,data]) => {
            const rfAcc  = (data.rf_accuracy*100).toFixed(1);
            const llmAcc = (data.llm_accuracy*100).toFixed(1);
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>${name.replace(/_/g,' ')} (${data.count})</td>
              <td class="${getAccuracyClass(rfAcc)}">${rfAcc}%</td>
              <td class="${getAccuracyClass(llmAcc)}">${llmAcc}%</td>
            `;
            tb.appendChild(tr);
          });
}

function updateRecentPredictions(predictions) {
    const tableBody = document.getElementById('recent-predictions-table');
    tableBody.innerHTML = '';

    if (!predictions || predictions.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center">No recent predictions available</td></tr>';
    } else {
        predictions.forEach(pred => {
            const predText = pred.Prediction === 1 ? 'Over' : 'Under';
            const confNum  = parseFloat(pred.Confidence) || 0;
            // result comes from your API: should be 'Over' or 'Under'
            const isCorrect = predText === pred.Result;
            const resultMark = isCorrect ? '✓' : '✗';

            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>${pred.Player}</td>
              <td>${pred['Prop Type']}</td>
              <td>${pred['Prop Value']}</td>
              <td>${predText}</td>
              <td>${confNum}%</td>
              <td>${resultMark}</td>
            `;
            tableBody.appendChild(tr);
        });

        // summary row: correct / total
        const total   = predictions.length;
        const correct = predictions.reduce((sum, pred) => {
            const predText = pred.Prediction === 1 ? 'Over' : 'Under';
            return sum + (predText === pred.Result ? 1 : 0);
        }, 0);

        const summaryEl = document.getElementById('recent-predictions-summary');
        if (summaryEl) {
            summaryEl.textContent = `${correct} / ${total}`;
        }
    }
}

function parseDateStr(dateStr) {
    const [y, m, d] = dateStr.split('-').map(Number);
    return new Date(y, m - 1, d);
}

function formatShortDate(dateStr) {
    const [, m, d] = dateStr.split('-');
    return `${Number(m)}/${Number(d)}`;
}

function createHistoricalChart(data) {
    if (!data.length) return;
    data.sort((a, b) => parseDateStr(a.date) - parseDateStr(b.date));

    const labels = data.map(d => formatShortDate(d.date));
    const rfAcc  = data.map(d => d.rf_accuracy    != null ? d.rf_accuracy * 100    : null);
    const llmAcc = data.map(d => d.llm_accuracy   != null ? d.llm_accuracy * 100   : null);
    const agAcc  = data.map(d => d.agreement_accuracy != null ? d.agreement_accuracy * 100 : null);

    if (window.historicalChart) window.historicalChart.destroy();

    const ctx = document.getElementById('historical-chart').getContext('2d');
    window.historicalChart = new Chart(ctx, {
        type: 'bar',
        data: { labels, datasets: [
            { label: 'RF Accuracy',        data: rfAcc },
            { label: 'LLM Accuracy',       data: llmAcc },
            { label: 'Agreement Accuracy', data: agAcc }
        ]},
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Accuracy (%)' }
                }
            },
            plugins: { legend: { position: 'top' } }
        }
    });
}

function updateHistoricalTable(rows) {
    const body = document.getElementById('historical-table-body');
    body.innerHTML = '';
    if (!rows || !rows.length) {
        body.innerHTML = '<tr><td colspan="5" class="text-center">No history available</td></tr>';
    } else {
        rows.forEach(r => {
            const total = r.total != null ? r.total : '-';
            const rf    = r.rf_accuracy != null    ? (r.rf_accuracy * 100).toFixed(1)+'%'    : '-';
            const llm   = r.llm_accuracy != null   ? (r.llm_accuracy * 100).toFixed(1)+'%'   : '-';
            const ag    = r.agreement_accuracy != null
                        ? (r.agreement_accuracy * 100).toFixed(1)+'%' : '-';
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>${formatShortDate(r.date)}</td>
              <td>${total}</td>
              <td>${rf}</td>
              <td>${llm}</td>
              <td>${ag}</td>
            `;
            body.appendChild(tr);
        });
    }
}

function formatDate(str) {
    if (!str) return '';
    const d = new Date(str);
    return `${d.toLocaleString('default',{month:'short'})} ${d.getDate()}, ${d.getFullYear()}`;
}

function getAccuracyClass(val) {
    const n = parseFloat(val);
    if (n >= 60) return 'accuracy-high';
    if (n >= 50) return 'accuracy-medium';
    return 'accuracy-low';
}

function showStatus(msg, err = false) {
    const el = document.getElementById('status-message');
    el.textContent = msg;
    el.style.display = 'block';
    el.style.backgroundColor = err
        ? 'rgba(220,53,69,0.9)'
        : 'rgba(0,0,0,0.7)';
}

function hideStatus() {
    document.getElementById('status-message').style.display = 'none';
}
