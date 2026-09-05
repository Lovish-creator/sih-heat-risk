/**
 * SIH26083 Real-Time Live Application Controller.
 * Manages live GPS auto-detection, click-to-pinpoint map interactions,
 * OpenStreetMap Nominatim search, and hourly/daily biometeorological streams.
 */

let currentCity = "abohar";
let customCoordinates = null; // { lat, lon, name, city }
let currentHorizonDay = 1;
let currentPersona = "general_public";
let cachedForecastData = null;
let cachedHourlyData = null;
let cachedAdvisories = null;
let cachedWardsData = [];
let isHourlyView = false;

document.addEventListener("DOMContentLoaded", () => {
  initApp();
  setupEventListeners();
  initScenarioRunner();
});

async function initApp() {
  initMap(30.14505, 74.19566, 12);
  await loadLocations();
  
  // Try high-accuracy location auto-detection on first visit
  detectUserLocation(false);
}

function setupEventListeners() {
  // 1. Detect My Location Button
  const detectBtn = document.getElementById("btnDetectLocation");
  if (detectBtn) {
    detectBtn.addEventListener("click", () => {
      detectUserLocation(true);
    });
  }

  // 2. City dropdown change
  const citySelect = document.getElementById("citySelect");
  if (citySelect) {
    citySelect.addEventListener("change", (e) => {
      customCoordinates = null;
      currentCity = e.target.value;
      const locBanner = document.getElementById("locationBannerText");
      if (locBanner) locBanner.innerHTML = `<strong>📍 Selected City:</strong> ${e.target.options[e.target.selectedIndex].text}`;
      refreshDashboardData();
    });
  }

  // Ward search / filter input
  const wardFilter = document.getElementById("wardFilterInput");
  if (wardFilter) {
    wardFilter.addEventListener("input", (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!cachedWardsData || cachedWardsData.length === 0) return;
      if (!q) {
        renderWardCards(cachedWardsData);
      } else {
        const filtered = cachedWardsData.filter(w => 
          (w.ward_name && w.ward_name.toLowerCase().includes(q)) ||
          (`ward ${w.ward_number}`.includes(q)) ||
          (w.alert_level && w.alert_level.toLowerCase().includes(q))
        );
        renderWardCards(filtered);
      }
    });
  }

  // 3. Search Box for Any City/Town via OpenStreetMap Nominatim
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
          const res = await fetch(`/api/v1/geocode/search?q=${encodeURIComponent(query)}&limit=6`);
          const data = await res.json();
          const results = data.results || [];

          if (results.length === 0) {
            searchDropdown.innerHTML = `<div class="search-result-item" style="color: #94a3b8;">No locations found. Try searching town, district, or pin code.</div>`;
          } else {
            searchDropdown.innerHTML = results.map(r => `
              <div class="search-result-item" data-lat="${r.latitude}" data-lon="${r.longitude}" data-name="${r.name}" data-city="${r.city}">
                <strong style="color: #38bdf8;">${r.city}</strong> <span style="font-size: 11px; color: #94a3b8;">${r.name}</span>
              </div>
            `).join("");

            searchDropdown.querySelectorAll(".search-result-item").forEach(item => {
              item.addEventListener("click", () => {
                const lat = parseFloat(item.dataset.lat);
                const lon = parseFloat(item.dataset.lon);
                const name = item.dataset.name;
                const city = item.dataset.city;

                customCoordinates = { lat, lon, name, city };
                searchDropdown.style.display = "none";
                searchInput.value = city;

                const locBanner = document.getElementById("locationBannerText");
                if (locBanner) {
                  locBanner.innerHTML = `<strong>📍 Selected Location:</strong> ${city} <span style="font-size: 12px; color: #94a3b8;">(${lat.toFixed(4)}, ${lon.toFixed(4)})</span>`;
                }

                setUserLocationMarker(lat, lon, city);
                refreshDashboardData();
              });
            });
          }
          searchDropdown.style.display = "block";
        } catch (err) {
          console.error("Geocoding search failed:", err);
        }
      }, 300);
    });

    document.addEventListener("click", (e) => {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.style.display = "none";
      }
    });
  }

  // 4. Forecast View Toggle (Daily vs Hourly)
  const btnViewDaily = document.getElementById("btnViewDaily");
  const btnViewHourly = document.getElementById("btnViewHourly");

  if (btnViewDaily && btnViewHourly) {
    btnViewDaily.addEventListener("click", () => {
      isHourlyView = false;
      btnViewDaily.classList.add("active");
      btnViewHourly.classList.remove("active");
      if (cachedForecastData) renderForecastChart(cachedForecastData, false);
    });

    btnViewHourly.addEventListener("click", async () => {
      isHourlyView = true;
      btnViewHourly.classList.add("active");
      btnViewDaily.classList.remove("active");
      await fetchHourlyData();
    });
  }

  // 5. Manual Coordinates Modal
  const btnManualCoords = document.getElementById("btnManualCoords");
  const coordsModal = document.getElementById("coordsModal");
  const coordsClose = document.getElementById("coordsClose");
  const btnApplyCoords = document.getElementById("btnApplyCoords");

  if (btnManualCoords && coordsModal) {
    btnManualCoords.addEventListener("click", () => coordsModal.classList.add("active"));
  }
  if (coordsClose && coordsModal) {
    coordsClose.addEventListener("click", () => coordsModal.classList.remove("active"));
  }
  if (btnApplyCoords && coordsModal) {
    btnApplyCoords.addEventListener("click", async () => {
      const latVal = parseFloat(document.getElementById("inputLat").value);
      const lonVal = parseFloat(document.getElementById("inputLon").value);
      if (!isNaN(latVal) && !isNaN(lonVal) && latVal >= -90 && latVal <= 90 && lonVal >= -180 && lonVal <= 180) {
        coordsModal.classList.remove("active");
        await handleMapClickLocation(latVal, lonVal);
      } else {
        alert("Please enter valid latitude (-90 to 90) and longitude (-180 to 180).");
      }
    });
  }

  // 6. Horizon Day Tabs
  document.querySelectorAll(".horizon-tab").forEach(tab => {
    tab.addEventListener("click", (e) => {
      document.querySelectorAll(".horizon-tab").forEach(t => t.classList.remove("active"));
      e.target.classList.add("active");
      currentHorizonDay = parseInt(e.target.dataset.day);
      updateHorizonView();
    });
  });

  // 7. Persona Advisory Tabs
  document.querySelectorAll(".persona-tab").forEach(tab => {
    tab.addEventListener("click", (e) => {
      document.querySelectorAll(".persona-tab").forEach(t => t.classList.remove("active"));
      e.target.classList.add("active");
      currentPersona = e.target.dataset.persona;
      renderPersonaAdvisories();
    });
  });

  // 8. Provenance Modal
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
    modalClose.addEventListener("click", () => provenanceModal.classList.remove("active"));
  }
}

/**
 * Global Handler triggered when clicking anywhere on the real map
 */
async function handleMapClickLocation(lat, lon) {
  const locBanner = document.getElementById("locationBannerText");
  if (locBanner) locBanner.textContent = `Resolving clicked location (${lat.toFixed(4)}, ${lon.toFixed(4)})...`;

  try {
    const res = await fetch(`/api/v1/geocode/reverse?lat=${lat}&lon=${lon}`);
    const geo = await res.json();
    const city = geo.city || "Custom Location";
    const suburb = geo.suburb_or_ward ? `${geo.suburb_or_ward}, ` : "";
    const state = geo.state ? `, ${geo.state}` : "";

    customCoordinates = { lat, lon, name: geo.display_name, city };

    if (locBanner) {
      locBanner.innerHTML = `<strong>📍 Real-Time Location:</strong> ${suburb}${city}${state} <span style="font-size: 12px; color: #94a3b8;">(${lat.toFixed(4)}, ${lon.toFixed(4)})</span>`;
    }

    setUserLocationMarker(lat, lon, `${suburb}${city}`);
    await refreshDashboardData();
  } catch (err) {
    console.error("Click geocode error:", err);
  }
}

/**
 * Detect User Real Location via High Accuracy GPS with IP Geolocation fallback
 */
async function detectUserLocation(userTriggered = false) {
  const detectBtn = document.getElementById("btnDetectLocation");
  const locBanner = document.getElementById("locationBannerText");
  
  if (detectBtn) detectBtn.textContent = "⌛ Detecting...";

  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        await handleDetectedCoordinates(lat, lon, "High-Accuracy GPS");
        if (detectBtn) detectBtn.innerHTML = "📍 Detect My Location";
      },
      async (err) => {
        console.warn("Browser GPS permission not granted. Using IP Geolocation fallback...", err);
        await fallbackIpGeolocation();
        if (detectBtn) detectBtn.innerHTML = "📍 Detect My Location";
      },
      { timeout: 8000, enableHighAccuracy: true, maximumAge: 0 }
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
    await handleDetectedCoordinates(lat, lon, `IP Network (${city}, ${region})`);
  } catch (err) {
    console.error("IP fallback failed:", err);
    // Default to Ahmedabad if both fail
    await refreshDashboardData();
  }
}

async function handleDetectedCoordinates(lat, lon, sourceLabel) {
  try {
    const res = await fetch(`/api/v1/geocode/reverse?lat=${lat}&lon=${lon}`);
    const geo = await res.json();
    const city = geo.city || "Your Location";
    const suburb = geo.suburb_or_ward ? `${geo.suburb_or_ward}, ` : "";
    const state = geo.state ? `, ${geo.state}` : "";

    customCoordinates = { lat, lon, name: geo.display_name, city };

    const locBanner = document.getElementById("locationBannerText");
    if (locBanner) {
      locBanner.innerHTML = `<strong>📍 Real-Time Location (${sourceLabel}):</strong> ${suburb}${city}${state} <span style="font-size: 12px; color: #94a3b8;">(${lat.toFixed(4)}, ${lon.toFixed(4)})</span>`;
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
    let currentUrl = `/api/v1/weather/current?`;
    let forecastUrl = `/api/v1/risk/forecast?days=7&`;
    let advUrl = `/api/v1/advisory?`;

    if (customCoordinates) {
      const coordStr = `lat=${customCoordinates.lat}&lon=${customCoordinates.lon}`;
      currentUrl += coordStr;
      forecastUrl += coordStr;
      advUrl += coordStr;
    } else {
      currentUrl += `city=${currentCity}`;
      forecastUrl += `city=${currentCity}`;
      advUrl += `city=${currentCity}`;
    }

    // 1. Fetch Real-Time Current Weather Observation
    const currentRes = await fetch(currentUrl);
    const currentData = await currentRes.json();
    const liveWeather = currentData.weather || {};

    // 2. Fetch 7-Day Live Risk Forecast
    const riskRes = await fetch(forecastUrl);
    const riskData = await riskRes.json();
    cachedForecastData = riskData.horizon || [];

    // 3. Fetch Live Advisories
    const advRes = await fetch(advUrl);
    cachedAdvisories = await advRes.json();

    // 4. Update Time Badge
    const timeBadge = document.getElementById("liveTimeBadge");
    if (timeBadge && liveWeather.timestamp) {
      const timeStr = liveWeather.timestamp.slice(11, 16) || "Now";
      timeBadge.textContent = `● LIVE STREAM (${timeStr} Local)`;
    }

    // 5. Update View Components
    updateHorizonView(liveWeather);
    updateMeteorologicalTelemetry(liveWeather);
    await fetchWardsData();
    await fetchHourlyData();
    
    if (isHourlyView) {
      if (cachedHourlyData.length > 0) renderForecastChart(cachedHourlyData, true);
    } else {
      renderForecastChart(cachedForecastData, false);
    }
    
    renderPersonaAdvisories();

  } catch (err) {
    console.error("Dashboard refresh error:", err);
  }
}

function updateMeteorologicalTelemetry(w) {
  if (!w) return;

  const elDew = document.getElementById("meteoDewPoint");
  const elFeels = document.getElementById("meteoFeelsLike");
  const elSolar = document.getElementById("meteoSolar");
  const elDni = document.getElementById("meteoDni");
  const elUv = document.getElementById("meteoUv");
  const elUvCat = document.getElementById("meteoUvCategory");
  const elWind = document.getElementById("meteoWind");
  const elWindDir = document.getElementById("meteoWindDir");
  const elGusts = document.getElementById("meteoGusts");
  const elVapor = document.getElementById("meteoVaporPres");
  const elRh = document.getElementById("meteoRh");
  const elPress = document.getElementById("meteoPressure");
  const elCloud = document.getElementById("meteoCloud");

  if (elDew) elDew.textContent = `${w.dew_point_c !== undefined ? w.dew_point_c : '--'}°C`;
  if (elFeels) elFeels.textContent = `${w.apparent_temperature_c !== undefined ? w.apparent_temperature_c : (w.temp_c || '--')}°C`;
  if (elSolar) elSolar.textContent = `${w.solar_radiation_w_m2 !== undefined ? w.solar_radiation_w_m2 : '--'} W/m²`;
  if (elDni) elDni.textContent = `${w.direct_normal_irradiance_w_m2 !== undefined ? w.direct_normal_irradiance_w_m2 : '--'} W/m²`;
  
  if (elUv) elUv.textContent = `${w.uv_index !== undefined ? w.uv_index : '--'}`;
  if (elUvCat) {
    const uvVal = w.uv_index || 0;
    const uvLabel = uvVal >= 11 ? 'Extreme' : uvVal >= 8 ? 'Very High' : uvVal >= 6 ? 'High' : uvVal >= 3 ? 'Moderate' : 'Low';
    elUvCat.textContent = `UV: ${uvLabel} (${uvVal})`;
  }

  if (elWind) elWind.textContent = `${w.wind_speed_kmh !== undefined ? w.wind_speed_kmh : '--'} km/h (${w.wind_speed_10m_m_s || '--'} m/s)`;
  if (elWindDir) elWindDir.textContent = `Dir: ${w.wind_direction_compass || 'N/A'} (${w.wind_direction_deg !== undefined ? w.wind_direction_deg : '--'}°)`;
  if (elGusts) elGusts.textContent = `${w.wind_gusts_kmh !== undefined ? w.wind_gusts_kmh : '--'} km/h`;

  if (elVapor) elVapor.textContent = `${w.vapor_pressure_hpa !== undefined ? w.vapor_pressure_hpa : '--'} hPa`;
  if (elRh) elRh.textContent = `${w.relative_humidity_pct !== undefined ? w.relative_humidity_pct : '--'}%`;
  if (elPress) elPress.textContent = `${w.surface_pressure_hpa !== undefined ? w.surface_pressure_hpa : '--'} hPa`;
  if (elCloud) elCloud.textContent = `${w.cloud_cover_pct !== undefined ? w.cloud_cover_pct : '--'}%`;
}

async function fetchHourlyData() {
  try {
    let hourlyUrl = `/api/v1/weather/hourly?hours=24&`;
    if (customCoordinates) {
      hourlyUrl += `lat=${customCoordinates.lat}&lon=${customCoordinates.lon}`;
    } else {
      hourlyUrl += `city=${currentCity}`;
    }

    const res = await fetch(hourlyUrl);
    const data = await res.json();
    cachedHourlyData = data.hourly_series || [];

    renderHourlyTable(cachedHourlyData);

    if (isHourlyView && cachedHourlyData.length > 0) {
      renderForecastChart(cachedHourlyData, true);
    }
  } catch (err) {
    console.error("Failed to fetch hourly weather:", err);
  }
}

function renderHourlyTable(hourly) {
  const tbody = document.getElementById("hourlyTableBody");
  if (!tbody) return;

  if (!hourly || hourly.length === 0) {
    tbody.innerHTML = `<tr><td colspan="11" style="text-align: center; color: #94a3b8; padding: 1rem;">No hourly stream available.</td></tr>`;
    return;
  }

  tbody.innerHTML = hourly.map(h => {
    const hzColor = h.hazard_score >= 75 ? '#ef4444' : h.hazard_score >= 50 ? '#f97316' : h.hazard_score >= 25 ? '#f59e0b' : '#10b981';
    return `
      <tr>
        <td><strong>${h.hour_label}</strong> <span style="font-size: 10px; color: #94a3b8;">(${h.date})</span></td>
        <td style="font-weight: 700; color: #f8fafc;">${h.temp_c}°C</td>
        <td style="color: #38bdf8;">${h.dew_point_c !== undefined ? h.dew_point_c : '--'}°C</td>
        <td>${h.relative_humidity_pct}%</td>
        <td>${h.wind_speed_kmh || '--'} km/h (${h.wind_speed_10m_m_s} m/s)</td>
        <td>${h.wind_direction_compass || '--'} (${h.wind_direction_deg || 0}°)</td>
        <td style="color: #f59e0b;">${h.solar_radiation_w_m2} W/m²</td>
        <td><span style="font-weight: 700; color: ${h.uv_index >= 8 ? '#ef4444' : h.uv_index >= 6 ? '#f97316' : '#a855f7'};">${h.uv_index}</span></td>
        <td style="font-weight: 700; color: #fb923c;">${h.utci_c}°C <span style="font-size: 10px;">(${h.utci_category})</span></td>
        <td style="font-weight: 700; color: #38bdf8;">${h.wbgt_c}°C</td>
        <td><span style="background-color: ${hzColor}; color: #fff; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 11px;">${h.hazard_score}/100</span></td>
      </tr>
    `;
  }).join("");
}

async function fetchWardsData() {
  try {
    let wardsUrl = `/api/v1/wards/summary?day=${currentHorizonDay}&`;
    if (customCoordinates) {
      wardsUrl += `lat=${customCoordinates.lat}&lon=${customCoordinates.lon}`;
    } else {
      wardsUrl += `city=${currentCity}`;
    }

    const res = await fetch(wardsUrl);
    if (!res.ok) throw new Error("Failed to fetch wards summary");
    const data = await res.json();

    // Update counters
    const dist = data.alert_distribution || {};
    const elRed = document.getElementById("statRed");
    const elOrange = document.getElementById("statOrange");
    const elYellow = document.getElementById("statYellow");
    const elGreen = document.getElementById("statGreen");
    const elCount = document.getElementById("wardCountBadge");
    const elAttr = document.getElementById("wardCensusAttribution");

    if (elRed) elRed.textContent = `🔴 ${dist.red_emergency || 0} Red Emergency`;
    if (elOrange) elOrange.textContent = `🟠 ${dist.orange_warning || 0} Orange Warning`;
    if (elYellow) elYellow.textContent = `🟡 ${dist.yellow_watch || 0} Yellow Watch`;
    if (elGreen) elGreen.textContent = `🟢 ${dist.green_normal || 0} Normal`;

    if (elCount) elCount.textContent = `${data.total_wards || 50} OFFICIAL MUNICIPAL WARDS`;
    if (elAttr) elAttr.textContent = `${data.city_name} (${data.state_name}) — ${data.census_source || 'Census 2011 PCA'}`;

    cachedWardsData = data.all_wards || [];
    renderWardCards(cachedWardsData);
  } catch (err) {
    console.error("Ward summary fetch error:", err);
  }
}

function renderWardCards(wards) {
  const container = document.getElementById("wardGridContainer");
  if (!container) return;

  if (!wards || wards.length === 0) {
    container.innerHTML = `<div style="color: #94a3b8; padding: 1rem;">No matching municipal wards found.</div>`;
    return;
  }

  container.innerHTML = wards.map(w => {
    const alertClass = w.alert_level === 'RED' ? 'border-red' :
                       w.alert_level === 'ORANGE' ? 'border-orange' :
                       w.alert_level === 'YELLOW' ? 'border-yellow' : 'border-green';
    
    const badgeColor = w.alert_color || '#10b981';
    const textColor = w.alert_level === 'YELLOW' ? '#000' : '#fff';

    return `
      <div class="ward-card ${alertClass}" onclick="zoomToWard(${w.ward_number})">
        <div class="ward-card-title">
          <span>${w.ward_name || `Ward ${w.ward_number}`}</span>
          <span style="background-color: ${badgeColor}; color: ${textColor}; font-weight: 800; font-size: 10px; padding: 2px 6px; border-radius: 4px;">
            ${w.alert_level} (${w.heat_risk_score})
          </span>
        </div>
        <div class="ward-card-subtitle">
          🌡️ <strong>${w.temp_c}°C</strong> <span style="font-size: 10px; color: ${w.uhi_delta_c >= 0 ? '#ef4444' : '#10b981'}; font-weight: 700;">(${w.uhi_delta_c !== undefined ? (w.uhi_delta_c >= 0 ? '+' + w.uhi_delta_c : w.uhi_delta_c) : '+0.0'}°C UHI)</span> &bull; 🏙️ <span style="color: #38bdf8; font-weight: 600;">${w.lcz_class || 'LCZ 3'}</span>
        </div>
        <div class="ward-metrics-row">
          <span class="ward-metric-badge">🔥 UTCI: ${w.utci_c}°C</span>
          <span class="ward-metric-badge">💦 WBGT: ${w.wbgt_c}°C</span>
          <span class="ward-metric-badge">📊 Vuln: ${w.vulnerability_score}/100</span>
        </div>
        <div class="ward-demo-summary">
          <div>📐 <strong>Area:</strong> ${w.area_sqkm} km² (${w.area_hectares || Math.round(w.area_sqkm * 100)} ha) &bull; <strong>Density:</strong> ${Math.round(w.pop_density_per_sqkm || 1200).toLocaleString()}/km²</div>
          <div>👥 <strong>Pop:</strong> ${w.tot_pop ? w.tot_pop.toLocaleString() : 'N/A'} &bull; 🔨 <strong>Labor:</strong> ${w.outdoor_worker_pct}% &bull; 👴 <strong>60+:</strong> ${w.elderly_pct}%</div>
          <div style="margin-top: 4px; color: #38bdf8; font-weight: 600; font-size: 11px;">
            📍 Click to zoom on map &rarr;
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function updateHorizonView(liveWeather = null) {
  if (!cachedForecastData || cachedForecastData.length === 0) return;

  const currentItem = cachedForecastData[currentHorizonDay - 1] || cachedForecastData[0];

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

  // If viewing current day and we have instant real-time live current observation, display it
  if (currentHorizonDay === 1 && liveWeather && liveWeather.temp_c !== undefined) {
    if (kpiTemp) kpiTemp.textContent = `${liveWeather.temp_c}°C`;
  } else {
    if (kpiTemp) kpiTemp.textContent = `${currentItem.temp_c}°C`;
  }

  if (kpiUtci) kpiUtci.textContent = `${currentItem.utci_c}°C`;
  if (kpiWbgt) kpiWbgt.textContent = `${currentItem.wbgt_c}°C`;
  if (kpiActionSummary) kpiActionSummary.textContent = currentItem.action_summary;

  // Refresh GIS Map and Wards for this Horizon Day & Coordinates
  const lat = customCoordinates ? customCoordinates.lat : null;
  const lon = customCoordinates ? customCoordinates.lon : null;
  loadWardRiskLayer(currentCity, currentHorizonDay, lat, lon);
  fetchWardsData();
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
      regimenNotice.innerHTML = `<strong>NIOSH Work/Rest Directive:</strong> ${personaData.niosh_work_rest_cycle}`;
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
      <h3 style="color: #38bdf8; margin-bottom: 1rem;">Real-Time Open Data Streams & Physics Engines</h3>
      <div style="font-size: 13.5px; line-height: 1.6; color: #cbd5e1;">
        <p><strong>Open-Meteo Open Weather API:</strong> Live real-time hourly & 7-day surface meteorology (temperature, relative humidity, 10m wind, and direct shortwave solar radiation flux in W/m²).</p>
        <p style="margin-top: 8px;"><strong>OpenStreetMap Nominatim:</strong> Global open reverse and forward geocoding with street-level address resolution.</p>
        <p style="margin-top: 8px;"><strong>NASA POWER API:</strong> Climatological reanalysis and solar surface irradiance validation.</p>
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

/* Dynamic Comparative Scenario Runner via Backend Physics Engine */
function initScenarioRunner() {
  const btnRun = document.getElementById("btnRunScenario");
  if (!btnRun) return;

  btnRun.addEventListener("click", async () => {
    btnRun.textContent = "⌛ Computing Physics...";

    try {
      // Scenario A: Dry & Windy (Ta=40°C, RH=15%, Wind=5.0m/s, Solar=150W/m²)
      const resA_fetch = await fetch("/api/v1/thermal/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          temp_c: 40.0,
          relative_humidity_pct: 15.0,
          wind_speed_10m_m_s: 5.0,
          solar_radiation_w_m2: 150.0
        })
      });
      const dataA = await resA_fetch.json();
      const hzA = dataA.hazard_analysis;

      // Scenario B: Humid, Stagnant & High Solar (Ta=40°C, RH=70%, Wind=0.8m/s, Solar=800W/m²)
      const resB_fetch = await fetch("/api/v1/thermal/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          temp_c: 40.0,
          relative_humidity_pct: 70.0,
          wind_speed_10m_m_s: 0.8,
          solar_radiation_w_m2: 800.0
        })
      });
      const dataB = await resB_fetch.json();
      const hzB = dataB.hazard_analysis;

      document.getElementById("scenA_utci").textContent = `${hzA.metrics.utci.value_c}°C (${hzA.metrics.utci.category})`;
      document.getElementById("scenA_wbgt").textContent = `${hzA.metrics.wbgt.value_c}°C`;
      document.getElementById("scenA_hazard").textContent = `${hzA.composite_hazard_score}/100`;
      document.getElementById("scenA_level").textContent = hzA.composite_hazard_score >= 75 ? "RED (Emergency Alert)" : hzA.composite_hazard_score >= 50 ? "ORANGE (Warning)" : "YELLOW (Watch)";

      document.getElementById("scenB_utci").textContent = `${hzB.metrics.utci.value_c}°C (${hzB.metrics.utci.category})`;
      document.getElementById("scenB_wbgt").textContent = `${hzB.metrics.wbgt.value_c}°C`;
      document.getElementById("scenB_hazard").textContent = `${hzB.composite_hazard_score}/100`;
      document.getElementById("scenB_level").textContent = hzB.composite_hazard_score >= 75 ? "RED (Emergency Alert)" : hzB.composite_hazard_score >= 50 ? "ORANGE (Warning)" : "YELLOW (Watch)";

    } catch (err) {
      console.error("Scenario calculation error:", err);
    } finally {
      btnRun.textContent = "Run Comparative Calculation";
    }
  });
}
