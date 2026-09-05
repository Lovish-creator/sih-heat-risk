/**
 * SIH26083 Real-World GIS Leaflet Map Controller.
 * Supports OpenStreetMap Streets, Esri High-Res Satellite View,
 * and Interactive Click/Drag-to-Pinpoint anywhere in India or globally.
 */

let mapInstance = null;
let geojsonLayer = null;
let userGpsMarker = null;
let layerControl = null;
let wardLayersMap = {};

function getColorByRisk(riskScore) {
  if (riskScore > 75.0) return "#ef4444"; // Red
  if (riskScore > 50.0) return "#f97316"; // Orange
  if (riskScore > 25.0) return "#f59e0b"; // Yellow
  return "#10b981"; // Green
}

function initMap(centerLat = 30.14505, centerLon = 74.19566, zoomLevel = 12) {
  if (mapInstance) {
    mapInstance.remove();
  }

  mapInstance = L.map('map', {
    center: [centerLat, centerLon],
    zoom: zoomLevel,
    zoomControl: true
  });

  // 1. OpenStreetMap Standard (Real Streets, Highways, Towns, Buildings)
  const osmStreets = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  });

  // 2. Esri World Imagery (Real High-Resolution Satellite View)
  const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
  });

  // 3. CartoDB Dark Matter (Disaster Theme)
  const cartoDark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://carto.com/">CARTO</a>'
  });

  // Default to OpenStreetMap Streets
  osmStreets.addTo(mapInstance);

  const baseMaps = {
    "🗺️ Real Street Map (OpenStreetMap)": osmStreets,
    "🛰️ Satellite View (Esri High-Res)": esriSatellite,
    "🌙 Dark Disaster Theme (CartoDB)": cartoDark
  };

  layerControl = L.control.layers(baseMaps, null, { position: 'topright' }).addTo(mapInstance);

  // Enable Interactive Map Click to Pinpoint Any Location
  mapInstance.on('click', async (e) => {
    const lat = e.latlng.lat;
    const lon = e.latlng.lng;
    if (typeof handleMapClickLocation === "function") {
      await handleMapClickLocation(lat, lon);
    }
  });

  return mapInstance;
}

function setUserLocationMarker(lat, lon, label = "Selected Location", draggable = true) {
  if (!mapInstance) {
    initMap(lat, lon, 12);
  }

  if (userGpsMarker) {
    mapInstance.removeLayer(userGpsMarker);
  }

  // Create custom pulsing GPS HTML marker
  const pulseIcon = L.divIcon({
    className: 'custom-gps-icon',
    html: `<div class="user-gps-pulse"></div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  });

  userGpsMarker = L.marker([lat, lon], {
    icon: pulseIcon,
    draggable: draggable
  }).addTo(mapInstance);

  userGpsMarker.bindPopup(`
    <div style="font-family: 'Inter', sans-serif; font-size: 13px;">
      <strong style="color: #0284c7;">📍 ${label}</strong>
      <div style="font-size: 11px; color: #475569; margin-top: 2px;">
        Lat: ${lat.toFixed(4)}, Lon: ${lon.toFixed(4)}
      </div>
      <div style="font-size: 10px; color: #059669; margin-top: 4px;">
        💡 Click or drag anywhere on map to change location
      </div>
    </div>
  `).openPopup();

  // Handle Drag End event
  userGpsMarker.on('dragend', async (e) => {
    const newPos = e.target.getLatLng();
    if (typeof handleMapClickLocation === "function") {
      await handleMapClickLocation(newPos.lat, newPos.lng);
    }
  });

  mapInstance.setView([lat, lon], Math.max(mapInstance.getZoom(), 12));
}

async function loadWardRiskLayer(cityId = "abohar", horizonDay = 1, customLat = null, customLon = null) {
  if (!mapInstance) {
    initMap();
  }

  try {
    let url = `/api/v1/map/risk?day=${horizonDay}`;
    if (customLat !== null && customLon !== null) {
      url += `&lat=${customLat}&lon=${customLon}`;
    } else {
      url += `&city=${cityId}`;
    }

    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to load GeoJSON");
    const geojsonData = await res.json();

    if (geojsonLayer) {
      mapInstance.removeLayer(geojsonLayer);
    }

    wardLayersMap = {};

    geojsonLayer = L.geoJSON(geojsonData, {
      style: function (feature) {
        const risk = feature.properties.heat_risk_score || 0;
        return {
          fillColor: getColorByRisk(risk),
          weight: 2,
          opacity: 0.95,
          color: '#ffffff',
          dashArray: '2',
          fillOpacity: 0.58
        };
      },
      onEachFeature: function (feature, layer) {
        const p = feature.properties;
        const d = p.demographics || {};
        const lw = p.local_weather || {};
        
        if (p.ward_number !== undefined) {
          wardLayersMap[p.ward_number] = layer;
        }

        const popupContent = `
          <div style="font-family: 'Inter', sans-serif; font-size: 12.5px; min-width: 250px; color: #0f172a;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
              <h4 style="margin: 0; color: #0284c7; font-size: 13.5px; font-weight: 700;">${p.ward_name || `Ward ${p.ward_number}`}</h4>
              <span style="background-color: ${p.alert_color}; color: ${p.alert_level === 'YELLOW' ? '#000' : '#fff'}; font-weight: 800; font-size: 10px; padding: 2px 6px; border-radius: 4px;">
                ${p.alert_level}
              </span>
            </div>
            <div style="font-size: 11px; color: #475569; margin-bottom: 6px;">
              ${p.city_name || ''} &bull; ${p.zone_name || 'Municipal Ward'} &bull; <span style="color: #0284c7; font-weight: 600;">${p.lcz_class || 'LCZ 3 Compact Low-Rise'}</span>
            </div>
            <div style="background-color: #f1f5f9; padding: 5px 8px; border-radius: 4px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
              <span style="font-weight: 600; color: #334155;">Relative Heat Risk:</span>
              <span style="color: ${p.alert_color}; font-weight: 800; font-size: 14px;">${p.heat_risk_score} / 100</span>
            </div>
            <div style="font-size: 11.5px; line-height: 1.45; color: #334155;">
              <div>🌡️ <strong>Air Temp (Ta):</strong> ${lw.temp_c !== undefined ? lw.temp_c : '--'}°C <span style="font-size: 10.5px; color: ${p.uhi_delta_c >= 0 ? '#ef4444' : '#059669'}; font-weight: 600;">(${p.uhi_delta_c !== undefined ? (p.uhi_delta_c >= 0 ? '+' + p.uhi_delta_c : p.uhi_delta_c) : '+0.0'}°C UHI)</span> | <strong>RH:</strong> ${lw.relative_humidity_pct !== undefined ? lw.relative_humidity_pct : '--'}%</div>
              <div>🔥 <strong>Physiological UTCI:</strong> ${p.utci_val}°C (${p.utci_category || 'Heat Stress'})</div>
              <div>💦 <strong>Occupational WBGT:</strong> ${p.wbgt_val}°C (${p.wbgt_risk || 'Risk'})</div>
              <hr style="border-color: #cbd5e1; margin: 4px 0;">
              <div>📐 <strong>Physical Ward Area:</strong> ${d.area_sqkm ? `${d.area_sqkm} km² (${d.area_hectares || Math.round(d.area_sqkm * 100)} ha)` : 'N/A'}</div>
              <div>👥 <strong>Population:</strong> ${d.tot_pop ? d.tot_pop.toLocaleString() : 'N/A'} (Density: ${d.pop_density_per_sqkm ? Math.round(d.pop_density_per_sqkm).toLocaleString() : 'N/A'}/km²)</div>
              <div>👴 <strong>Elderly (60+):</strong> ${d.pop_elderly_60plus ? d.pop_elderly_60plus.toLocaleString() : 'N/A'} (${d.elderly_percentage}%)</div>
              <div>🔨 <strong>Outdoor Laborers:</strong> ${d.workers_outdoor ? d.workers_outdoor.toLocaleString() : 'N/A'} (${d.outdoor_worker_percentage}%)</div>
            </div>
          </div>
        `;
        layer.bindPopup(popupContent);

        layer.on({
          mouseover: function (e) {
            const l = e.target;
            l.setStyle({
              weight: 3.5,
              color: '#38bdf8',
              fillOpacity: 0.8
            });
            l.bringToFront();
          },
          mouseout: function (e) {
            geojsonLayer.resetStyle(e.target);
          }
        });
      }
    }).addTo(mapInstance);

    if (customLat === null || customLon === null) {
      mapInstance.fitBounds(geojsonLayer.getBounds(), { padding: [20, 20] });
    }

  } catch (err) {
    console.error("GIS Error:", err);
  }
}

function zoomToWard(wardNumber) {
  if (!mapInstance || !wardLayersMap[wardNumber]) return;
  const layer = wardLayersMap[wardNumber];
  mapInstance.fitBounds(layer.getBounds(), { padding: [50, 50], maxZoom: 15 });
  layer.openPopup();
  layer.setStyle({
    weight: 4,
    color: '#38bdf8',
    fillOpacity: 0.85
  });
  setTimeout(() => {
    if (geojsonLayer && wardLayersMap[wardNumber]) {
      geojsonLayer.resetStyle(wardLayersMap[wardNumber]);
    }
  }, 3500);
}
