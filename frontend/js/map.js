/**
 * SIH26083 Real-World GIS Leaflet Map Controller.
 * Supports OpenStreetMap Streets, Esri High-Res Satellite View,
 * and Interactive Click/Drag-to-Pinpoint anywhere in India or globally.
 */

let mapInstance = null;
let geojsonLayer = null;
let userGpsMarker = null;
let layerControl = null;

function getColorByRisk(riskScore) {
  if (riskScore > 75.0) return "#ef4444"; // Red
  if (riskScore > 50.0) return "#f97316"; // Orange
  if (riskScore > 25.0) return "#f59e0b"; // Yellow
  return "#10b981"; // Green
}

function initMap(centerLat = 20.5937, centerLon = 78.9629, zoomLevel = 5) {
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

  mapInstance.setView([lat, lon], Math.max(mapInstance.getZoom(), 11));
}

async function loadWardRiskLayer(cityId = "ahmedabad", horizonDay = 1, customLat = null, customLon = null) {
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

    geojsonLayer = L.geoJSON(geojsonData, {
      style: function (feature) {
        const risk = feature.properties.heat_risk_score || 0;
        return {
          fillColor: getColorByRisk(risk),
          weight: 2,
          opacity: 0.9,
          color: '#ffffff',
          dashArray: '3',
          fillOpacity: 0.55
        };
      },
      onEachFeature: function (feature, layer) {
        const p = feature.properties;
        const d = p.demographics || {};
        
        const popupContent = `
          <div style="font-family: 'Inter', sans-serif; font-size: 13px; min-width: 220px;">
            <h4 style="margin: 0 0 6px 0; color: #0284c7; font-size: 14px;">${p.ward_name}</h4>
            <div style="margin-bottom: 6px;">
              <strong>Heat-Health Risk:</strong> <span style="color: ${p.alert_color}; font-weight: bold;">${p.heat_risk_score} / 100 (${p.alert_level})</span>
            </div>
            <hr style="border-color: #cbd5e1; margin: 4px 0;">
            <div style="font-size: 11.5px; color: #334155; line-height: 1.4;">
              <div><strong>UTCI:</strong> ${p.utci_val}°C (${p.utci_category})</div>
              <div><strong>WBGT:</strong> ${p.wbgt_val}°C (${p.wbgt_risk})</div>
              <div><strong>Elderly (60+):</strong> ${d.pop_elderly_60plus?.toLocaleString() || 'N/A'} (${d.elderly_percentage}%)</div>
              <div><strong>Outdoor Workers:</strong> ${d.workers_outdoor?.toLocaleString() || 'N/A'} (${d.outdoor_worker_percentage}%)</div>
              <div><strong>Pop Density:</strong> ${Math.round(d.pop_density_per_sqkm)?.toLocaleString() || 'N/A'} /km²</div>
            </div>
          </div>
        `;
        layer.bindPopup(popupContent);

        layer.on({
          mouseover: function (e) {
            const l = e.target;
            l.setStyle({
              weight: 3,
              color: '#0284c7',
              fillOpacity: 0.75
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
      mapInstance.fitBounds(geojsonLayer.getBounds());
    }

  } catch (err) {
    console.error("GIS Error:", err);
  }
}
