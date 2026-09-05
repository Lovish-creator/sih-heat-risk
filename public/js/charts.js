/**
 * SIH26083 Live Multi-Horizon Chart.js Controller.
 * Supports Hourly (Next 24 Hours) and Daily (7-Day) Real-Time Forecasts.
 */

let forecastChart = null;

function renderForecastChart(chartData, isHourly = false) {
  const ctx = document.getElementById('forecastChart');
  if (!ctx) return;

  let labels = [];
  let tempData = [];
  let utciData = [];
  let wbgtData = [];
  let riskScoreData = [];

  if (isHourly) {
    labels = chartData.map(d => `${d.hour_label} (${d.date.slice(5)})`);
    tempData = chartData.map(d => d.temp_c);
    utciData = chartData.map(d => d.utci_c);
    wbgtData = chartData.map(d => d.wbgt_c);
    riskScoreData = chartData.map(d => d.hazard_score);
  } else {
    labels = chartData.map(d => `${d.horizon_label} (${d.date.slice(5)})`);
    tempData = chartData.map(d => d.temp_c);
    utciData = chartData.map(d => d.utci_c);
    wbgtData = chartData.map(d => d.wbgt_c);
    riskScoreData = chartData.map(d => d.heat_risk_score);
  }

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
          label: isHourly ? 'Hazard Index (0-100)' : 'Heat-Health Risk (0-100)',
          data: riskScoreData,
          borderColor: '#ef4444',
          backgroundColor: 'transparent',
          borderWidth: 3,
          pointRadius: 4,
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
          title: { display: true, text: 'Relative Index Score (0-100)', color: '#ef4444' },
          ticks: { color: '#ef4444' },
          grid: { drawOnChartArea: false }
        }
      }
    }
  });
}
