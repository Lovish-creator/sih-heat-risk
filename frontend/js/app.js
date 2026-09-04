/**
 * SIH26083 Main Dashboard Application Logic.
 * Supports Real Live Open Data APIs & User Location Detection.
 */

let currentCity = "ahmedabad";
let customCoordinates = null; // { lat, lon, name }
let currentHorizonDay = 1;
let currentPersona = "general_public";
let cachedForecastData = null;
let cachedAdvisories = null;
let isLiveMode = true;

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
  // 1. Detect My Location Button
  const detectBtn = document.getElementById("btnDetectLocation");
  if (detectBtn) {
    detectBtn.addEventListener("click", () => {
      detectUserLocation();
    });
  }

  // 2. City dropdown change
  const citySelect = document.getElementById("citySelect");
  if (citySelect) {
    citySelect.addEventListener("change", (e) => {
      customCoordinates = null;
      currentCity = e.target.value;
      const locBanner = document.getElementById("locationBannerText");
      if (locBanner) locBanner.textContent = `Pilot City: ${e.target.options[e.target.selectedIndex].text}`;
      refreshDashboardData();
    });
  }

  // 3. Search Box for Any City/Town
  const searchInput = document.getElementById("searchInput");
  const searchDropdown = document.getElementById("searchResultsDropdown");
  let debounceTimeout = null;

  if (searchInput && searchDropdown) {
    searchInput.addEventListener("input", (e) => {
      clearTimeout(debounceTimeout);
      const query = e.target.value.trim();
      if (query.length < 2) {
        searchDropdown.style.display = "none";
        return;
      }

      debounceTimeout = setTimeout(async () => {
        try {
          const res = await fetch(`/api/v1/geocode/search?q=${encodeURIComponent(query)}&limit=5`);
          const data = await res.json();
          const results = data.results || [];

          if (results.length === 0) {
            searchDropdown.innerHTML = `<div class="search-result-item" style="color: #64748b;">No locations found</div>`;
          } else {
            searchDropdown.innerHTML = results.map(r => `
              <div class="search-result-item" data-lat="${r.latitude}" data-lon="${r.longitude}" data-name="${r.name}" data-city="${r.city}">
                <strong>${r.city}</strong> <span style="font-size: 11px; color: #94a3b8;">${r.name}</span>
              </div>
            `).join("");

            searchDropdown.querySelectorAll(".search-result-item").forEach(item => {
              item.addEventListener("click", (evt) => {
                const lat = parseFloat(item.dataset.lat);
                const lon = parseFloat(item.dataset.lon);
                const name = item.dataset.name;
                const city = item.dataset.city;

                customCoordinates = { lat, lon, name, city };
                searchDropdown.style.display = "none";
                searchInput.value = city;

                const locBanner = document.getElementById("locationBannerText");
                if (locBanner) locBanner.innerHTML = `<strong>📍 Selected Location:</strong> ${city} <span style="font-size: 12px; color: #94a3b8;">(${lat.toFixed(4)}, ${lon.toFixed(4)})</span>`;

                setUserLocationMarker(lat, lon, city);
                refreshDashboardData();
              });
            });
          }
          searchDropdown.style.display = "block";
        } catch (err) {
          console.error("Geocoding search failed:", err);
        }
      }, 350);
    });

    document.addEventListener("click", (e) => {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.style.display = "none";
      }
    });
  }

  // 4. Horizon Day Tabs
  document.querySelectorAll(".horizon-tab").forEach(tab => {
    tab.addEventListener("click", (e) => {
      document.querySelectorAll(".horizon-tab").forEach(t => t.classList.remove("active"));
      e.target.classList.add("active");
      currentHorizonDay = parseInt(e.target.dataset.day);
      updateHorizonView();
    });
  });

  // 5. Persona Advisory Tabs
  document.querySelectorAll(".persona-tab").forEach(tab => {
    tab.addEventListener("click", (e) => {
      document.querySelectorAll(".persona-tab").forEach(t => t.classList.remove("active"));
      e.target.classList.add("active");
      currentPersona = e.target.dataset.persona;
      renderPersonaAdvisories();
    });
  });

  // 6. Modal Triggers
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

/**
 * Detect User Real Location via Browser Geolocation API with IP Geolocation fallback
 */
async function detectUserLocation() {
  const detectBtn = document.getElementById("btnDetectLocation");
  const locBanner = document.getElementById("locationBannerText");
  
  if (detectBtn) detectBtn.textContent = "⌛ Detecting...";

  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        await handleDetectedCoordinates(lat, lon, "GPS");
        if (detectBtn) detectBtn.innerHTML = "📍 Detect My Location";
      },
      async (err) => {
        console.warn("Browser GPS permission denied/unavailable. Falling back to IP Geolocation...", err);
        await fallbackIpGeolocation();
        if (detectBtn) detectBtn.innerHTML = "📍 Detect My Location";
      },
      { timeout: 7000, enableHighAccuracy: true }
    );
  } else {
    await fallbackIpGeolocation();
    if (detectBtn) detectBtn.innerHTML = "📍 Detect My Location";
  }
}

async function fallbackIpGeolocation() {
  const locBanner = document.getElementById("locationBannerText");
  try {
    const res = await fetch("https://ipapi.co/json/");
    if (!res.ok) throw new Error("IP Geolocation failed");
    const ipData = await res.json();
    const lat = parseFloat(ipData.latitude);
    const lon = parseFloat(ipData.longitude);
    const city = ipData.city || "Detected City";
    const region = ipData.region || "";
    await handleDetectedCoordinates(lat, lon, `IP Location (${city}, ${region})`);
  } catch (err) {
    console.error("IP fallback failed:", err);
    if (locBanner) locBanner.textContent = "Could not detect location. Please select a city or search above.";
  }
}

async function handleDetectedCoordinates(lat, lon, sourceLabel) {
  try {
    const res = await fetch(`/api/v1/geocode/reverse?lat=${lat}&lon=${lon}`);
    const geo = await res.json();
    const city = geo.city || "Your Location";
    const suburb = geo.suburb_or_ward ? `${geo.suburb_or_ward}, ` : "";
    const state = geo.state ? `, ${geo.state}` : "";

    customCoordinates = { lat, lon, name: geo.display_name, city: city };

    const locBanner = document.getElementById("locationBannerText");
    if (locBanner) {
      locBanner.innerHTML = `<strong>📍 Real Detected Location (${sourceLabel}):</strong> ${suburb}${city}${state} <span style="font-size: 12px; color: #94a3b8;">(${lat.toFixed(4)}, ${lon.toFixed(4)})</span>`;
    }

    setUserLocationMarker(lat, lon, `${suburb}${city}`);
    await refreshDashboardData();
  } catch (err) {
    console.error("Reverse geocode failed:", err);
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
    let riskUrl = `/api/v1/risk/forecast?days=5`;
    let advUrl = `/api/v1/advisory`;

    if (customCoordinates) {
      riskUrl += `&lat=${customCoordinates.lat}&lon=${customCoordinates.lon}`;
      advUrl += `&lat=${customCoordinates.lat}&lon=${customCoordinates.lon}`;
    } else {
      riskUrl += `&city=${currentCity}`;
      advUrl += `&city=${currentCity}`;
    }

    // 1. Fetch Live 5-Day Risk Forecast
    const riskRes = await fetch(riskUrl);
    const riskData = await riskRes.json();
    cachedForecastData = riskData.horizon;

    // 2. Fetch Live Advisories
    const advRes = await fetch(advUrl);
    cachedAdvisories = await advRes.json();

    // 3. Update View Components
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

  // Refresh GIS Map for this Horizon Day & Coordinates
  const lat = customCoordinates ? customCoordinates.lat : null;
  const lon = customCoordinates ? customCoordinates.lon : null;
  loadWardRiskLayer(currentCity, currentHorizonDay, lat, lon);
}

function renderPersonaAdvisories() {
  if (!cachedAdvisories || !cachedAdvisories.personas) return;

  const personaData = cachedAdvisories.personas[currentPersona];
  const listContainer = document.getElementById("advisoryList");
  const regimenNotice = document.getElementById("occupationalRegimenNotice");

  if (!personaData || !listContainer) return;

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
      <h3 style="color: #38bdf8; margin-bottom: 1rem;">Real-Time Open Data Sources & Scientific Models</h3>
      <div style="font-size: 13.5px; line-height: 1.6; color: #cbd5e1;">
        <p><strong>Open-Meteo Weather API:</strong> Live real-time surface meteorology (temperature, relative humidity, 10m wind speed, and shortwave/direct solar radiation flux in W/m²).</p>
        <p style="margin-top: 8px;"><strong>NASA POWER API:</strong> Global analysis-ready solar irradiance and surface meteorological reanalysis.</p>
        <p style="margin-top: 8px;"><strong>OpenStreetMap Nominatim:</strong> Global open reverse and forward geocoding with zero proprietary keys.</p>
        <p style="margin-top: 8px;"><strong>Universal Thermal Climate Index (UTCI):</strong> ${meth.models.utci.formula}. Evaluates physiological energy balance under temperature, humidity, 10m wind, and shortwave solar irradiance.</p>
        <p style="margin-top: 8px;"><strong>Wet Bulb Globe Temperature (WBGT):</strong> ${meth.models.wbgt.formula}. Aligned with NIOSH 2016 occupational criteria.</p>
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
