/**
 * SIH26083 Centralized API Client.
 * Communicates with FastAPI backend for Extreme Heat Early Warning & Decision Support.
 * Ministry of Earth Sciences (MoES) / NCMRWF Prototype.
 */

const API_CONFIG = {
  BASE_URL: "",
  TIMEOUT_MS: 12000,
  CACHE_TTL_MS: 120000 // 2-minute memory cache
};

const _apiCache = new Map();

class ApiClient {
  static async request(endpoint, options = {}) {
    const cacheKey = endpoint;
    const now = Date.now();

    if (!options.method || options.method === "GET") {
      const cached = _apiCache.get(cacheKey);
      if (cached && (now - cached.timestamp < API_CONFIG.CACHE_TTL_MS)) {
        return cached.data;
      }
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), options.timeout || API_CONFIG.TIMEOUT_MS);

    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
        ...options,
        signal: controller.signal,
        headers: {
          "Accept": "application/json",
          ...(options.headers || {})
        }
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorBody = await response.text();
        let message = `API Error ${response.status}: ${response.statusText}`;
        try {
          const parsed = JSON.parse(errorBody);
          if (parsed.detail) message = parsed.detail;
        } catch (e) {}
        throw new Error(message);
      }

      const data = await response.json();

      if (!options.method || options.method === "GET") {
        _apiCache.set(cacheKey, { timestamp: now, data });
      }

      return data;
    } catch (err) {
      clearTimeout(timeoutId);
      if (err.name === "AbortError") {
        throw new Error("Request timed out while contacting meteorological service.");
      }
      throw err;
    }
  }

  static clearCache() {
    _apiCache.clear();
  }

  static _buildParams(params = {}) {
    const q = new URLSearchParams();
    if (params.city) q.set("city", params.city);
    if (params.lat !== undefined && params.lat !== null) q.set("lat", params.lat);
    if (params.lon !== undefined && params.lon !== null) q.set("lon", params.lon);
    return q.toString();
  }

  static async getCurrentWeather(params = {}) {
    const qs = this._buildParams(params);
    return this.request(`/api/v1/weather/current?${qs}`);
  }

  static async getThermalCurrent(params = {}) {
    const qs = this._buildParams(params);
    return this.request(`/api/v1/thermal/current?${qs}`);
  }

  static async getRiskCurrent(params = {}) {
    const qs = this._buildParams(params);
    return this.request(`/api/v1/risk/current?${qs}`);
  }

  static async getForecast(params = {}) {
    const qs = this._buildParams(params);
    return this.request(`/api/v1/weather/forecast?${qs}`);
  }

  static async getThermalForecast(params = {}) {
    const qs = this._buildParams(params);
    return this.request(`/api/v1/thermal/forecast?${qs}`);
  }

  static async getRiskForecast(params = {}) {
    const qs = this._buildParams(params);
    return this.request(`/api/v1/risk/forecast?${qs}`);
  }

  static async getHourlyWeather(params = {}) {
    const q = new URLSearchParams();
    q.set("hours", params.hours || 24);
    if (params.city) q.set("city", params.city);
    if (params.lat !== undefined && params.lat !== null) q.set("lat", params.lat);
    if (params.lon !== undefined && params.lon !== null) q.set("lon", params.lon);
    return this.request(`/api/v1/weather/hourly?${q.toString()}`);
  }

  static async getAdvisories(params = {}) {
    const qs = this._buildParams(params);
    return this.request(`/api/v1/advisory?${qs}`);
  }

  static async getVulnerability(params = {}) {
    const qs = this._buildParams(params);
    return this.request(`/api/v1/vulnerability?${qs}`);
  }

  static async getMapRiskGeoJSON(day = 1, params = {}) {
    const q = new URLSearchParams();
    q.set("day", day);
    if (params.city) q.set("city", params.city);
    if (params.lat !== undefined && params.lat !== null) q.set("lat", params.lat);
    if (params.lon !== undefined && params.lon !== null) q.set("lon", params.lon);
    return this.request(`/api/v1/map/risk?${q.toString()}`);
  }

  static async getWardsSummary(day = 1, params = {}) {
    const q = new URLSearchParams();
    q.set("day", day);
    if (params.city) q.set("city", params.city);
    if (params.lat !== undefined && params.lat !== null) q.set("lat", params.lat);
    if (params.lon !== undefined && params.lon !== null) q.set("lon", params.lon);
    return this.request(`/api/v1/wards/summary?${q.toString()}`);
  }

  static async getCapAlert(params = {}) {
    const qs = this._buildParams(params);
    return this.request(`/api/v1/alerts/cap/json?${qs}`);
  }

  static async searchLocations(query, limit = 8) {
    if (!query || query.trim().length < 2) return { query: "", results: [] };
    const q = new URLSearchParams({ q: query.trim(), limit });
    return this.request(`/api/v1/geocode/search?${q.toString()}`);
  }

  static async reverseGeocode(lat, lon) {
    const q = new URLSearchParams({ lat, lon });
    return this.request(`/api/v1/geocode/reverse?${q.toString()}`);
  }

  static async getIpLocation() {
    return this.request(`/api/v1/geocode/ip`);
  }

  static async getDataFreshness() {
    return this.request(`/api/v1/data-freshness`);
  }

  static async getProvenanceSources() {
    return this.request(`/api/v1/provenance/sources`);
  }
}

window.ApiClient = ApiClient;
