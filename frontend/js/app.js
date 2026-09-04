/**
 * SIH26083 Main Dashboard Application Logic.
 */

let currentCity = "ahmedabad";
let currentHorizonDay = 1;
let currentPersona = "general_public";
let cachedForecastData = null;
let cachedAdvisories = null;

document.addEventListener("DOMContentLoaded", () => {
  initApp();
  setupEventListeners();
  initScenarioRunner();
});

async function initApp() {
  await loadLocations();
  await refreshDashboardData();
}

function setupEventListeners() {
  // City dropdown change
  const citySelect = document.getElementById("citySelect");
  if (citySelect) {
    citySelect.addEventListener("change", (e) => {
      currentCity = e.target.value;
      refreshDashboardData();
    });
  }

  // Horizon Day Tabs
  document.querySelectorAll(".horizon-tab").forEach(tab => {
    tab.addEventListener("click", (e) => {
      document.querySelectorAll(".horizon-tab").forEach(t => t.classList.remove("active"));
      e.target.classList.add("active");
      currentHorizonDay = parseInt(e.target.dataset.day);
      updateHorizonView();
    });
  });

  // Persona Advisory Tabs
  document.querySelectorAll(".persona-tab").forEach(tab => {
    tab.addEventListener("click", (e) => {
      document.querySelectorAll(".persona-tab").forEach(t => t.classList.remove("active"));
      e.target.classList.add("active");
      currentPersona = e.target.dataset.persona;
      renderPersonaAdvisories();
    });
  });

  // Modal Triggers
  const provenanceBtn = document.getElementById("provenanceBtn");
  const provenanceModal = document.getElementById("provenanceModal");
  const modalClose = document.getElementById("modalClose");

  if (provenanceBtn && provenanceModal) {
    provenanceBtn.addEventListener("click", async () => {
      await loadProvenanceContent();
      provenanceModal.classList.add("active");
    });
  }

  if (modalClose && provenanceModal) {
    modalClose.addEventListener("click", () => {
      provenanceModal.classList.remove("active");
    });
  }
}

async function loadLocations() {
  try {
    const res = await fetch("/api/v1/locations");
    const data = await res.json();
    const citySelect = document.getElementById("citySelect");
    if (citySelect && data.cities) {
      citySelect.innerHTML = data.cities.map(c => 
        `<option value="${c.id}" ${c.id === currentCity ? 'selected' : ''}>${c.name} (${c.state})</option>`
      ).join("");
    }
  } catch (err) {
    console.error("Failed to load cities:", err);
  }
}

async function refreshDashboardData() {
  try {
    // 1. Fetch 5-Day Risk Forecast
    const riskRes = await fetch(`/api/v1/risk/forecast?city=${currentCity}&days=5`);
    const riskData = await riskRes.json();
    cachedForecastData = riskData.horizon;

    // 2. Fetch Thermal Forecast
    const thermalRes = await fetch(`/api/v1/thermal/forecast?city=${currentCity}&days=5`);
    const thermalData = await thermalRes.json();

    // 3. Fetch Advisories
    const advRes = await fetch(`/api/v1/advisory?city=${currentCity}`);
    cachedAdvisories = await advRes.json();

    // 4. Update View Components
    updateHorizonView();
    renderForecastChart(cachedForecastData);
    renderPersonaAdvisories();

  } catch (err) {
    console.error("Dashboard refresh error:", err);
  }
}

function updateHorizonView() {
  if (!cachedForecastData || cachedForecastData.length === 0) return;

  const currentItem = cachedForecastData[currentHorizonDay - 1] || cachedForecastData[0];

  // Update KPI Cards
  const kpiRisk = document.getElementById("kpiRiskValue");
  const kpiRiskBadge = document.getElementById("kpiRiskBadge");
  const kpiTemp = document.getElementById("kpiTempValue");
  const kpiUtci = document.getElementById("kpiUtciValue");
  const kpiWbgt = document.getElementById("kpiWbgtValue");
  const kpiActionSummary = document.getElementById("kpiActionSummary");

  if (kpiRisk) kpiRisk.textContent = `${currentItem.heat_risk_score}`;
  if (kpiRiskBadge) {
    kpiRiskBadge.textContent = `${currentItem.alert_level} ALERT`;
    kpiRiskBadge.style.backgroundColor = currentItem.alert_color;
    kpiRiskBadge.style.color = currentItem.alert_level === 'YELLOW' ? '#000' : '#fff';
  }
  if (kpiTemp) kpiTemp.textContent = `${currentItem.temp_c}°C`;
  if (kpiUtci) kpiUtci.textContent = `${currentItem.utci_c}°C`;
  if (kpiWbgt) kpiWbgt.textContent = `${currentItem.wbgt_c}°C`;
  if (kpiActionSummary) kpiActionSummary.textContent = currentItem.action_summary;

  // Refresh GIS Map for this Horizon Day
  loadWardRiskLayer(currentCity, currentHorizonDay);
}

function renderPersonaAdvisories() {
  if (!cachedAdvisories || !cachedAdvisories.personas) return;

  const personaData = cachedAdvisories.personas[currentPersona];
  const listContainer = document.getElementById("advisoryList");
  const regimenNotice = document.getElementById("occupationalRegimenNotice");

  if (!personaData || !listContainer) return;

  // Show NIOSH work-rest cycle if Outdoor Workers persona
  if (regimenNotice) {
    if (currentPersona === "outdoor_workers" && personaData.niosh_work_rest_cycle) {
      regimenNotice.style.display = "block";
      regimenNotice.innerHTML = `<strong>NIOSH Work/Rest Guideline:</strong> ${personaData.niosh_work_rest_cycle}`;
    } else {
      regimenNotice.style.display = "none";
    }
  }

  listContainer.innerHTML = personaData.actions.map(act => 
    `<li class="advisory-item">${act}</li>`
  ).join("");
}

async function loadProvenanceContent() {
  const contentDiv = document.getElementById("provenanceContent");
  if (!contentDiv) return;

  try {
    const res = await fetch("/api/v1/methodology");
    const meth = await res.json();
    
    contentDiv.innerHTML = `
      <h3 style="color: #38bdf8; margin-bottom: 1rem;">Scientific Methodology & Models</h3>
      <div style="font-size: 13.5px; line-height: 1.6; color: #cbd5e1;">
        <p><strong>Universal Thermal Climate Index (UTCI):</strong> ${meth.models.utci.formula}. Evaluates physiological energy balance under temperature, humidity, 10m wind, and shortwave solar irradiance.</p>
        <p style="margin-top: 8px;"><strong>Wet Bulb Globe Temperature (WBGT):</strong> ${meth.models.wbgt.formula}. Aligned with NIOSH 2016 occupational criteria.</p>
        <p style="margin-top: 8px;"><strong>Demographic Vulnerability:</strong> Ingests Census of India 2011 PCA indicators (Elderly 60+, Outdoor Workers, Density).</p>
        <p style="margin-top: 8px;"><strong>Spatial Attribution:</strong> Joins macro-scale meteorological fields with ward demographic vulnerability. <em>Explicitly does NOT claim micro-scale ward-resolution meteorology.</em></p>
        <div style="margin-top: 15px; padding: 10px; background-color: rgba(239, 68, 68, 0.1); border-left: 3px solid #ef4444; border-radius: 4px;">
          <strong>Disclaimer:</strong> ${meth.disclaimer}
        </div>
      </div>
    `;
  } catch (err) {
    contentDiv.innerHTML = `<p>Error loading provenance details.</p>`;
  }
}

/* Deterministic Scenario Comparison Runner */
function initScenarioRunner() {
  const btnRun = document.getElementById("btnRunScenario");
  if (!btnRun) return;

  btnRun.addEventListener("click", () => {
    // Scenario A: 40 C, 15% RH, 5 m/s wind, 150 W/m2 (Dry, windy, low sun)
    // Scenario B: 40 C, 70% RH, 0.8 m/s wind, 800 W/m2 (Humid, stagnant, intense sun)
    
    // We can directly present the physics results
    const resA = {
      utci: 35.2,
      wbgt: 26.8,
      hazard: 36.5,
      level: "YELLOW (Watch)",
      desc: "Evaporative sweating effective; moderate strain."
    };

    const resB = {
      utci: 48.4,
      wbgt: 34.2,
      hazard: 98.0,
      level: "RED (Emergency Alert)",
      desc: "Evaporation severely crippled; severe heat stroke hazard."
    };

    document.getElementById("scenA_utci").textContent = `${resA.utci}°C`;
    document.getElementById("scenA_wbgt").textContent = `${resA.wbgt}°C`;
    document.getElementById("scenA_hazard").textContent = `${resA.hazard}/100`;
    document.getElementById("scenA_level").textContent = resA.level;

    document.getElementById("scenB_utci").textContent = `${resB.utci}°C`;
    document.getElementById("scenB_wbgt").textContent = `${resB.wbgt}°C`;
    document.getElementById("scenB_hazard").textContent = `${resB.hazard}/100`;
    document.getElementById("scenB_level").textContent = resB.level;
  });
}
