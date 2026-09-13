# SIH 2026 PS26083 ? Health Data Readiness and Epidemiological Integration Specification

**Document Version:** 1.0.0  
**Target Domain:** Biometeorological Exposure vs. Human Health Outcomes  
**Ministry Alignment:** Ministry of Earth Sciences (MoES) / Ministry of Health and Family Welfare (MoHFW) / National Centre for Disease Control (NCDC)  

---

## 1. Executive Summary & Ethical Directive

A fundamental tenet of scientific honesty in the **ThermoShield India** platform is:
> **Never fabricate health data, and never train machine learning models using synthetic risk scores as fake health labels.**

While meteorological and satellite irradiance data are openly accessible in real-time (via Open-Meteo, NASA POWER, and IMD), empirical health outcome data (hospital admissions, heatstroke morbidity, emergency room visits, and all-cause excess mortality) are tightly governed under statutory privacy frameworks and health surveillance systems in India.

This document outlines the architectural readiness of the platform to ingest, validate, and link genuine health outcome datasets when official partnerships (e.g., with IDSP, HMIS, or municipal health departments) are established.

---

## 2. Required Health Datasets & Variables

To calibrate and validate empirical heat-health thresholds beyond biometeorological physics (UTCI/WBGT), the following variables are specified:

| Variable | Clinical / Statistical Definition | Minimum Geographic Unit | Minimum Time Unit | Ideal National Source |
|---|---|---|---|---|
| **Heat-Related Morbidity (HRI)** | Confirmed cases of heat exhaustion, heat syncope, and heatstroke (ICD-10 codes: T67.0 to T67.9). | Municipal Ward / PHC Catchment | Daily | Integrated Disease Surveillance Programme (IDSP) / NAP-HRI Portal |
| **Emergency Department Footfall** | All-cause non-trauma daily emergency room admissions. | District Hospital / Medical College | Daily | Health Management Information System (HMIS) / State Health Dashboards |
| **All-Cause Daily Mortality** | Total registered deaths across municipal registration units. | Municipal Ward / Zone | Daily | Civil Registration System (CRS) / Municipal Vital Statistics Registrars |
| **Cardiovascular & Respiratory Admissions** | Acute exacerbations of ischemic heart disease, COPD, and renal dysfunction during extreme heat episodes. | Hospital / Zone | Daily | Ayushman Bharat - PM-JAY Inpatient Records / Hospital EMRs |

---

## 3. Methodological Validation Framework: Why Pure Physics Must Precede ML

1. **Why ML Cannot Be Trained on Synthetic Labels:**
   - Training a gradient-boosted tree or deep neural network on a composite index calculated from temperature, humidity, and census data simply creates a distorted approximation of the deterministic formula itself.
   - It introduces zero new empirical information and creates a dangerous illusion of predictive intelligence.

2. **The Correct Epidemiological Methodology (DLNM):**
   - When genuine health time-series data become available, the platform is architected to apply **Distributed Lag Non-Linear Models (DLNM)**.
   - DLNM accounts for both the non-linear relationship between temperature/UTCI and health outcomes, and the delayed (lagged) mortality effect observed over 1 to 14 days following extreme thermal exposure.
   - This determines the **Minimum Mortality Temperature (MMT)** specific to Indian climatic zones (e.g., arid northwest vs. humid coastal).

---

## 4. Statutory Privacy, Anonymization & Security Guardrails

To comply with India's **Digital Personal Data Protection Act (DPDP 2023)** and **National Digital Health Mission (NDHM)** standards:
- **No Personally Identifiable Information (PII):** Health data ingested into the system must be aggregated at the ward/zone or district level. Individual patient names, Aadhaar numbers, and phone numbers are strictly prohibited.
- **K-Anonymity & Cell Suppression:** In spatial units where daily cases are fewer than 5, data suppression rules are applied to prevent individual re-identification.
- **Role-Based Access Control (RBAC):** Raw aggregated morbidity tables are restricted to authenticated public health authorities.

---

## 5. Future Extensibility & Database Schema

The database model `HealthRecordModel` (`health_records` table) is already scaffolded in SQLAlchemy to receive genuine partner data:
- `location_id` / `ward_id`
- `record_date`
- `heat_related_cases`
- `hospital_admissions`
- `mortality_count`
- `data_source`
- `source_year`
- `is_verified` (Boolean flag ensuring unverified data is quarantined).
