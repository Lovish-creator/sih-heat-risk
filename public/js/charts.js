/**
 * SIH26083 Multi-Chart Analytics Controller.
 * Powered by Chart.js — 100% Real Data, Zero Synthetic Hardcoded Fallbacks.
 * Ministry of Earth Sciences (MoES) / NCMRWF Prototype Decision Support.
 */

let chartRiskTrajectory = null;
let chartThermalIndices = null;
let chartWeatherDrivers = null;
let chartOverviewSparkline = null;

const CHART_DEFAULTS = {
  fontFamily: "'Inter', sans-serif",
  textColor: "#94a3b8",
  gridColor: "rgba(255, 255, 255, 0.06)",
  tooltipBg: "#0f172a",
  tooltipBorder: "#334155"
};

/**
 * 1. 5-Day Relative Heat-Health Risk Trajectory (0 - 100)
 */
function renderRiskTrajectoryChart(horizonList) {
  if (typeof Chart === "undefined") return;
  const ctx = document.getElementById("chartRiskTrajectory");
  if (!ctx || !horizonList || horizonList.length === 0) return;

  const labels = horizonList.map(d => `${d.horizon_label || ('Day ' + d.horizon_day)} (${(d.date || '').slice(5)})`);
  const riskScores = horizonList.map(d => (d.heat_risk_score !== undefined && d.heat_risk_score !== null) ? d.heat_risk_score : null);

  if (chartRiskTrajectory) {
    chartRiskTrajectory.destroy();
  }

  chartRiskTrajectory = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Relative Heat-Health Risk (0-100)",
          data: riskScores,
          borderColor: "#ef4444",
          backgroundColor: "rgba(239, 68, 68, 0.15)",
          borderWidth: 3,
          fill: true,
          tension: 0.35,
          spanGaps: true,
          pointRadius: 6,
          pointHoverRadius: 8,
          pointBackgroundColor: riskScores.map(score =>
            score !== null ? (score >= 75 ? "#ef4444" : score >= 50 ? "#f97316" : score >= 25 ? "#f59e0b" : "#10b981") : "#64748b"
          )
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { color: CHART_DEFAULTS.textColor, font: { family: CHART_DEFAULTS.fontFamily, size: 11 } },
          grid: { color: CHART_DEFAULTS.gridColor }
        },
        y: {
          min: 0,
          max: 100,
          ticks: { color: CHART_DEFAULTS.textColor, stepSize: 25 },
          grid: { color: CHART_DEFAULTS.gridColor },
          title: { display: true, text: "Relative Risk Score (0 - 100)", color: CHART_DEFAULTS.textColor }
        }
      },
      plugins: {
        legend: { labels: { color: "#f8fafc", font: { family: CHART_DEFAULTS.fontFamily, size: 11 } } },
        tooltip: {
          backgroundColor: CHART_DEFAULTS.tooltipBg,
          titleColor: "#38bdf8",
          bodyColor: "#f8fafc",
          borderColor: CHART_DEFAULTS.tooltipBorder,
          borderWidth: 1,
          callbacks: {
            label: (item) => `Relative Risk: ${item.raw !== null ? item.raw.toFixed(1) : 'N/A'}/100`
          }
        }
      }
    }
  });
}

/**
 * 2. Biometeorological Stress Index Comparison (Ta vs UTCI vs WBGT vs Heat Index)
 */
function renderThermalIndexComparisonChart(horizonList, weatherList) {
  if (typeof Chart === "undefined") return;
  const ctx = document.getElementById("chartThermalIndices");
  if (!ctx || !horizonList || horizonList.length === 0) return;

  const labels = horizonList.map(d => `${d.horizon_label || ('Day ' + d.horizon_day)} (${(d.date || '').slice(5)})`);
  const utciData = horizonList.map(d => (d.utci_c !== undefined && d.utci_c !== null) ? d.utci_c : null);
  const wbgtData = horizonList.map(d => (d.wbgt_c !== undefined && d.wbgt_c !== null) ? d.wbgt_c : null);
  const taData = horizonList.map(d => (d.temp_c !== undefined && d.temp_c !== null) ? d.temp_c : null);
  const hiData = horizonList.map(d => (d.heat_index_c !== undefined && d.heat_index_c !== null) ? d.heat_index_c : null);

  if (chartThermalIndices) {
    chartThermalIndices.destroy();
  }

  chartThermalIndices = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Dry-Bulb Air Temp Ta (°C)",
          data: taData,
          borderColor: "#94a3b8",
          borderDash: [5, 5],
          borderWidth: 2,
          spanGaps: true,
          tension: 0.3
        },
        {
          label: "Physiological UTCI (°C)",
          data: utciData,
          borderColor: "#f97316",
          borderWidth: 2.5,
          spanGaps: true,
          tension: 0.3
        },
        {
          label: "Occupational WBGT (°C)",
          data: wbgtData,
          borderColor: "#38bdf8",
          borderWidth: 2.5,
          spanGaps: true,
          tension: 0.3
        },
        {
          label: "NOAA Heat Index (°C)",
          data: hiData,
          borderColor: "#eab308",
          borderWidth: 2,
          spanGaps: true,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { color: CHART_DEFAULTS.textColor, font: { family: CHART_DEFAULTS.fontFamily, size: 11 } },
          grid: { color: CHART_DEFAULTS.gridColor }
        },
        y: {
          ticks: { color: CHART_DEFAULTS.textColor },
          grid: { color: CHART_DEFAULTS.gridColor },
          title: { display: true, text: "Temperature Equivalent (°C)", color: CHART_DEFAULTS.textColor }
        }
      },
      plugins: {
        legend: { labels: { color: "#f8fafc", font: { family: CHART_DEFAULTS.fontFamily, size: 11 } } },
        tooltip: {
          backgroundColor: CHART_DEFAULTS.tooltipBg,
          titleColor: "#38bdf8",
          bodyColor: "#f8fafc",
          borderColor: CHART_DEFAULTS.tooltipBorder,
          borderWidth: 1,
          callbacks: {
            label: (item) => `${item.dataset.label}: ${item.raw !== null ? item.raw.toFixed(1) + '°C' : 'N/A'}`
          }
        }
      }
    }
  });
}

/**
 * 3. Primary Meteorological Drivers (Temp/DewPoint vs Humidity/Solar)
 */
function renderWeatherDriversChart(weatherList) {
  if (typeof Chart === "undefined") return;
  const ctx = document.getElementById("chartWeatherDrivers");
  if (!ctx || !weatherList || weatherList.length === 0) return;

  const labels = weatherList.map(d => `${d.horizon_label || ('Day ' + d.horizon_day)} (${(d.date || '').slice(5)})`);
  const tempData = weatherList.map(d => (d.temp_c !== undefined && d.temp_c !== null) ? d.temp_c : null);
  const rhData = weatherList.map(d => (d.relative_humidity_pct !== undefined && d.relative_humidity_pct !== null) ? d.relative_humidity_pct : null);
  const solarData = weatherList.map(d => (d.solar_radiation_w_m2 !== undefined && d.solar_radiation_w_m2 !== null) ? Math.round(d.solar_radiation_w_m2 / 10) : null);

  if (chartWeatherDrivers) {
    chartWeatherDrivers.destroy();
  }

  chartWeatherDrivers = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          type: "line",
          label: "Dry-Bulb Temp (°C)",
          data: tempData,
          borderColor: "#f97316",
          borderWidth: 3,
          yAxisID: "yTemp",
          tension: 0.2,
          spanGaps: true
        },
        {
          type: "bar",
          label: "Relative Humidity (%)",
          data: rhData,
          backgroundColor: "rgba(56, 189, 248, 0.4)",
          borderColor: "#38bdf8",
          borderWidth: 1,
          yAxisID: "yPct"
        },
        {
          type: "line",
          label: "Solar Radiation (W/m² ÷ 10)",
          data: solarData,
          borderColor: "#facc15",
          borderWidth: 2,
          yAxisID: "yPct",
          tension: 0.2,
          spanGaps: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { color: CHART_DEFAULTS.textColor, font: { family: CHART_DEFAULTS.fontFamily, size: 11 } },
          grid: { color: CHART_DEFAULTS.gridColor }
        },
        yTemp: {
          type: "linear",
          position: "left",
          ticks: { color: "#f97316" },
          grid: { color: CHART_DEFAULTS.gridColor },
          title: { display: true, text: "Dry-Bulb Temp (°C)", color: "#f97316" }
        },
        yPct: {
          type: "linear",
          position: "right",
          ticks: { color: "#38bdf8" },
          grid: { drawOnChartArea: false },
          title: { display: true, text: "RH (%) / Solar (W/m² ÷ 10)", color: "#38bdf8" }
        }
      },
      plugins: {
        legend: { labels: { color: "#f8fafc", font: { family: CHART_DEFAULTS.fontFamily, size: 11 } } },
        tooltip: {
          backgroundColor: CHART_DEFAULTS.tooltipBg,
          titleColor: "#38bdf8",
          bodyColor: "#f8fafc",
          borderColor: CHART_DEFAULTS.tooltipBorder,
          borderWidth: 1
        }
      }
    }
  });
}

/**
 * 4. Overview Mini Trend Sparkline
 */
function renderOverviewMiniTrend(horizonList) {
  if (typeof Chart === "undefined") return;
  const ctx = document.getElementById("chartOverviewMiniTrend");
  if (!ctx || !horizonList || horizonList.length === 0) return;

  const labels = horizonList.map(d => d.horizon_label || ('D+' + d.horizon_day));
  const riskScores = horizonList.map(d => (d.heat_risk_score !== undefined && d.heat_risk_score !== null) ? d.heat_risk_score : null);

  if (chartOverviewSparkline) {
    chartOverviewSparkline.destroy();
  }

  chartOverviewSparkline = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          data: riskScores,
          borderColor: "#38bdf8",
          backgroundColor: "rgba(56, 189, 248, 0.15)",
          borderWidth: 2,
          fill: true,
          tension: 0.35,
          spanGaps: true,
          pointRadius: 3,
          pointBackgroundColor: "#38bdf8"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { display: false },
        y: { display: false, min: 0, max: 100 }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (item) => `Relative Risk: ${item.raw !== null ? item.raw.toFixed(1) : 'N/A'}/100`
          }
        }
      }
    }
  });
}

window.renderRiskTrajectoryChart = renderRiskTrajectoryChart;
window.renderThermalIndexComparisonChart = renderThermalIndexComparisonChart;
window.renderWeatherDriversChart = renderWeatherDriversChart;
window.renderOverviewMiniTrend = renderOverviewMiniTrend;
