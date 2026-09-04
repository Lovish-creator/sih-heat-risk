# Novelty & Differentiation Strategy

Treating novelty as a design problem, this document articulates how SIH26083 advances beyond existing operational dashboards by coupling multi-parameter biometeorology with demographic vulnerability and actionable ward-level risk attribution.

## Comparative Innovation Matrix

| Existing Capability | Existing Systems / Current State | Critical Limitation | SIH26083 Integrated Solution |
|:---|:---|:---|:---|
| **Heatwave Warning Trigger** | IMD Synoptic District Bulletins | Relies primarily on absolute dry-bulb air temperature ($T_a \ge 40^\circ\text{C}$ or $+4.5^\circ\text{C}$ departure from normal). Ignores humidity, wind speed, and direct radiant heat load. | Computes physiological **Universal Thermal Climate Index (UTCI)** and **Wet Bulb Globe Temperature (WBGT)** incorporating temperature, humidity, 10m wind, and shortwave solar irradiance. |
| **Exposure Metric** | Experimental Heat Index (HI) web maps | Heat Index only models shaded conditions without wind or direct solar radiation, assuming fixed metabolic rates. | Dual physiological framework: UTCI for ambient human energy balance ($T_{mrt}$, $v_{10}$) + NIOSH WBGT for occupational outdoor labor strain. |
| **Vulnerability Integration** | Static city-wide Heat Action Plans (HAPs) | City-wide blanket alerts treat all neighborhoods identically, regardless of age demographics or occupational composition. | Micro-spatial **Ward-Level Risk Attribution** fusing environmental hazard with Census 2011 demographic vulnerability (elderly $60+$ ratio, outdoor worker ratio, population density). |
| **Forecast Anticipation** | 24-48 hour synoptic station alerts | Citizens and outdoor workers receive minimal actionable lead time for labor rescheduling or shelter preparation. | Modular **5-Day Horizon Architecture (D+1 to D+5)** computing forward thermal indices and cumulative duration exposure penalties. |
| **Public Health Action** | Generic public advisories ("Drink water, stay indoors") | Advisories are one-size-fits-all and lack operational thresholds for construction sites, gig workers, or municipal cooling logistics. | **Multi-Persona Actionable Advisory Engine** delivering tailored, evidence-based recommendations mapped directly to NCDC 2024 and WHO guidelines for (1) Citizens, (2) Outdoor Workers (NIOSH work-rest cycles), and (3) Municipal Authorities. |
| **Health Impact Representation** | Uncalibrated claims or unscientific death prediction | Either complete absence of health risk metrics or ungrounded claims of exact mortality counts. | Transparent **Relative Heat-Health Risk Score (0–100)** with clear alert levels (Green, Yellow, Orange, Red) and documented scientific provenance. |

---

## What We Deliberately DO NOT Claim
1. We **do not claim** to predict exact mortality or hospital admission counts without access to protected hospital telemetry (Tier-3).
2. We **do not claim** that coarse meteorological grids ($\sim 50\text{ km}$) constitute micro-scale ward-resolution meteorology; rather, we provide **ward-level risk attribution** by combining the regional environmental hazard with localized demographic vulnerability.
3. We **do not claim** to use "black-box AI" where transparent physical biometeorological equations and multi-criteria risk scoring provide superior interpretability and trust for public disaster management.
