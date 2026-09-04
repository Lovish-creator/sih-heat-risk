/**
 * SIH26083 GIS Leaflet Choropleth Map Controller.
 */

let mapInstance = null;
let geojsonLayer = null;

function getColorByRisk(riskScore) {
  if (riskScore > 75.0) return "#ef4444"; // Red
  if (riskScore > 50.0) return "#f97316"; // Orange
  if (riskScore > 25.0) return "#f59e0b"; // Yellow
  return "#10b981"; // Green
}

function initMap(centerLat = 23.0225, centerLon = 72.5714, zoomLevel = 12) {
  if (mapInstance) {
    mapInstance.remove();
  }

  mapInstance = L.map('map', {
    center: [centerLat, centerLon],
    zoom: zoomLevel,
    zoomControl: true
  });

  // Dark CartoDB Tile Layer
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://carto.com/">CARTO</a> | &copy; OpenStreetMap',
    maxZoom: 18
  }).addTo(mapInstance);

  return mapInstance;
}

async function loadWardRiskLayer(cityId = "ahmedabad", horizonDay = 1) {
  if (!mapInstance) {
    initMap();
  }

  try {
    const res = await fetch(`/api/v1/map/risk?city=${cityId}&day=${horizonDay}`);
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
          opacity: 1,
          color: '#ffffff',
          dashArray: '3',
          fillOpacity: 0.65
        };
      },
      onEachFeature: function (feature, layer) {
        const p = feature.properties;
        const d = p.demographics || {};
        
        const popupContent = `
          <div style="font-family: 'Inter', sans-serif; font-size: 13px; min-width: 200px;">
            <h4 style="margin: 0 0 6px 0; color: #38bdf8; font-size: 14px;">${p.ward_name} (${p.zone_name})</h4>
            <div style="margin-bottom: 6px;">
              <strong>Heat-Health Risk:</strong> <span style="color: ${p.alert_color}; font-weight: bold;">${p.heat_risk_score} / 100 (${p.alert_level})</span>
            </div>
            <hr style="border-color: #475569; margin: 4px 0;">
            <div style="font-size: 11.5px; color: #cbd5e1; line-height: 1.4;">
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
              color: '#38bdf8',
              fillOpacity: 0.85
            });
            l.bringToFront();
          },
          mouseout: function (e) {
            geojsonLayer.resetStyle(e.target);
          }
        });
      }
    }).addTo(mapInstance);

    // Fit map bounds to polygons
    mapInstance.fitBounds(geojsonLayer.getBounds());

  } catch (err) {
    console.error("GIS Error:", err);
  }
}
