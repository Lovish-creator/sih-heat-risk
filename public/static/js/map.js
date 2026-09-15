/**
 * SIH26083 GIS Leaflet Controller & Decision-Support Drawer.
 * High-performance spatial choropleth with multi-layer basemaps (OSM, Satellite, Dark Disaster).
 * Ministry of Earth Sciences (MoES) / NCMRWF Tier 1 Prototype.
 */

let mapInstance = null;
let geojsonLayer = null;
let userGpsMarker = null;
let layerControl = null;
let wardLayersMap = {};
let activeSelectedLayer = null;

function getColorByRisk(riskScore) {
  if (riskScore >= 75.0) return "#ef4444"; // Red: Extreme / Emergency
  if (riskScore >= 50.0) return "#f97316"; // Orange: Warning / Severe
  if (riskScore >= 25.0) return "#f59e0b"; // Yellow: Caution / Moderate
  return "#10b981"; // Green: Normal / Low
}

function initMap(centerLat = 30.14505, centerLon = 74.19566, zoomLevel = 12) {
  const mapContainer = document.getElementById("map");
  if (!mapContainer || typeof L === "undefined") return null;

  if (mapInstance) {
    try {
      mapInstance.remove();
    } catch (e) {}
    mapInstance = null;
  }

  try {
    mapInstance = L.map('map', {
      center: [centerLat, centerLon],
      zoom: zoomLevel,
      zoomControl: true,
      dragging: true,
      scrollWheelZoom: true,
      touchZoom: true,
      doubleClickZoom: true,
      tap: false
    });

    // 1. OpenStreetMap Standard
    const osmStreets = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    // 2. Esri World Imagery
    const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: 'Tiles &copy; Esri'
    });

    // 3. CartoDB Dark Matter
    const cartoDark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://carto.com/">CARTO</a>'
    });

    osmStreets.addTo(mapInstance);

    const baseMaps = {
      "🗺️ Real Street Map (OSM)": osmStreets,
      "🛰️ Satellite View (Esri High-Res)": esriSatellite,
      "🌙 Dark Disaster Theme (CartoDB)": cartoDark
    };

    layerControl = L.control.layers(baseMaps, null, { position: 'topright' }).addTo(mapInstance);

    mapInstance.on('click', async (e) => {
      if (e.originalEvent && e.originalEvent._stopped) return;
      const lat = e.latlng.lat;
      const lon = e.latlng.lng;
      if (typeof handleMapClickLocation === "function") {
        await handleMapClickLocation(lat, lon);
      }
    });

    return mapInstance;
  } catch (err) {
    console.error("Leaflet initMap error:", err);
    return null;
  }
}

function setUserLocationMarker(lat, lon, label = "Selected Location", draggable = true) {
  if (typeof L === "undefined") return;
  if (!mapInstance) {
    initMap(lat, lon, 12);
  }
  if (!mapInstance) return;

  if (userGpsMarker && mapInstance) {
    try { mapInstance.removeLayer(userGpsMarker); } catch (e) {}
  }

  const pulseIcon = L.divIcon({
    className: 'custom-gps-icon',
    html: `<div class="user-gps-pulse" style="background: #38bdf8; border-radius: 50%; height: 14px; width: 14px; box-shadow: 0 0 10px #38bdf8; border: 2px solid white;"></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10]
  });

  userGpsMarker = L.marker([lat, lon], {
    icon: pulseIcon,
    draggable: draggable
  }).addTo(mapInstance);

  userGpsMarker.bindPopup(`
    <div style="font-family: 'Inter', sans-serif; font-size: 13px; color: #0f172a;">
      <strong style="color: #0284c7;">📍 ${label}</strong>
      <div style="font-size: 11px; color: #475569; margin-top: 2px;">
        Lat: ${lat.toFixed(4)}, Lon: ${lon.toFixed(4)}
      </div>
      <div style="font-size: 10.5px; color: #059669; margin-top: 4px;">
        💡 Drag marker or click anywhere to reposition analysis
      </div>
    </div>
  `);

  userGpsMarker.on('dragend', async (e) => {
    const newPos = e.target.getLatLng();
    if (typeof handleMapClickLocation === "function") {
      await handleMapClickLocation(newPos.lat, newPos.lng);
    }
  });
}

async function loadWardRiskLayer(cityId = "abohar", horizonDay = 1, customLat = null, customLon = null) {
  if (typeof L === "undefined") return;
  if (!mapInstance) {
    initMap();
    if (!mapInstance) return;
  }

  try {
    const geojsonData = await ApiClient.getMapRiskGeoJSON(horizonDay, {
      city: customLat === null ? cityId : undefined,
      lat: customLat !== null ? customLat : undefined,
      lon: customLon !== null ? customLon : undefined
    });

    if (geojsonLayer && mapInstance) {
      try { mapInstance.removeLayer(geojsonLayer); } catch (e) {}
    }

    wardLayersMap = {};

    geojsonLayer = L.geoJSON(geojsonData, {
      style: function (feature) {
        const risk = feature.properties.heat_risk_score !== undefined ? feature.properties.heat_risk_score : 0;
        return {
          fillColor: getColorByRisk(risk),
          weight: 1.8,
          opacity: 0.95,
          color: '#ffffff',
          dashArray: '2',
          fillOpacity: 0.65
        };
      },
      onEachFeature: function (feature, layer) {
        const p = feature.properties;
        const wNum = p.ward_number || p.id || 'N/A';
        const wName = p.ward_name || `Ward ${wNum}`;
        const risk = p.heat_risk_score !== undefined ? p.heat_risk_score.toFixed(1) : '--';
        const alertLvl = p.alert_level || 'NORMAL';
        const alertCol = p.alert_color || getColorByRisk(p.heat_risk_score || 0);

        wardLayersMap[wNum] = layer;

        layer.bindTooltip(`
          <div style="font-family: 'Inter', sans-serif; font-size: 12px; line-height: 1.35;">
            <strong style="color: #38bdf8;">${wName}</strong><br/>
            <span style="display: inline-block; background-color: ${alertCol}; color: ${alertLvl === 'CAUTION' ? '#000' : '#fff'}; font-weight: 800; font-size: 10px; padding: 1px 5px; border-radius: 3px; margin-top: 2px;">
              ${risk} / 100 (${alertLvl})
            </span>
          </div>
        `, { sticky: true, className: 'leaflet-custom-tooltip' });

        layer.on({
          mouseover: function (e) {
            const target = e.target;
            target.setStyle({ weight: 3.5, color: '#f8fafc', fillOpacity: 0.85 });
            target.bringToFront();
          },
          mouseout: function (e) {
            if (activeSelectedLayer !== e.target) {
              geojsonLayer.resetStyle(e.target);
            }
          },
          click: function (e) {
            L.DomEvent.stopPropagation(e);
            if (activeSelectedLayer) {
              geojsonLayer.resetStyle(activeSelectedLayer);
            }
            activeSelectedLayer = e.target;
            activeSelectedLayer.setStyle({ weight: 4.5, color: '#38bdf8', fillOpacity: 0.95 });
            openDecisionDrawer(feature.properties);
          }
        });
      }
    }).addTo(mapInstance);

    if (geojsonLayer.getLayers().length > 0) {
      mapInstance.fitBounds(geojsonLayer.getBounds(), { padding: [30, 30], maxZoom: 14 });
    }

    // Auto-select and display top hotspot ward in the Decision Support Drawer
    if (geojsonData && geojsonData.features && geojsonData.features.length > 0) {
      const topFeature = [...geojsonData.features].sort((a, b) => (b.properties?.heat_risk_score || 0) - (a.properties?.heat_risk_score || 0))[0];
      if (topFeature && topFeature.properties) {
        openDecisionDrawer(topFeature.properties);
      }
    }

  } catch (err) {
    console.error("GIS ward choropleth load error:", err);
  }
}

function openDecisionDrawer(props) {
  const drawer = document.getElementById("decisionDrawer");
  if (!drawer || !props) return;

  const wNum = props.ward_number || 1;
  const wName = props.ward_name || `Ward ${wNum}`;
  const risk = props.heat_risk_score !== undefined ? Number(props.heat_risk_score).toFixed(1) : '--';
  const alertLvl = props.alert_level || (props.heat_risk_score >= 75 ? 'EMERGENCY' : props.heat_risk_score >= 50 ? 'WARNING' : props.heat_risk_score >= 25 ? 'CAUTION' : 'NORMAL');
  const alertColor = props.alert_color || getColorByRisk(props.heat_risk_score || 0);

  const d = props.demographics || {};
  const wx = props.local_weather || {};

  const bodyEl = document.getElementById("drawerWardBody") || drawer;
  if (bodyEl) {
    bodyEl.innerHTML = `
      <div class="drawer-header" style="margin-bottom: 0.75rem; padding-bottom: 0.6rem; border-bottom: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <h3 style="font-size: 1.15rem; font-weight: 800; color: #38bdf8; margin: 0;">${wName}</h3>
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 2px;">
            ${props.city_name || 'Municipal Area'} &bull; ${props.zone_name || 'Urban Zone'}
          </div>
        </div>
        <span style="background-color: ${alertColor}; color: ${alertLvl === 'CAUTION' || alertLvl === 'YELLOW' ? '#000' : '#fff'}; font-weight: 800; font-size: 0.75rem; padding: 3px 8px; border-radius: var(--radius-sm); text-transform: uppercase;">
          ${alertLvl}
        </span>
      </div>

      <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid var(--border-subtle); padding: 0.75rem; border-radius: var(--radius-md); margin-bottom: 0.85rem; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <span style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Relative Heat-Health Risk</span>
          <div style="font-size: 1.75rem; font-weight: 900; color: #f8fafc; line-height: 1.1;">
            ${risk} <span style="font-size: 0.95rem; color: var(--text-muted); font-weight: 500;">/ 100</span>
          </div>
        </div>
        <div style="text-align: right; font-size: 0.72rem; color: #34d399;">
          <span>⚡ Live Evaluated</span><br/>
          <span style="color: var(--text-muted);">Hazard + Vulnerability</span>
        </div>
      </div>

      <div class="drawer-section-heading" style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.4rem;">🌡️ Biometeorology & Microclimate</div>
      <div style="display: flex; flex-direction: column; gap: 0.45rem; font-size: 0.8rem; margin-bottom: 0.85rem; background: rgba(0,0,0,0.2); padding: 0.6rem; border-radius: var(--radius-sm); border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">NOAA Heat Index:</span>
          <strong style="color: #fbbf24;">${props.heat_index_val !== undefined ? Number(props.heat_index_val).toFixed(1) + '°C' : '--°C'}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Physiological UTCI:</span>
          <strong style="color: #f97316;">${props.utci_val !== undefined ? Number(props.utci_val).toFixed(1) + '°C' : '--°C'} <span style="font-size: 0.72rem; color: var(--text-muted);">(${props.utci_category || 'Stress'})</span></strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Occupational WBGT:</span>
          <strong style="color: #38bdf8;">${props.wbgt_val !== undefined ? Number(props.wbgt_val).toFixed(1) + '°C' : '--°C'} <span style="font-size: 0.72rem; color: var(--text-muted);">(${props.wbgt_risk || 'Caution'})</span></strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Local Microclimate Temp:</span>
          <strong style="color: #f8fafc;">${wx.temp_c !== undefined ? Number(wx.temp_c).toFixed(1) + '°C' : '--°C'} <span style="color: #ef4444; font-size: 0.72rem;">(${props.uhi_delta_c >= 0 ? '+' : ''}${props.uhi_delta_c || 0.0}°C UHI)</span></strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Relative Humidity / Wind:</span>
          <strong style="color: #e2e8f0;">${wx.relative_humidity_pct !== undefined ? Math.round(wx.relative_humidity_pct) + '%' : '--%'} &bull; ${wx.wind_speed_10m_m_s !== undefined ? Number(wx.wind_speed_10m_m_s).toFixed(1) + ' m/s' : '--'}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Urban Typology (LCZ):</span>
          <strong style="color: #a78bfa;">${props.lcz_class || 'LCZ 3 Compact Low-Rise'}</strong>
        </div>
      </div>

      <div class="drawer-section-heading" style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.4rem;">👥 Demographics (Census 2011 PCA)</div>
      <div style="display: flex; flex-direction: column; gap: 0.45rem; font-size: 0.8rem; margin-bottom: 0.85rem; background: rgba(0,0,0,0.2); padding: 0.6rem; border-radius: var(--radius-sm); border: 1px solid rgba(255,255,255,0.05);">
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Elderly (Age 60+):</span>
          <strong style="color: #f8fafc;">${d.elderly_percentage !== undefined ? Number(d.elderly_percentage).toFixed(1) + '%' : '--%'} <span style="font-size: 0.72rem; color: var(--text-muted);">(${d.pop_elderly_60plus !== undefined ? Number(d.pop_elderly_60plus).toLocaleString() : '--'})</span></strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Outdoor Laborers:</span>
          <strong style="color: #f8fafc;">${d.outdoor_worker_percentage !== undefined ? Number(d.outdoor_worker_percentage).toFixed(1) + '%' : '--%'} <span style="font-size: 0.72rem; color: var(--text-muted);">(${d.workers_outdoor !== undefined ? Number(d.workers_outdoor).toLocaleString() : '--'})</span></strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Population Density:</span>
          <strong style="color: #f8fafc;">${d.pop_density_per_sqkm !== undefined ? Math.round(d.pop_density_per_sqkm).toLocaleString() + ' /km²' : '-- /km²'}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Total Ward Population:</span>
          <strong style="color: #f8fafc;">${d.tot_pop !== undefined ? Number(d.tot_pop).toLocaleString() : '--'}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 2px 0;">
          <span style="color: var(--text-secondary);">Spatial Extent:</span>
          <strong style="color: #f8fafc;">${d.area_sqkm || '--'} km² (${d.area_hectares || '--'} ha)</strong>
        </div>
      </div>

      <div style="background-color: var(--bg-card-hover); padding: 0.65rem 0.75rem; border-radius: var(--radius-md); border-left: 3px solid ${alertColor}; margin-bottom: 0.75rem;">
        <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; margin-bottom: 0.25rem;">Why is this unit elevated risk?</div>
        <p style="font-size: 0.78rem; color: #f1f5f9; line-height: 1.35; margin: 0;">
          ${props.action_summary || 'Elevated risk driven by combination of ambient microclimatic thermal load and vulnerable demographics.'}
        </p>
      </div>

      <div style="font-size: 0.7rem; color: var(--text-muted); padding-top: 0.4rem; border-top: 1px solid var(--border-subtle);">
        📌 <strong>Data Provenance:</strong> ${props.provenance?.geometry_source || 'Official Municipal Delimitation'} &amp; ${props.provenance?.demographics_source || 'Census 2011 PCA'}.
      </div>
    `;
  }

  drawer.classList.add("active");
}

function closeDecisionDrawer() {
  const drawer = document.getElementById("decisionDrawer");
  if (drawer) drawer.classList.remove("active");
  if (activeSelectedLayer && geojsonLayer) {
    geojsonLayer.resetStyle(activeSelectedLayer);
    activeSelectedLayer = null;
  }
}

window.initMap = initMap;
window.setUserLocationMarker = setUserLocationMarker;
window.loadWardRiskLayer = loadWardRiskLayer;
window.openDecisionDrawer = openDecisionDrawer;
window.closeDecisionDrawer = closeDecisionDrawer;
window.getColorByRisk = getColorByRisk;
