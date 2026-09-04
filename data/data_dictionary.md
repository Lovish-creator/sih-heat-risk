# SIH26083 - Data Dictionary

This data dictionary formally describes every meteorological, physiological, demographic, and risk variable processed within the pipeline.

| Variable Name | Source ID | Unit | Physical / Domain Meaning | Used By | Transformation / Formula |
|:---|:---|:---|:---|:---|:---|
| `T2M` | SRC-02 | $^\circ\text{C}$ | Dry bulb air temperature at 2 meters above ground level | UTCI, WBGT, Heat Index, Hazard Score | Extracted directly from NASA POWER / IMD; verified within $[-10, 60]^\circ\text{C}$ |
| `RH2M` | SRC-02 | $\%$ | Relative humidity at 2 meters above ground level ($0\text{--}100\%$) | UTCI, WBGT, Heat Index, Vapor Pressure | Clamped to $[0.0, 100.0]\%$; used to derive actual vapor pressure $e$ (hPa) |
| `WS10M` | SRC-02 | $\text{m/s}$ | Wind speed at 10 meters above ground level | UTCI Engine | Clamped to $[0.5, 17.0]\text{ m/s}$ (UTCI operational polynomial boundary) |
| `WS2M` | SRC-02 | $\text{m/s}$ | Wind speed at 2 meters above ground level | WBGT Black Globe Calculation | Estimated via 1/7th power law $v_2 = v_{10} \times (2/10)^{0.2}$ if only 10m wind is available |
| `ALLSKY_SFC_SW_DWN` | SRC-02 | $\text{W/m}^2$ | All Sky Surface Shortwave Downward Irradiance (Solar Radiation) | UTCI Mean Radiant Temp ($T_{mrt}$), WBGT Black Globe ($T_g$) | Converted to radiant flux; used in energy balance equations for outdoor solar load |
| `e_hPa` | Calculated | $\text{hPa}$ | Water vapor pressure | UTCI Polynomial | Magnus-Tetens formulation: $e = 6.112 \times \exp\left(\frac{17.67 \times T}{T + 243.5}\right) \times \frac{RH}{100}$ |
| `T_mrt` | Calculated | $^\circ\text{C}$ | Mean Radiant Temperature (surrounding radiative field) | UTCI Polynomial | Stefan-Boltzmann approximation: $T_{mrt} = \left( T_a^4 + \frac{f_p \cdot \alpha \cdot S}{\epsilon \cdot \sigma} \right)^{0.25} - 273.15$ |
| `UTCI` | SRC-06 | $^\circ\text{C}$ | Universal Thermal Climate Index equivalent temperature | Thermal Hazard Score, Citizen Advisory | Evaluated via Bröde et al. (2012) 6th-order polynomial with 240 regression coefficients |
| `WBGT_outdoor` | SRC-07 | $^\circ\text{C}$ | Outdoor Wet Bulb Globe Temperature | Occupational Hazard Score, Worker Rest Regimens | $WBGT = 0.7 \cdot T_{nw} + 0.2 \cdot T_g + 0.1 \cdot T_a$ (Stull psychrometric $T_{nw}$ & radiation-adjusted $T_g$) |
| `Heat_Index` | NOAA/NWS | $^\circ\text{C}$ | Rothfusz Heat Index ("Feels Like" temperature) | General Public Hazard Metric | Rothfusz 9-term polynomial in Fahrenheit, converted to Celsius, with low/high RH adjustments |
| `Hazard_Score` | Engine | $0\text{--}100$ | Dimensionless Normalized Environmental Thermal Stress | Risk Engine | Weighted combination: $0.60 \cdot \text{Norm}(UTCI) + 0.25 \cdot \text{Norm}(WBGT) + 0.15 \cdot \text{Norm}(HI)$ |
| `tot_pop` | SRC-03 | Count | Total Census ward population (2011 baseline) | Vulnerability Density | Ward raw count from Census Primary Census Abstract (PCA) |
| `pop_elderly_60plus` | SRC-03 | Count | Population aged 60 years and above | Vulnerability Engine | Percentage elderly: $\frac{\text{pop\_elderly\_60plus}}{\text{tot\_pop}} \times 100$ |
| `workers_outdoor` | SRC-03 | Count | Main & Marginal agricultural laborers, construction, and street vendors | Vulnerability Engine | Percentage outdoor workers: $\frac{\text{workers\_outdoor}}{\text{tot\_pop}} \times 100$ |
| `pop_density_sqkm` | SRC-03 / SRC-11 | Persons/$\text{km}^2$ | Ward population divided by ward geometric polygon area | Vulnerability Engine | Ward population density: $\frac{\text{tot\_pop}}{\text{Area}(\text{km}^2)}$ |
| `Vulnerability_Score` | Engine | $0\text{--}100$ | Multi-criteria Demographic Sensitivity Index | Risk Engine | $0.40 \cdot \text{Norm}(Elderly\%) + 0.35 \cdot \text{Norm}(Worker\%) + 0.25 \cdot \text{Norm}(Density)$ |
| `Heat_Risk_Score` | Engine | $0\text{--}100$ | Composite Relative Heat-Health Risk Index | GIS Ward Attribution, Advisories, Alerts | $0.55 \cdot \text{Hazard\_Score} + 0.30 \cdot \text{Vulnerability\_Score} + 0.15 \cdot \text{Duration\_Factor}$ |
| `Alert_Level` | Engine | Enum | 4-Tier Warning Category | UI, SMS/Alert Simulation | Categorized as `GREEN` (0-25), `YELLOW` (26-50), `ORANGE` (51-75), `RED` (76-100) |
