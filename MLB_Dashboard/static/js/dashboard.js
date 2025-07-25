// MLB_Dashboard/static/js/dashboard.js

// MLB_Dashboard/static/js/dashboard.js

// ── MLB Insights Dropdown Logic ───────────────────────────────
let insightsData = {};

function initInsights(insights) {
  insightsData = insights;
  const propSelect = document.getElementById('insights-select');
  const dateSelect = document.getElementById('insights-date-select');
  const display    = document.getElementById('insights-display');

  // Populate prop dropdown
  Object.keys(insightsData).forEach(pt => {
    propSelect.appendChild(new Option(pt, pt));
  });

  // When prop changes, build the date list
  propSelect.addEventListener('change', () => {
    const prop = propSelect.value;
    display.classList.add('d-none');
    display.textContent = '';

    // clear old dates
    dateSelect.innerHTML = '<option value="" selected>Select a date</option>';

    if (!prop || !insightsData[prop]?.length) {
      dateSelect.classList.add('d-none');
      return;
    }

    // sort insights by date ascending
    const sorted = insightsData[prop]
      .slice()
      .sort((a,b) => new Date(a.date) - new Date(b.date));

    // populate date dropdown
    sorted.forEach(ins => {
      const opt = new Option(ins.date, ins.date);
      dateSelect.appendChild(opt);
    });

    dateSelect.classList.remove('d-none');
  });

  // When date changes, show that exact insight
  dateSelect.addEventListener('change', () => {
    const prop = propSelect.value;
    const date = dateSelect.value;
    if (!prop || !date) {
      display.classList.add('d-none');
      return;
    }

    const insight = insightsData[prop].find(ins => ins.date === date);
    if (!insight) {
      display.classList.add('d-none');
      return;
    }

    const keyFactors = Array.isArray(insight.key_factors)
      ? insight.key_factors.join(', ')
      : insight.key_factors;

    display.textContent =
      `Date: ${insight.date}\n\n` +
      `Strongest Insight:\n${insight.strongest_insight}\n\n` +
      `Key Factors:\n${keyFactors}\n\n` +
      `Pattern Analysis:\n${insight.pattern_analysis}`;

    display.classList.remove('d-none');
  });
}

document.addEventListener('DOMContentLoaded', () => {
  showStatus("Loading dashboard data…");

  // 1) load insights
  fetch('/api/mlb-insights')
    .then(r => r.json())
    .then(res => {
      if (res.success) initInsights(res.insights);
      else console.error('Insights error:', res.error);
    })
    .catch(e => console.error('Fetch insights failed:', e));

  // 2) load main dashboard data
  fetch('/api/dashboard-data')
    .then(r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then(r => {
      if (r.success) {
        hideStatus();
        updateDashboard(r.data);
      } else {
        showStatus("Error: " + r.error, true);
        console.error('Dashboard data error:', r.error);
      }
    })
    .catch(e => {
      showStatus("Error: " + e.message, true);
      console.error('Fetch failed:', e);
    });
});

function updateDashboard(data) {
    if (data.latest_date) {
        const lu = document.getElementById('last-updated');
        if (lu) lu.textContent = `(${formatDate(data.latest_date)})`;
        const ln = document.getElementById('last-night-date');
        if (ln) ln.textContent = formatDate(data.latest_date);
    }

    updateOverallMetrics(data.overall);
    updatePropTypeTable(data.prop_types);
    updateRecentPredictions(data.recent_predictions);
    updateHistoricalTable(data.historical_data);
    updateXgbTable(data.xgb_comparison);
    updateAllTimePropAccuracyTable(data);
    try {
        createHistoricalChart(data.historical_data);
    } catch (err) {
        console.error('Chart error:', err);
    }
    try {
        createBankrollChart(data.bankroll_history);
    } catch (err) {
        console.error('Bankroll chart error:', err);
    }
    try {
        createBankrollChart(data.bankroll_history);
        updateBankrollHistoryTable(data.bankroll_history);
    } catch (err) {
        console.error('Bankroll chart/table error:', err);
    }



    updateBetslips(data.betslips);

    // ---- LOGGING FOR DEBUG ----
    if (data.xgb_by_prop) {
        console.log("xgb_by_prop keys:", Object.keys(data.xgb_by_prop));
        if (data.xgb_by_prop['Hits+Runs+RBIs']) {
            console.log("Hits+Runs+RBIs entry:", data.xgb_by_prop['Hits+Runs+RBIs']);
        } else {
            console.warn("No entry for Hits+Runs+RBIs in xgb_by_prop!");
        }
    } else {
        console.error("No xgb_by_prop in API response");
    }
    // --------------------------

    // NEW: Initialize XGB by-prop-type dropdown/table
    if (data.xgb_by_prop) {
        initXgbPropTypeSection(data.xgb_by_prop);

        // Also log what the dropdown options are
        const select = document.getElementById('xgb-prop-select');
        if (select) {
            let opts = [];
            for (let i = 0; i < select.options.length; i++) {
                opts.push({label: select.options[i].text, value: select.options[i].value});
            }
            console.log("Dropdown options:", opts);
        }

        // Auto-select first prop type on load (to show real values)
        if (select && select.options.length > 1) {
            select.selectedIndex = 1;
            console.log("Auto-selecting prop:", select.value);
            select.dispatchEvent(new Event('change'));
        }
    }

    // *** in updateDashboard(data) ***
    if (data.confidence_accuracy) {
        createConfidenceChart(data.confidence_accuracy);
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
  const tbody = document.getElementById('recent-predictions-table');
  tbody.innerHTML = '';

  const total   = predictions?.length || 0;
  let correct = 0;

  if (total > 0) {
    predictions.forEach(pred => {
      const predText  = pred.Prediction === 1 ? 'Over' : 'Under';
      const confNum   = parseFloat(pred.Confidence) || 0;
      const isCorrect = predText === pred.Actual_Result;
      if (isCorrect) correct++;

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${pred.Player}</td>
        <td>${pred['Prop Type']}</td>
        <td>${pred['Prop Value']}</td>
        <td>${pred['LLM_Prediction']}</td>
        <td>${pred['RF_Confidence']}</td>
        <td>${isCorrect ? '✓' : '✗'}</td>
      `;
      tbody.appendChild(tr);
    });
  } else {
    // still render a single row spanning all 6 columns
    const tr = document.createElement('tr');
    tr.innerHTML = '<td colspan="6" class="text-center">No recent predictions available</td>';
    tbody.appendChild(tr);
  }

  // always update footer summary
  document.getElementById('recent-predictions-summary')
          .textContent = `${correct} / ${total}`;
}

function updateHistoricalTable(rows) {
    const body = document.getElementById('historical-table-body');
    body.innerHTML = '';
    if (!rows || !rows.length) {
        body.innerHTML = '<tr><td colspan="5" class="text-center">No history available</td></tr>';
    } else {
        rows.forEach(r => {
            const total = r.total != null ? r.total : '-';
            const rf    = r.rf_accuracy    != null ? (r.rf_accuracy * 100).toFixed(1)+'%'    : '-';
            const llm   = r.llm_accuracy   != null ? (r.llm_accuracy * 100).toFixed(1)+'%'   : '-';
            const ag    = r.agreement_accuracy != null ? (r.agreement_accuracy * 100).toFixed(1)+'%' : '-';
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

function createHistoricalChart(data) {
    if (!data || !data.length) return;
    data.sort((a, b) => parseDateStr(a.date) - parseDateStr(b.date));

    const labels = data.map(d => formatShortDate(d.date));
    const rfAcc  = data.map(d => d.rf_accuracy    != null ? d.rf_accuracy * 100    : null);
    const llmAcc = data.map(d => d.llm_accuracy   != null ? d.llm_accuracy * 100   : null);
    const agAcc  = data.map(d => d.agreement_accuracy != null ? d.agreement_accuracy * 100 : null);

    if (window.historicalChart) window.historicalChart.destroy();

    const ctx = document.getElementById('historical-chart').getContext('2d');
    window.historicalChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            { label: 'RF Accuracy',        data: rfAcc },
            { label: 'LLM Accuracy',       data: llmAcc },
            { label: 'Agreement Accuracy', data: agAcc }
          ]
        },
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

function formatDate(str) {
    if (!str) return '';
    const d = new Date(str);
    return `${d.toLocaleString('default',{month:'short'})} ${d.getDate()}, ${d.getFullYear()}`;
}

function formatShortDate(dateStr) {
    const [, m, d] = dateStr.split('-');
    return `${Number(m)}/${Number(d)}`;
}

function parseDateStr(dateStr) {
    const [y, m, d] = dateStr.split('-').map(Number);
    return new Date(y, m - 1, d);
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

function updateBetslips(betslips) {
  const container = document.getElementById('betslips-card-container');
  container.innerHTML = '';

  if (!betslips || betslips.length === 0) {
    container.innerHTML = '<div class="text-center">No betslips generated yet.</div>';
    return;
  }

  betslips.forEach((slip, i) => {
    // ensure we have a legs array
    if (!slip.legs || !Array.isArray(slip.legs)) {
      console.warn(`Skipping invalid slip #${i+1}`, slip);
      return;
    }

    const slipCard = document.createElement('div');
    slipCard.className = 'betslip-card';

    // build legs HTML
    const legsHtml = slip.legs.map(leg => {
      const pick = leg.Pick || 'Over';
      const pickClass = pick === 'Over' ? 'pick-over' : 'pick-under';
      return `
        <div class="betslip-leg">
          <div class="player-name">${leg.Player}</div>
          <div class="prop">${leg["Prop Type"]} (${leg["Prop Value"]})</div>
          <div class="pick ${pickClass}">${pick}</div>
        </div>
      `;
    }).join('');

    slipCard.innerHTML = `
      <div class="betslip-header">Slip ${i + 1}</div>
      <div class="betslip-legs">${legsHtml}</div>
      <div class="betslip-meta">
        <span>Stake: $${(slip.stake||0).toFixed(2)}</span>
        <span>Multiplier: ${slip.payout_multiplier||'?'}×</span>
        <span>Win Prob: ${((slip.win_probability||0)*100).toFixed(1)}%</span>
        <span>Expected Return: $${(slip.expected_return||0).toFixed(2)}</span>
      </div>
    `;

    container.appendChild(slipCard);
  });
}

function updateXgbTable(rows) {
  const body = document.getElementById('xgb-table-body');
  body.innerHTML = '';
  if (!rows || !rows.length) {
    body.innerHTML = '<tr><td colspan="4" class="text-center">No XGBoost data available</td></tr>';
    return;
  }
  rows.slice().reverse().forEach(r => {
    const date = r.Date || r.date || '';
    const total = r.XGB_Total ?? r.total ?? '';
    const correct = r.XGB_Correct ?? r.xgb_correct ?? '';
    let acc = r.XGB_Accuracy ?? r.xgb_accuracy;
    if (acc !== undefined && acc !== null && acc !== '') {
      acc = acc > 1 ? acc.toFixed(1) + '%' : (acc * 100).toFixed(1) + '%';
    } else {
      acc = '-';
    }
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${date}</td>
      <td>${total}</td>
      <td>${correct}</td>
      <td>${acc}</td>
    `;
    body.appendChild(tr);
  });
}

function initXgbPropTypeSection(xgb_by_prop) {
  const select = document.getElementById('xgb-prop-select');
  const tbody = document.getElementById('xgb-prop-table-body');
  if (!select || !tbody || !xgb_by_prop) return;

  // Populate dropdown
  select.innerHTML = '<option value="">Select prop type</option>';
  Object.keys(xgb_by_prop).forEach(prop => {
    select.appendChild(new Option(prop.replace(/_/g,' '), prop));
  });

  // When changed, update table
  select.addEventListener('change', () => {
    const prop = select.value;
    tbody.innerHTML = '';
    if (!prop || !xgb_by_prop[prop]) return;

    // Sort most recent first
    let propRows = xgb_by_prop[prop].slice().reverse();
    if (!propRows.length) {
      tbody.innerHTML = '<tr><td colspan="4" class="text-center">No data for this prop type</td></tr>';
      return;
    }
    propRows.forEach(r => {
      const date = r.date || '';
      let count = r.count ?? '-';
      let correct = r.xgb_correct ?? '-';
      let acc = r.xgb_accuracy;

      if (acc !== undefined && acc !== null && acc !== '') {
        acc = acc > 1 ? acc.toFixed(1) + '%' : (acc * 100).toFixed(1) + '%';
      } else {
        acc = '-';
      }

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${date}</td>
        <td>${count}</td>
        <td>${correct}</td>
        <td>${acc}</td>
      `;
      tbody.appendChild(tr);
    });
  });
}

function createBankrollChart(history) {
    if (!history || !history.length) return;

    // Sort and prep data
    history.sort((a, b) => new Date(a.date) - new Date(b.date));
    const startRow = history.find(d => d.num_slips === 0);
    const firstBetIdx = history.findIndex(d => d.num_slips > 0);

    let labels = [], bankrolls = [];

    // Show initial bankroll point
    if (startRow && firstBetIdx >= 0) {
        labels.push(history[firstBetIdx].date + ' (start)');
        bankrolls.push(startRow.bankroll);
    }

    // Actual bet days
    history.forEach(d => {
        if (d.num_slips > 0) {
            labels.push(d.date);
            bankrolls.push(d.bankroll);
        }
    });

    // Chart.js destroy old chart
    if (window.bankrollChart) window.bankrollChart.destroy();

    const ctx = document.getElementById('bankroll-chart').getContext('2d');
    window.bankrollChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Bankroll',
                    data: bankrolls,
                    borderColor: '#1c7',
                    tension: 0.2,
                    fill: false,
                    pointRadius: 3,
                    pointBackgroundColor: '#1c7'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: 'Bankroll ($)' }, beginAtZero: false }
            },
            plugins: { legend: { position: 'top' } }
        }
    });

    // Modern summary bar below chart
    const summaryBar = document.getElementById('bankroll-summary-bar');
    const start = startRow ? startRow.bankroll : bankrolls[0] || 0;
    const end = bankrolls[bankrolls.length-1] || 0;
    const max = Math.max(...bankrolls, start);
    const min = Math.min(...bankrolls, start);
    const pnl = end - start;
    const pnlClass = pnl > 0 ? "pnl-pos" : (pnl < 0 ? "pnl-neg" : "");

}

function updateBankrollHistoryTable(history) {
    const tbody = document.getElementById('bankroll-history-table');
    if (!tbody || !history || !history.length) return;
    tbody.innerHTML = '';
    history.forEach(row => {
        if (row.num_slips === 0) return; // skip the start row
        const netVal = row.net_result === null ? '' :
            `<span style="color:${row.net_result >= 0 ? 'green':'red'};">
                ${row.net_result >= 0 ? '+' : ''}$${(row.net_result||0).toFixed(2)}
            </span>`;
        const returnedVal = row.total_returned === null ? '' : `$${(row.total_returned||0).toFixed(2)}`;
        const stakedVal = row.total_staked === null ? '' : `$${(row.total_staked||0).toFixed(2)}`;
        const slipsVal = row.num_slips || '';
        tbody.innerHTML += `
            <tr>
                <td>${row.date}</td>
                <td>${slipsVal}</td>
                <td>${stakedVal}</td>
                <td>${returnedVal}</td>
                <td>${netVal}</td>
            </tr>
        `;
    });
}

function updateAllTimePropAccuracyTable(data) {
  const tbody = document.getElementById('alltime-prop-accuracy-table');
  if (!tbody || !data.alltime_prop_accuracy) return;
  tbody.innerHTML = '';

  // Turn the dict into an array of [key, obj]
  const entries = Object.entries(data.alltime_prop_accuracy)
    .map(([key, obj]) => {
      // obj.accuracy might be a fraction (0.4789) or already a percent string ('47.9%')
      let raw = obj.accuracy;
      let numPct;
      if (typeof raw === 'string' && raw.trim().endsWith('%')) {
        numPct = parseFloat(raw);
      } else {
        numPct = parseFloat(raw) * 100;
      }
      return {
        prop_type: obj.prop_type,
        total: obj.total,
        pct: numPct
      };
    })
    // sort by descending pct
    .sort((a, b) => b.pct - a.pct);

  // build table rows
  entries.forEach(({prop_type, total, pct}) => {
    const formatted = pct.toFixed(1) + '%';
    // getAccuracyClass expects a number/string without '%'
    const cls = getAccuracyClass(pct);
    tbody.innerHTML += `
      <tr>
        <td>${prop_type}</td>
        <td>${total}</td>
        <td class="${cls}">${formatted}</td>
      </tr>
    `;
  });
}

function createConfidenceChart(bandArr) {
  // bandArr is now an array of {band, total, correct, accuracy}
  const labels = bandArr.map(d => d.band);
  const dataPts= bandArr.map(d => +(d.accuracy * 100).toFixed(1));

  const ctx = document.getElementById('confidence-chart').getContext('2d');
  if (window.confidenceChart) window.confidenceChart.destroy();

  window.confidenceChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'RF Accuracy (%)',
        data: dataPts,
        backgroundColor: '#0d6efd'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: { display: true, text: 'Accuracy (%)' }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: ctx => {
              const d = bandArr[ctx.dataIndex];
              return d.total
                ? `Accuracy: ${dataPts[ctx.dataIndex]}% (${d.correct}/${d.total})`
                : 'No predictions';
            }
          }
        }
      }
    }
  });
}