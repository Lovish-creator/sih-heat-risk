/**
 * SIH26083 5-Day Horizon Chart.js Controller.
 */

let forecastChart = null;

function renderForecastChart(riskHorizonData) {
  const ctx = document.getElementById('forecastChart');
  if (!ctx) return;

  const labels = riskHorizonData.map(d => `${d.horizon_label} (${d.date.slice(5)})`);
  const tempData = riskHorizonData.map(d => d.temp_c);
  const utciData = riskHorizonData.map(d => d.utci_c);
  const wbgtData = riskHorizonData.map(d => d.wbgt_c);
  const riskScoreData = riskHorizonData.map(d => d.heat_risk_score);

  if (forecastChart) {
    forecastChart.destroy();
  }

  forecastChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Air Temp Ta (°C)',
          data: tempData,
          borderColor: '#94a3b8',
          backgroundColor: 'transparent',
          borderDash: [5, 5],
          borderWidth: 2,
          tension: 0.3,
          yAxisID: 'yTemp'
        },
        {
          label: 'Physiological UTCI (°C)',
          data: utciData,
          borderColor: '#f97316',
          backgroundColor: 'rgba(249, 115, 22, 0.1)',
          fill: true,
          borderWidth: 3,
          tension: 0.3,
          yAxisID: 'yTemp'
        },
        {
          label: 'Occupational WBGT (°C)',
          data: wbgtData,
          borderColor: '#38bdf8',
          backgroundColor: 'transparent',
          borderWidth: 2,
          tension: 0.3,
          yAxisID: 'yTemp'
        },
        {
          label: 'Heat-Health Risk (0-100)',
          data: riskScoreData,
          borderColor: '#ef4444',
          backgroundColor: 'transparent',
          borderWidth: 3,
          pointRadius: 6,
          pointBackgroundColor: '#ef4444',
          tension: 0.3,
          yAxisID: 'yRisk'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          labels: {
            color: '#f8fafc',
            font: { family: 'Inter', size: 11 }
          }
        },
        tooltip: {
          backgroundColor: '#1e293b',
          titleColor: '#38bdf8',
          bodyColor: '#f8fafc',
          borderColor: '#475569',
          borderWidth: 1
        }
      },
      scales: {
        x: {
          ticks: { color: '#94a3b8', font: { family: 'Inter', size: 10 } },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        yTemp: {
          type: 'linear',
          position: 'left',
          title: { display: true, text: 'Temperature & Biometeorology (°C)', color: '#94a3b8' },
          ticks: { color: '#94a3b8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        yRisk: {
          type: 'linear',
          position: 'right',
          min: 0,
          max: 100,
          title: { display: true, text: 'Relative Risk Score (0-100)', color: '#ef4444' },
          ticks: { color: '#ef4444' },
          grid: { drawOnChartArea: false }
        }
      }
    }
  });
}
