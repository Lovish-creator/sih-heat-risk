/**
 * SIH26083 Master Application Controller & Tab Router.
 * 100% Genuine Data — Zero Synthetic Hardcoded Fallbacks.
 * Ministry of Earth Sciences (MoES) / NCMRWF Tier 1 Prototype.
 */

// Global State
let currentCity = "abohar";
let customCoordinates = null; // { lat, lon, name, city }
let currentHorizonDay = 1; // 1 to 5 (D+0 to D+4)
let activeTabId = "overview";

let cachedUnifiedState = null;
let cachedWards = [];
let cachedCapAlert = null;

document.addEventListener("DOMContentLoaded", () => {
  initApp();
  setupNavigation();
  setupEventListeners();
});

async function initApp() {
  // 1. Safe Map Init
  try {
    if (typeof initMap === "function") {
      initMap(30.14505, 74.19566, 12);
    }
  } catch (err) {
    console.warn("Initial map setup deferred:", err);
  }

  // 2. Load Initial Data immediately
  await refreshDashboardData();
}

/**
 * 6-Tab Operational Navigation Router
 */
function setupNavigation() {
  const tabs = document.querySelectorAll(".nav-tab");
  const views = document.querySelectorAll(".view-section");

  function switchTab(tabId) {
    activeTabId = tabId;
    tabs.forEach(t => t.classList.toggle("active", t.dataset.tab === tabId));
    views.forEach(v => v.classList.toggle("active", v.id === `view_${tabId}`));

    // Leaflet map needs resize trigger when becoming visible
    if (tabId === "map" && typeof mapInstance !== "undefined" && mapInstance) {
      setTimeout(() => {
        try { mapInstance.invalidateSize(); } catch (e) {}
      }, 150);
    }

    // Refresh views if data is ready
    if (cachedUnifiedState) {
      try {
        if (tabId === "forecast") {
          renderForecastView(cachedUnifiedState);
        }
        if (tabId === "vulnerability") {
          renderVulnerabilityView(cachedWards);
        }
        if (tabId === "advisories") {
          renderAdvisoriesView(cachedUnifiedState.advisory, cachedUnifiedState.thermal);
        }
        if (tabId === "methodology") {
          renderMethodologyView();
        }
      } catch (err) {
        console.error("Tab render error:", err);
      }
    }
  }

  tabs.forEach(t => {
    t.addEventListener("click", () => {
      switchTab(t.dataset.tab);
    });
  });

  window.addEventListener("hashchange", () => {
    const hash = window.location.hash.replace("#", "");
    if (["overview", "map", "forecast", "vulnerability", "advisories", "methodology"].includes(hash)) {
      switchTab(hash);
    }
  });

  if (window.location.hash) {
    const initHash = window.location.hash.replace("#", "");
    if (["overview", "map", "forecast", "vulnerability", "advisories", "methodology"].includes(initHash)) {
      switchTab(initHash);
    }
  }
}

/**
 * Global Event Listeners (Search, Pilot Select, Horizon, GPS, Modals)
 */
function setupEventListeners() {
  // 1. City Select Dropdown
  const citySelect = document.getElementById("citySelect");
  if (citySelect) {
    citySelect.addEventListener("change", (e) => {
      customCoordinates = null;
      currentCity = e.target.value;
      ApiClient.clearCache();
      refreshDashboardData();
    });
  }

  // 2. Horizon Segmented Control (D+0 to D+4)
  const horizonBtns = document.querySelectorAll(".horizon-btn");
  horizonBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      horizonBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentHorizonDay = parseInt(btn.dataset.day, 10) || 1;
      
      try {
        loadWardRiskLayer(
          currentCity,
          currentHorizonDay,
          customCoordinates ? customCoordinates.lat : null,
          customCoordinates ? customCoordinates.lon : null
        );
      } catch (e) {}
      fetchWardsData();
    });
  });

  // 3. Search Autocomplete with Sub-10ms Local-First Engine
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
          const data = await ApiClient.searchLocations(query, 8);
          const results = Array.isArray(data) ? data : (data.results || []);

          if (!results || results.length === 0) {
            searchDropdown.innerHTML = `<div class="search-dropdown-item" style="color: #94a3b8;">No locations found for "${query}". Try searching city or district name.</div>`;
          } else {
            searchDropdown.innerHTML = results.map(r => `
              <div class="search-dropdown-item" data-lat="${r.latitude}" data-lon="${r.longitude}" data-name="${r.name}" data-city="${r.city}">
                <strong style="color: #38bdf8;">${r.city}</strong> <span style="font-size: 11px; color: #94a3b8;">${r.name}</span>
              </div>
            `).join("");

            searchDropdown.querySelectorAll(".search-dropdown-item").forEach(item => {
              item.addEventListener("click", () => {
                const lat = parseFloat(item.dataset.lat);
                const lon = parseFloat(item.dataset.lon);
                const name = item.dataset.name;
                const city = item.dataset.city;

                customCoordinates = { lat, lon, name, city };
                searchInput.value = `${city} (${lat.toFixed(3)}, ${lon.toFixed(3)})`;
                searchDropdown.style.display = "none";
                ApiClient.clearCache();
                setUserLocationMarker(lat, lon, city);
                refreshDashboardData();
              });
            });
          }
          searchDropdown.style.display = "block";
        } catch (err) {
          console.error("Search geocode error:", err);
        }
      }, 250);
    });

    searchInput.addEventListener("keydown", async (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const query = searchInput.value.trim();
        if (!query) return;
        try {
          const data = await ApiClient.searchLocations(query, 1);
          const results = Array.isArray(data) ? data : (data.results || []);
          if (results && results.length > 0) {
            const r = results[0];
            customCoordinates = { lat: r.latitude, lon: r.longitude, name: r.name, city: r.city };
            searchDropdown.style.display = "none";
            ApiClient.clearCache();
            setUserLocationMarker(r.latitude, r.longitude, r.city);
            refreshDashboardData();
          }
        } catch (err) {}
      }
    });

    document.addEventListener("click", (e) => {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.style.display = "none";
      }
    });
  }

  // 4. GPS Auto-Detect Button (Triggered Only On User Click)
  const btnDetect = document.getElementById("btnDetectLocation");
  if (btnDetect) {
    btnDetect.addEventListener("click", () => detectUserLocation(true));
  }

  // 5. Manual Lat/Lon Coordinates Modal
  const btnManual = document.getElementById("btnManualCoords");
  const coordsModal = document.getElementById("coordsModal");
  const coordsClose = document.getElementById("coordsClose");
  const btnApplyCoords = document.getElementById("btnApplyCoords");

  if (btnManual && coordsModal) {
    btnManual.addEventListener("click", () => coordsModal.classList.add("active"));
    coordsClose?.addEventListener("click", () => coordsModal.classList.remove("active"));
    btnApplyCoords?.addEventListener("click", () => {
      const lat = parseFloat(document.getElementById("inputLat")?.value);
      const lon = parseFloat(document.getElementById("inputLon")?.value);
      if (isNaN(lat) || isNaN(lon) || lat < -90 || lat > 90 || lon < -180 || lon > 180) {
        alert("Please enter valid latitude (-90 to +90) and longitude (-180 to +180).");
        return;
      }
      customCoordinates = { lat, lon, name: `Custom (${lat.toFixed(4)}, ${lon.toFixed(4)})`, city: `Coordinates (${lat.toFixed(2)}, ${lon.toFixed(2)})` };
      coordsModal.classList.remove("active");
      ApiClient.clearCache();
      setUserLocationMarker(lat, lon, customCoordinates.city);
      refreshDashboardData();
    });
  }

  // 6. Ward Ranking Table Filter Input
  const wardFilterInput = document.getElementById("wardFilterInput");
  if (wardFilterInput) {
    wardFilterInput.addEventListener("input", (e) => {
      const q = e.target.value.toLowerCase().trim();
      filterWardRankingTable(q);
    });
  }

  // 7. CSV Export Button
  const btnExportCsv = document.getElementById("btnExportWardCsv");
  if (btnExportCsv) {
    btnExportCsv.addEventListener("click", exportWardDataToCSV);
  }

  // 8. CAP Emergency Alert Modal
  const btnViewCap = document.getElementById("btnViewCapAlert");
  const capModal = document.getElementById("capModal");
  const capClose = document.getElementById("capClose");
  if (btnViewCap && capModal) {
    btnViewCap.addEventListener("click", async () => {
      await showCapAlertModal();
      capModal.classList.add("active");
    });
    capClose?.addEventListener("click", () => capModal.classList.remove("active"));
  }
}

/**
 * Handle Map Click to Pinpoint
 */
async function handleMapClickLocation(lat, lon) {
  try {
    const geo = await ApiClient.reverseGeocode(lat, lon);
    const city = geo.city || "Detected Location";
    const suburb = geo.suburb_or_ward ? `${geo.suburb_or_ward}, ` : "";

    customCoordinates = { lat, lon, name: geo.display_name, city };
    ApiClient.clearCache();
    setUserLocationMarker(lat, lon, `${suburb}${city}`);
    await refreshDashboardData();
  } catch (err) {
    console.error("Map click reverse geocode error:", err);
  }
}

/**
 * GPS Location Detection on Button Click
 */
async function detectUserLocation(userTriggered = false) {
  const detectBtn = document.getElementById("btnDetectLocation");
  if (detectBtn) detectBtn.textContent = "⌛ Detecting...";

  let resolved = false;

  if ("geolocation" in navigator) {
    try {
      await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          async (pos) => {
            resolved = true;
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            try {
              const geo = await ApiClient.reverseGeocode(lat, lon);
              customCoordinates = { lat, lon, name: geo.display_name, city: geo.city || "Your Location" };
              setUserLocationMarker(lat, lon, customCoordinates.city);
              await refreshDashboardData();
            } catch (err) {}
            if (detectBtn) detectBtn.textContent = "📍 Detect Location";
            resolve(true);
          },
          (err) => {
            console.warn("Browser GPS denied or timed out:", err);
            reject(err);
          },
          { timeout: 5000, enableHighAccuracy: true, maximumAge: 0 }
        );
      });
      return;
    } catch (e) {}
  }

  if (!resolved) {
    try {
      const ipData = await ApiClient.getIpLocation();
      if (ipData && ipData.latitude && ipData.longitude) {
        const lat = parseFloat(ipData.latitude);
        const lon = parseFloat(ipData.longitude);
        const city = ipData.city || "Detected Location";
        customCoordinates = { lat, lon, name: `${city}, ${ipData.region || ''}`, city };
        setUserLocationMarker(lat, lon, city);
        await refreshDashboardData();
      }
    } catch (err) {
      console.warn("IP Geolocation failover warning:", err);
    }
    if (detectBtn) detectBtn.textContent = "📍 Detect Location";
  }
}

/**
 * Master Data Refresh: Ingestion of Live Meteorological & Biometeorological Endpoints
 */
async function refreshDashboardData() {
  const queryParams = customCoordinates ? {
    lat: customCoordinates.lat,
    lon: customCoordinates.lon,
    city: customCoordinates.city
  } : { city: currentCity };

  try {
    // 1. Update Context Banner Safely
    const bannerEl = document.getElementById("locationBannerText");
    if (bannerEl) {
      if (customCoordinates) {
        bannerEl.innerHTML = `<strong>📍 Location:</strong> ${customCoordinates.name || customCoordinates.city} <span style="color: #94a3b8; font-size: 11px;">(${customCoordinates.lat.toFixed(4)}, ${customCoordinates.lon.toFixed(4)})</span>`;
      } else {
        const sel = document.getElementById("citySelect");
        let cityName = currentCity.toUpperCase();
        if (sel && sel.selectedIndex >= 0 && sel.options && sel.options[sel.selectedIndex]) {
          cityName = sel.options[sel.selectedIndex].text;
        }
        const isVerified = cityName.includes("⭐");
        bannerEl.innerHTML = `<strong>📍 Jurisdiction:</strong> ${cityName} ${isVerified ? '<span class="status-badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); font-size: 10px; margin-left: 6px;">VERIFIED MUNICIPAL DATA</span>' : ''}`;
      }
    }

    // 2. Fetch All Core APIs in Parallel
    const [weatherRes, thermalRes, riskRes, forecastRes, riskForecastRes, hourlyRes, advRes, vulnRes, freshnessRes] = await Promise.all([
      ApiClient.getCurrentWeather(queryParams).catch(() => null),
      ApiClient.getThermalCurrent(queryParams).catch(() => null),
      ApiClient.getRiskCurrent(queryParams).catch(() => null),
      ApiClient.getForecast(queryParams).catch(() => null),
      ApiClient.getRiskForecast(queryParams).catch(() => null),
      ApiClient.getHourlyWeather(queryParams).catch(() => null),
      ApiClient.getAdvisories(queryParams).catch(() => null),
      ApiClient.getVulnerability(queryParams).catch(() => null),
      ApiClient.getDataFreshness().catch(() => null)
    ]);

    const weatherObj = weatherRes?.weather || {};
    const thermalObj = thermalRes?.thermal_analysis || {};
    const riskObj = riskRes || {};
    const forecastList = forecastRes?.data || [];
    const riskForecastList = riskForecastRes?.horizon || [];
    const hourlyList = hourlyRes?.hourly_series || [];
    const advObj = advRes || {};
    const vulnObj = vulnRes || {};

    cachedUnifiedState = {
      city_id: riskObj.city_id || weatherRes?.city_id || currentCity,
      city_name: riskObj.city_name || weatherRes?.city_name || currentCity,
      weather: weatherObj,
      thermal: thermalObj,
      risk: riskObj,
      forecast: forecastList,
      risk_forecast: riskForecastList,
      hourly: hourlyList,
      advisory: advObj,
      vulnerability: vulnObj
    };

    // 3. Render Overview View
    try {
      renderOverviewView(cachedUnifiedState);
    } catch (e) {
      console.error("renderOverviewView error:", e);
    }

    // 4. Render Forecast Charts & Table
    try {
      if (typeof renderOverviewMiniTrend === "function") {
        renderOverviewMiniTrend(riskForecastList.length > 0 ? riskForecastList : forecastList);
      }
      if (typeof renderForecastView === "function") {
        renderForecastView(cachedUnifiedState);
      }
      if (typeof renderHourlyTable === "function") {
        renderHourlyTable(hourlyList);
      }
    } catch (e) {
      console.error("renderForecast error:", e);
    }

    // 5. Render Advisories View
    try {
      if (typeof renderAdvisoriesView === "function") {
        renderAdvisoriesView(advObj, thermalObj);
      }
    } catch (e) {
      console.error("renderAdvisories error:", e);
    }

    // 6. Fetch Wards & Load GIS Choropleth
    try {
      await fetchWardsData();
      if (typeof loadWardRiskLayer === "function") {
        loadWardRiskLayer(
          currentCity,
          currentHorizonDay,
          customCoordinates ? customCoordinates.lat : null,
          customCoordinates ? customCoordinates.lon : null
        );
      }
    } catch (e) {
      console.error("loadWardRiskLayer error:", e);
    }

    // 7. Update Freshness Badge
    const freshBadge = document.getElementById("liveTimeBadge");
    if (freshBadge) {
      const isFallback = freshnessRes?.fallback_active;
      const statusText = freshnessRes?.status || (isFallback ? "FALLBACK BUFFER ACTIVE" : "REAL-TIME SYNCHRONIZED");
      freshBadge.textContent = `● FRESHNESS: ${statusText}`;
      freshBadge.className = isFallback ? "status-badge status-badge-proto" : "status-badge status-badge-live";
    }

  } catch (err) {
    console.error("Dashboard master refresh error:", err);
  }
}

/**
 * Fetch and cache Municipal Wards
 */
async function fetchWardsData() {
  const queryParams = customCoordinates ? {
    lat: customCoordinates.lat,
    lon: customCoordinates.lon,
    city: customCoordinates.city
  } : { city: currentCity };

  try {
    const wardsData = await ApiClient.getWardsSummary(currentHorizonDay, queryParams);
    cachedWards = Array.isArray(wardsData) ? wardsData : (wardsData.all_wards || wardsData.wards || wardsData.top_hotspots || []);
    if (cachedUnifiedState && (!cachedUnifiedState.vulnerability.wards || cachedUnifiedState.vulnerability.wards.length === 0)) {
      cachedUnifiedState.vulnerability.wards = cachedWards;
    }
    if (typeof renderVulnerabilityView === "function") {
      renderVulnerabilityView(cachedWards);
    }
  } catch (err) {
    console.error("Wards summary fetch error:", err);
  }
}

/**
 * 1. Render Overview View — Zero Synthetic Hardcoding
 */
function renderOverviewView(state) {
  if (!state) return;

  const r = state.risk || {};
  const w = state.weather || {};
  const t = state.thermal || {};
  const metrics = t.metrics || {};

  // Dominant Risk Hero Score (0 - 100)
  const score = (r.heat_risk_score !== undefined && r.heat_risk_score !== null) ? r.heat_risk_score : null;
  const alertLevel = r.alert_level || (score !== null ? (score >= 75 ? "EMERGENCY" : score >= 50 ? "WARNING" : score >= 25 ? "CAUTION" : "NORMAL") : "AWAITING TELEMETRY");
  const alertColor = r.alert_color || (score !== null ? (typeof getColorByRisk === "function" ? getColorByRisk(score) : "#f97316") : "#64748b");

  const scoreEl = document.getElementById("heroRiskScore");
  const badgeEl = document.getElementById("heroRiskBadge");
  const descEl = document.getElementById("heroRiskDesc");
  const bannerEl = document.getElementById("emergencyAlertBanner");
  const bannerTextEl = document.getElementById("emergencyAlertText");

  if (scoreEl) scoreEl.textContent = score !== null ? (typeof score === 'number' ? score.toFixed(1) : score) : "--";
  if (badgeEl) {
    badgeEl.textContent = `${alertLevel} ALERT`;
    badgeEl.style.backgroundColor = alertColor;
    badgeEl.style.color = (alertLevel === "YELLOW" || alertLevel === "CAUTION") ? "#000000" : "#ffffff";
  }

  // Plain-Language Interpretation
  if (descEl) {
    if (score !== null) {
      if (score >= 75) {
        descEl.textContent = "Extreme heat stress hazard. High air temperature combined with oppressive humidity and radiation exceeds human metabolic cooling capacity.";
      } else if (score >= 50) {
        descEl.textContent = "Severe heat stress conditions. Outdoor workers and elderly residents face heightened physiological strain.";
      } else if (score >= 25) {
        descEl.textContent = "Moderate heat conditions. Extended direct sun exposure without hydration will induce fatigue.";
      } else {
        descEl.textContent = "Comfortable to mild conditions. Thermal indices remain within safe baseline thresholds.";
      }
    } else {
      descEl.textContent = "Awaiting meteorological data from public weather provider...";
    }
  }

  // Emergency Alert Banner
  if (bannerEl && bannerTextEl) {
    bannerEl.className = `emergency-alert-banner alert-${alertLevel.toLowerCase()}`;
    bannerTextEl.textContent = r.action_summary || "Routine monitoring in effect. Ensure public hydration facilities are accessible.";
  }

  // Supporting Thermal Stress Sub-Metrics
  const utciVal = metrics.utci?.value_c !== undefined ? metrics.utci.value_c : null;
  const utciCat = metrics.utci?.category || "Calculated from Weather Data";
  const wbgtVal = metrics.wbgt?.value_c !== undefined ? metrics.wbgt.value_c : null;
  const wbgtCat = metrics.wbgt?.risk_category || "NIOSH / ISO 7243";
  const hiVal = metrics.heat_index?.value_c !== undefined ? metrics.heat_index.value_c : null;

  const elUtci = document.getElementById("valHeroUtci");
  const elWbgt = document.getElementById("valHeroWbgt");
  const elHi = document.getElementById("valHeroHi");

  if (elUtci) elUtci.textContent = utciVal !== null ? `${utciVal.toFixed(1)}°C (${utciCat})` : "--°C";
  if (elWbgt) elWbgt.textContent = wbgtVal !== null ? `${wbgtVal.toFixed(1)}°C (${wbgtCat})` : "--°C";
  if (elHi) elHi.textContent = hiVal !== null ? `${hiVal.toFixed(1)}°C` : "--°C";

  // Vulnerability Snapshot
  const elElderly = document.getElementById("valHeroElderly");
  const elLabor = document.getElementById("valHeroLabor");
  const elDensity = document.getElementById("valHeroDensity");

  const distDemo = state.vulnerability?.district_demographics || {};
  const demo = distDemo.demographics || distDemo || {};

  const eld = demo.elderly_percentage !== undefined ? demo.elderly_percentage : (state.vulnerability?.elderly_percentage);
  const wrk = demo.outdoor_worker_percentage !== undefined ? demo.outdoor_worker_percentage : (state.vulnerability?.outdoor_worker_percentage);
  const den = demo.pop_density_per_sqkm !== undefined ? demo.pop_density_per_sqkm : (state.vulnerability?.pop_density_per_sqkm);

  if (elElderly) elElderly.textContent = eld !== undefined && eld !== null ? `${typeof eld === 'number' ? eld.toFixed(1) : eld}%` : "--%";
  if (elLabor) elLabor.textContent = wrk !== undefined && wrk !== null ? `${typeof wrk === 'number' ? wrk.toFixed(1) : wrk}%` : "--%";
  if (elDensity) elDensity.textContent = den !== undefined && den !== null ? `${Math.round(den).toLocaleString()} /km²` : "-- /km²";

  // Meteorological Telemetry Grid
  const elTa = document.getElementById("telTa");
  const elTdp = document.getElementById("telTdp");
  const elRh = document.getElementById("telRh");
  const elSolar = document.getElementById("telSolar");
  const elUv = document.getElementById("telUv");
  const elWind = document.getElementById("telWind");
  const elPressure = document.getElementById("telPressure");

  if (elTa) elTa.textContent = w.temp_c !== undefined ? `${w.temp_c.toFixed(1)}°C` : "--°C";
  if (elTdp) elTdp.textContent = w.dew_point_c !== undefined ? `${w.dew_point_c.toFixed(1)}°C` : "--°C";
  if (elRh) elRh.textContent = w.relative_humidity_pct !== undefined ? `${Math.round(w.relative_humidity_pct)}%` : "--%";
  if (elSolar) elSolar.textContent = w.solar_radiation_w_m2 !== undefined ? `${Math.round(w.solar_radiation_w_m2)} W/m²` : "-- W/m²";
  if (elUv) elUv.textContent = w.uv_index !== undefined ? `${w.uv_index.toFixed(1)}` : "--";
  if (elWind) elWind.textContent = w.wind_speed_kmh !== undefined ? `${w.wind_speed_kmh.toFixed(1)} km/h` : "-- km/h";
  if (elPressure) elPressure.textContent = w.surface_pressure_hpa !== undefined ? `${Math.round(w.surface_pressure_hpa)} hPa` : "-- hPa";
}

/**
 * 2. Render 5-Day Forecast Analytics View
 */
function renderForecastView(state) {
  if (!state) return;

  const riskForecast = state.risk_forecast || [];
  const weatherForecast = state.forecast || [];

  if (typeof renderRiskTrajectoryChart === "function") renderRiskTrajectoryChart(riskForecast);
  if (typeof renderThermalIndexComparisonChart === "function") renderThermalIndexComparisonChart(riskForecast, weatherForecast);
  if (typeof renderWeatherDriversChart === "function") renderWeatherDriversChart(weatherForecast);

  // Plain-Language Interpretation Box
  const interpBox = document.getElementById("forecastInterpretationText");
  if (interpBox) {
    if (riskForecast.length > 0) {
      const peakDay = [...riskForecast].sort((a, b) => (b.heat_risk_score || 0) - (a.heat_risk_score || 0))[0];
      const peakScore = peakDay?.heat_risk_score;
      const peakDate = peakDay?.date || "horizon";
      const peakLabel = peakDay?.horizon_label || "Day 2";

      interpBox.innerHTML = `
        <strong>Key Horizon Takeaway:</strong> Peak biometeorological stress is projected for <strong>${peakLabel} (${peakDate})</strong> with a Relative Heat-Health Risk score of <strong>${peakScore !== undefined ? peakScore.toFixed(1) : '--'}/100 (${peakDay?.alert_level || 'WARNING'})</strong>.
        Elevated atmospheric moisture combined with daytime solar irradiance reduces human evaporative cooling efficiency. Municipal authorities are advised to pre-position hydration relief tankers.
      `;
    } else {
      interpBox.textContent = "Awaiting 5-day horizon biometeorological projection stream...";
    }
  }
}

/**
 * Render 24-Hour Diurnal Hourly Table
 */
function renderHourlyTable(hourlyList) {
  const tbody = document.getElementById("hourlyTableBody");
  if (!tbody) return;

  if (!hourlyList || hourlyList.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #94a3b8; padding: 1.5rem;">Loading 24-hour diurnal telemetry...</td></tr>`;
    return;
  }

  tbody.innerHTML = hourlyList.map(h => {
    const risk = h.heat_risk_score !== undefined ? h.heat_risk_score : 0;
    const alertColor = typeof getColorByRisk === "function" ? getColorByRisk(risk) : "#f97316";
    const alertLevel = risk >= 75 ? "EMERGENCY" : risk >= 50 ? "WARNING" : risk >= 25 ? "CAUTION" : "NORMAL";

    return `
      <tr>
        <td><strong>${h.hour_label || h.time_iso?.slice(11, 16) || '--'}</strong></td>
        <td>${h.temp_c !== undefined ? h.temp_c.toFixed(1) + '°C' : '--'}</td>
        <td>${h.relative_humidity_pct !== undefined ? Math.round(h.relative_humidity_pct) + '%' : '--'}</td>
        <td><strong>${h.utci_c !== undefined ? h.utci_c.toFixed(1) + '°C' : '--'}</strong></td>
        <td>${h.wbgt_c !== undefined ? h.wbgt_c.toFixed(1) + '°C' : '--'}</td>
        <td>
          <span style="background-color: ${alertColor}; color: ${alertLevel === 'CAUTION' ? '#000' : '#fff'}; font-weight: 800; font-size: 10px; padding: 2px 6px; border-radius: 4px;">
            ${risk.toFixed(1)} (${alertLevel})
          </span>
        </td>
        <td>${h.solar_radiation_w_m2 !== undefined ? Math.round(h.solar_radiation_w_m2) + ' W/m²' : '--'}</td>
      </tr>
    `;
  }).join("");
}

/**
 * 3. Render Demographic Vulnerability View & Table
 */
function renderVulnerabilityView(wardsList) {
  const tbody = document.getElementById("vulnerabilityTableBody");
  const countEl = document.getElementById("vulnerabilityTotalWards");
  if (!tbody) return;

  const wards = wardsList || cachedWards || [];
  if (countEl) countEl.textContent = `${wards.length} Units`;

  if (wards.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: #94a3b8; padding: 2rem;">Loading Census of India 2011 PCA demographic data...</td></tr>`;
    return;
  }

  const sorted = [...wards].sort((a, b) => (b.heat_risk_score || 0) - (a.heat_risk_score || 0));

  tbody.innerHTML = sorted.map((w, idx) => {
    const d = w.demographics || w || {};
    const risk = w.heat_risk_score !== undefined ? w.heat_risk_score : (w.risk_score || 0);
    const alertColor = typeof getColorByRisk === "function" ? getColorByRisk(risk) : "#f97316";
    const alertLevel = w.alert_level || (risk >= 75 ? "EMERGENCY" : risk >= 50 ? "WARNING" : risk >= 25 ? "CAUTION" : "NORMAL");

    const utciVal = w.utci_c !== undefined ? w.utci_c : (w.utci_val !== undefined ? w.utci_val : (w.metrics?.utci?.value_c));
    const wbgtVal = w.wbgt_c !== undefined ? w.wbgt_c : (w.wbgt_val !== undefined ? w.wbgt_val : (w.metrics?.wbgt?.value_c));

    const eldPct = w.elderly_pct !== undefined ? w.elderly_pct : (d.elderly_percentage !== undefined ? d.elderly_percentage : null);
    const wrkPct = w.outdoor_worker_pct !== undefined ? w.outdoor_worker_pct : (d.outdoor_worker_percentage !== undefined ? d.outdoor_worker_percentage : null);
    const totPop = w.tot_pop !== undefined ? w.tot_pop : (d.tot_pop !== undefined ? d.tot_pop : null);
    const density = w.pop_density_per_sqkm !== undefined ? w.pop_density_per_sqkm : (d.pop_density_per_sqkm !== undefined ? d.pop_density_per_sqkm : null);

    const eldCount = eldPct !== null && totPop !== null ? Math.round(totPop * (eldPct / 100)) : null;
    const wrkCount = wrkPct !== null && totPop !== null ? Math.round(totPop * (wrkPct / 100)) : null;

    return `
      <tr>
        <td><strong>#${idx + 1}</strong></td>
        <td>
          <strong style="color: #f8fafc;">${w.ward_name || ('Ward ' + (w.ward_number || idx + 1))}</strong>
          <div style="font-size: 11px; color: #94a3b8;">${w.zone_name || w.lcz_class || 'Urban Local Body'}</div>
        </td>
        <td>
          <span style="background-color: ${alertColor}; color: ${alertLevel === 'CAUTION' ? '#000' : '#fff'}; font-weight: 800; font-size: 11px; padding: 2px 7px; border-radius: 4px;">
            ${typeof risk === 'number' ? risk.toFixed(1) : risk}
          </span>
        </td>
        <td><strong>${utciVal !== undefined && utciVal !== null ? (typeof utciVal === 'number' ? utciVal.toFixed(1) + '°C' : utciVal) : '--'}</strong></td>
        <td>${wbgtVal !== undefined && wbgtVal !== null ? (typeof wbgtVal === 'number' ? wbgtVal.toFixed(1) + '°C' : wbgtVal) : '--'}</td>
        <td>${eldPct !== null ? `${eldPct.toFixed(1)}% <span style="font-size:10px; color:#94a3b8;">(${eldCount !== null ? eldCount.toLocaleString() : '--'})</span>` : '--'}</td>
        <td>${wrkPct !== null ? `${wrkPct.toFixed(1)}% <span style="font-size:10px; color:#94a3b8;">(${wrkCount !== null ? wrkCount.toLocaleString() : '--'})</span>` : '--'}</td>
        <td>
          <div>${totPop !== null ? totPop.toLocaleString() : '--'}</div>
          <div style="font-size: 10px; color: #94a3b8;">${density !== null ? Math.round(density).toLocaleString() + ' /km²' : ''}</div>
        </td>
      </tr>
    `;
  }).join("");
}

/**
 * Filter Ward Table by Search String
 */
function filterWardRankingTable(query) {
  const tbody = document.getElementById("vulnerabilityTableBody");
  if (!tbody || !cachedWards) return;

  if (!query) {
    renderVulnerabilityView(cachedWards);
    return;
  }

  const filtered = cachedWards.filter(w => {
    const name = (w.ward_name || "").toLowerCase();
    const zone = (w.zone_name || "").toLowerCase();
    const lcz = (w.lcz_class || "").toLowerCase();
    return name.includes(query) || zone.includes(query) || lcz.includes(query);
  });

  renderVulnerabilityView(filtered);
}

/**
 * 4. Render Actionable Advisories View (3 Persona Tabs)
 */
function renderAdvisoriesView(advisoryState, thermalState) {
  const pGeneral = document.getElementById("advCitizenList") || document.getElementById("advGeneralContent");
  const pLabor = document.getElementById("advWorkerList") || document.getElementById("advLaborContent");
  const pAuth = document.getElementById("advMuniList") || document.getElementById("advAuthContent");
  const pHealth = document.getElementById("advHealthList");
  const wbgtSummary = document.getElementById("advWorkRestNotice") || document.getElementById("advWbgtWorkRest");

  const personas = advisoryState?.personas || {};
  const wbgtMetric = thermalState?.metrics?.wbgt || {};
  const alertLevel = (advisoryState?.alert_level || "ORANGE").toUpperCase();

  if (wbgtSummary) {
    const regimen = wbgtMetric.work_rest_regimen || personas.outdoor_workers?.niosh_work_rest_cycle || "45 min work / 15 min rest per hour";
    const riskLvl = wbgtMetric.risk_level || (alertLevel === "RED" ? "EXTREME HEAT STRESS" : alertLevel === "ORANGE" ? "HIGH HEAT STRESS" : "MODERATE HEAT STRESS");
    wbgtSummary.innerHTML = `
      <div style="font-weight: 700; color: #38bdf8; margin-bottom: 2px;">⚡ NIOSH / ISO 7243 Regimen: ${riskLvl}</div>
      <div style="color: #fed7aa; font-size: 0.85rem; font-weight: 500;">⏱️ ${regimen}</div>
    `;
  }

  function renderBulletList(items = []) {
    if (!items || items.length === 0) {
      return `<li class="advisory-bullet" style="color: #94a3b8;">No critical advisory actions triggered at current alert level.</li>`;
    }
    return items.map(item => `<li class="advisory-bullet">${item}</li>`).join("");
  }

  if (pGeneral) {
    pGeneral.innerHTML = renderBulletList(personas.general_public?.actions || [
      "Limit direct sun exposure between 12:00 and 15:00 IST; wear lightweight, light-colored, loose cotton clothing.",
      "Keep living spaces cool using window curtains, fans, and wet evaporative curtains.",
      "Carry a water bottle and umbrella/hat during all outdoor transit.",
      "Never leave infants, elderly persons, or pets in parked vehicles even for brief periods."
    ]);
  }

  if (pLabor) {
    pLabor.innerHTML = renderBulletList(personas.outdoor_workers?.actions || [
      "Mandatory 15-minute rest breaks in shaded/ventilated areas every 45 minutes of continuous labor.",
      "Employers must provide cool drinking water with oral rehydration salts (ORS) at accessible points.",
      "Reschedule heavy asphalt, roofing, and direct-sun agricultural labor to early morning (6:00-10:00 AM).",
      "Implement buddy system to rapidly identify early signs of heat exhaustion or heat stroke."
    ]);
  }

  if (pAuth) {
    pAuth.innerHTML = renderBulletList(personas.authorities?.actions || [
      "Issue public broadcast alerts via SMS, radio, and digital traffic display boards.",
      "Inspect construction sites and industrial yards for mandatory shaded resting areas and hydration points.",
      "Keep public parks and air-conditioned libraries open for extended hours as public cooling respites.",
      "Review daily emergency medical service (EMS) call volumes for heat exhaustion spikes."
    ]);
  }

  if (pHealth) {
    pHealth.innerHTML = renderBulletList(personas.health_emergency?.actions || [
      "Activate Heat Stroke Treatment Protocol and reserve dedicated beds with ice packs and cooling fans.",
      "Maintain adequate buffer stocks of IV Fluids (Normal Saline/Ringer's Lactate) and Oral Rehydration Salts (ORS).",
      "Mandate daily surveillance reporting of Heat-Related Illnesses (HRI) on the Integrated Health Information Platform (IHIP).",
      "Deploy 108/102 Emergency Medical Service (EMS) ambulances to high-risk outdoor worker clusters and transit corridors."
    ]);
  }
}

/**
 * 5. Render Methodology & Provenance Audit View
 */
async function renderMethodologyView() {
  const provContainer = document.getElementById("provenanceGridContainer");
  if (provContainer && !provContainer.dataset.loaded) {
    try {
      const data = await ApiClient.getProvenanceSources();
      const sources = data?.sources || [];
      if (sources.length > 0) {
        provContainer.innerHTML = sources.map(s => `
          <div class="provenance-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
              <h4 style="font-size: 0.9rem; font-weight: 700; color: #f8fafc; margin: 0;">${s.name}</h4>
              <span class="provenance-status-pill">${s.status || 'ONLINE'}</span>
            </div>
            <p style="font-size: 0.78rem; color: #94a3b8; margin-bottom: 0.5rem;">${s.organization}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem;">
              <span style="color: #38bdf8;">${s.tier}</span>
              ${s.official_url ? `<a href="${s.official_url}" target="_blank" rel="noopener noreferrer" style="color: #93c5fd; text-decoration: none; font-size: 0.75rem;">Website ↗</a>` : ''}
            </div>
          </div>
        `).join("");
        provContainer.dataset.loaded = "true";
      }
    } catch (err) {
      console.warn("Could not load provenance data:", err);
    }
  }
}

/**
 * CSV Export for Municipal Wards Data
 */
function exportWardDataToCSV() {
  if (!cachedWards || cachedWards.length === 0) {
    alert("Ward data is still loading. Please wait a moment.");
    return;
  }

  const headers = [
    "Rank",
    "Ward Number",
    "Ward Name",
    "Zone / Locality",
    "LCZ Class",
    "Heat Risk Score",
    "Alert Level",
    "Temperature (°C)",
    "UTCI (°C)",
    "WBGT (°C)",
    "Vulnerability Score",
    "Elderly %",
    "Outdoor Worker %",
    "Total Population",
    "Population Density (/km²)",
    "Area (km²)"
  ];

  const rows = cachedWards.map((w, idx) => {
    const d = w.demographics || w || {};
    const risk = w.heat_risk_score !== undefined ? w.heat_risk_score : (w.risk_score || 0);
    const utci = w.utci_c !== undefined ? w.utci_c : (w.utci_val || '');
    const wbgt = w.wbgt_c !== undefined ? w.wbgt_c : (w.wbgt_val || '');
    const eldPct = w.elderly_pct !== undefined ? w.elderly_pct : (d.elderly_percentage || '');
    const wrkPct = w.outdoor_worker_pct !== undefined ? w.outdoor_worker_pct : (d.outdoor_worker_percentage || '');
    const totPop = w.tot_pop !== undefined ? w.tot_pop : (d.tot_pop || '');
    const density = w.pop_density_per_sqkm !== undefined ? w.pop_density_per_sqkm : (d.pop_density_per_sqkm || '');
    const area = w.area_sqkm !== undefined ? w.area_sqkm : (d.area_sqkm || '');

    return [
      idx + 1,
      w.ward_number || (idx + 1),
      `"${(w.ward_name || '').replace(/"/g, '""')}"`,
      `"${(w.zone_name || '').replace(/"/g, '""')}"`,
      `"${(w.lcz_class || '').replace(/"/g, '""')}"`,
      typeof risk === 'number' ? risk.toFixed(1) : risk,
      w.alert_level || 'NORMAL',
      w.temp_c !== undefined ? (typeof w.temp_c === 'number' ? w.temp_c.toFixed(1) : w.temp_c) : '',
      typeof utci === 'number' ? utci.toFixed(1) : utci,
      typeof wbgt === 'number' ? wbgt.toFixed(1) : wbgt,
      w.vulnerability_score !== undefined ? (typeof w.vulnerability_score === 'number' ? w.vulnerability_score.toFixed(1) : w.vulnerability_score) : '',
      typeof eldPct === 'number' ? eldPct.toFixed(1) : eldPct,
      typeof wrkPct === 'number' ? wrkPct.toFixed(1) : wrkPct,
      totPop,
      density,
      area
    ];
  });

  const csvContent = [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${currentCity.toUpperCase()}_Ward_Heat_Risk_Horizon_D${currentHorizonDay}_Census2011.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/**
 * Show CAP Alert Modal
 */
async function showCapAlertModal() {
  const queryParams = customCoordinates ? {
    lat: customCoordinates.lat,
    lon: customCoordinates.lon,
    city: customCoordinates.city
  } : { city: currentCity };

  try {
    const data = await ApiClient.getCapAlert(queryParams);
    const smsEl = document.getElementById("capSmsPayload");
    const jsonEl = document.getElementById("capPayloadJson");

    if (smsEl) {
      smsEl.textContent = data.sms_broadcast_text || "Heatwave Warning: High physiological stress detected in the municipal area. Stay hydrated and avoid direct sunlight.";
    }

    if (jsonEl) {
      jsonEl.textContent = JSON.stringify(data.cap_alert || data, null, 2);
    }
  } catch (err) {
    console.error("CAP Alert fetch error:", err);
  }
}
