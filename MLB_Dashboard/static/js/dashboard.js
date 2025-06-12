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
    // hidden span for backward compatibility
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
    createHistoricalChart(data.historical_data);
    updateHistoricalTable(data.historical_data);
}

function updateOverallMetrics(o) {
    if (!o) return;
    document.getElementById('rf-accuracy').textContent = `${(o.rf_accuracy*100).toFixed(1)}%`;
    document.getElementById('total-predictions').textContent = o.total;
    document.getElementById('llm-accuracy').textContent = `${(o.llm_accuracy*100).toFixed(1)}%`;
    document.getElementById('total-predictions-llm').textContent = o.total;
    document.getElementById('agreement-accuracy').textContent = `${(o.agreement_accuracy*100).toFixed(1)}%`;
    document.getElementById('agreement-count').textContent = o.agreement_count;
}

function updatePropTypeTable(pt) {
    const tb = document.getElementById('prop-types-table');
    tb.innerHTML = '';
    if (!pt || !Object.keys(pt).length) {
        tb.innerHTML = '<tr><td colspan="3" class="text-center">No prop type data available</td></tr>';
        return;
    }
    Object.entries(pt)
          .sort((a,b)=> b[1].count - a[1].count)
          .forEach(([name,data])=>{
            const rf  = (data.rf_accuracy*100).toFixed(1);
            const llm = (data.llm_accuracy*100).toFixed(1);
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>${name.replace(/_/g,' ')} (${data.count})</td>
              <td class="${getAccuracyClass(rf)}">${rf}%</td>
              <td class="${getAccuracyClass(llm)}">${llm}%</td>
            `;
            tb.appendChild(tr);
          });
}

function updateRecentPredictions(arr) {
    const tb = document.getElementById('recent-predictions-table');
    tb.innerHTML = '';
    if (!arr || !arr.length) {
        tb.innerHTML = '<tr><td colspan="6" class="text-center">No recent predictions available</td></tr>';
        return;
    }
    arr.forEach(pred => {
        const correct = pred.RF_Correct;
        const tr = document.createElement('tr');
        tr.classList.add(correct ? 'correct-prediction' : 'incorrect-prediction');
        tr.innerHTML = `
          <td>${pred.Player}</td>
          <td>${pred['Prop Type']}</td>
          <td>${pred['Prop Value']}</td>
          <td>${pred.RF_Prediction===1?'Over':'Under'}</td>
          <td>${(pred.RF_Confidence*100).toFixed(0)}%</td>
          <td>${correct?'✓':'✗'}</td>
        `;
        tb.appendChild(tr);
    });
}

function createHistoricalChart(data) {
    if (!data.length) return;
    data.sort((a,b)=> new Date(a.date)-new Date(b.date));
    const labels = data.map(d=>d.date);
    const props  = Object.keys(data[0]).filter(k=>k!=='date');
    const sets = [];
    props.forEach(p=>{
      sets.push({
        label: `${p} RF`,
        data: data.map(d=>d[p]?.rf*100||null),
        borderWidth:2, tension:0.1, fill:false
      });
      sets.push({
        label: `${p} LLM`,
        data: data.map(d=>d[p]?.llm*100||null),
        borderDash:[5,5], borderWidth:1, tension:0.1, fill:false
      });
    });
    const ctx = document.getElementById('historical-chart').getContext('2d');
    new Chart(ctx,{ type:'line', data:{labels, datasets:sets},
      options:{
        responsive:true, maintainAspectRatio:false,
        scales:{
          y:{beginAtZero:true,max:100,title:{display:true,text:'Accuracy (%)'}},
          x:{title:{display:true,text:'Date'}}
        },
        plugins:{legend:{position:'top'}}
      }
    });
}

function updateHistoricalTable(rows) {
    const body = document.getElementById('historical-table-body');
    body.innerHTML = '';
    if (!rows||!rows.length) {
      body.innerHTML = '<tr><td colspan="5" class="text-center">No history available</td></tr>';
      return;
    }
    rows.forEach(r=>{
      const total = r.total!=null?r.total:'-';
      const rf    = r.rf_accuracy!=null ? (r.rf_accuracy*100).toFixed(1)+'%' : '-';
      const llm   = r.llm_accuracy!=null? (r.llm_accuracy*100).toFixed(1)+'%' : '-';
      const ag    = r.agreement_accuracy!=null? (r.agreement_accuracy*100).toFixed(1)+'%' : '-';
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

function formatDate(str) {
  if(!str) return '';
  const d=new Date(str);
  return `${d.toLocaleString('default',{month:'short'})} ${d.getDate()}, ${d.getFullYear()}`;
}

function formatShortDate(str) {
  if(!str) return '';
  const d=new Date(str);
  return `${d.getMonth()+1}/${d.getDate()}`;
}

function getAccuracyClass(val) {
  const n=parseFloat(val);
  if(n>=60) return 'accuracy-high';
  if(n>=50) return 'accuracy-medium';
  return 'accuracy-low';
}

function showStatus(msg, err=false) {
  const el=document.getElementById('status-message');
  el.textContent=msg;
  el.style.display='block';
  el.style.backgroundColor = err? 'rgba(220,53,69,0.9)' : 'rgba(0,0,0,0.7)';
}

function hideStatus() {
  document.getElementById('status-message').style.display='none';
}
