# Data Acquisition & Demographic Provenance Manual — Taapamigo (SIH26083)

This document provides complete, transparent, and authoritative instructions for acquiring and verifying demographic data from the Office of the Registrar General & Census Commissioner, India (ORGI / Ministry of Home Affairs).

---

## 1. Demographic Reality & Table Structure in Census of India 2011

When building human thermal stress and vulnerability models for India, researchers and engineers must distinguish between different Census table series.

### 1.1 What is the Primary Census Abstract (PCA)?
The **Primary Census Abstract (PCA)** is the foundational district-, sub-district-, and village/ward-level abstract published by the Census Commissioner.
- **Official Portal:** [https://censusindia.gov.in/census.website/data/census-tables](https://censusindia.gov.in/census.website/data/census-tables) or Open Government Data (OGD) Portal [https://data.gov.in](https://data.gov.in).
- **Available PCA Fields:**
  - Total Population, Males, Females
  - Scheduled Castes (SC) and Scheduled Tribes (ST) populations
  - Children aged 0–6 (Persons, Males, Females)
  - Literates and Illiterates
  - Total Workers, Main Workers, Marginal Workers, Non-Workers
  - **Four Broad Industrial Categories of Workers:**
    1. Cultivators (CL)
    2. Agricultural Labourers (AL)
    3. Household Industry Workers (HHI)
    4. Other Workers (OW)
  - Area ($\text{km}^2$) and calculated Population Density.

### 1.2 Important Fact: The PCA Does NOT Contain Elderly (60+) Counts
- **Finding:** A common misconception is that age distributions are in the PCA. **The Census PCA does not record single-year or broad age groups beyond children 0–6.**
- **Where Elderly (60+) Data Actually Resides:**
  Age-specific population tables are published separately in the **C-Series (Social & Cultural Tables)**:
  - **Table C-13:** *"Single Year Age Returns by Residence and Sex"* (District level).
  - **Table C-14:** *"Five Year Age Group Data by Residence and Sex"* (District level, reporting Age Groups 60–64, 65–69, 70–74, 75–79, 80+).
- **Implication for Taapamigo:** Any district dataset claiming that age 60+ counts were extracted directly from the "Census 2011 PCA" was factually incorrect. In Taapamigo's prototype demographic files, elderly counts were derived from baseline state/district percentage estimates, and are now honestly flagged as `"data_quality": "estimated"`.

---

## 2. Definition & Limitations of the "Outdoor Worker" Proxy

In occupational heat stress standards (e.g., ISO 7243, NIOSH 2016), outdoor workers represent the primary demographic at risk of fatal heat exhaustion and heat stroke due to physical metabolic exertion under high solar irradiance.

### 2.1 The Census PCA Limitation
In the 2011 Census PCA, workers are grouped into only four broad buckets:
$$\text{Total Workers} = \text{Cultivators} + \text{Agricultural Labourers} + \text{Household Industry Workers} + \text{Other Workers}$$

- **Cultivators + Agricultural Labourers:** These can be identified as outdoor agricultural laborers.
- **Urban Outdoor Workers (Construction, Street Vendors, Delivery, Logistics, Brick Kilns):** In urban municipal wards, these workers are categorized under **"Other Workers"**, pooled together with indoor office workers, civil servants, and retail clerks. **The PCA cannot isolate construction or informal outdoor laborers from indoor workers.**
- **Taapamigo Proxy Definition:**
  Where direct sector surveys are unavailable, the outdoor worker metric in `data/sample/india_census_districts.json` represents an **estimated occupational exposure ratio** calibrated for each district's urban/rural mix, flagged as `"data_quality": "estimated"`.

---

## 3. Step-by-Step Manual Acquisition Instructions

To obtain the genuine government datasets without relying on automated scraping:

### Step A: Primary Census Abstract (PCA) — District Level
1. Navigate to the Census of India 2011 Official Table Repository:
   `https://censusindia.gov.in/census.website/data/census-tables`
2. Select Category: **"Primary Census Abstract (PCA)"** $\rightarrow$ **"PCA Data (Total/Rural/Urban)"**.
3. Download the state-wise Excel workbooks:
   - For example: `PCA_Total_Punjab.xlsx` or `PCA_Total_Gujarat.xlsx`.
4. Relevant columns:
   - Column `TOT_P`: Total Persons
   - Column `MAINWORK_P` + `MARGWORK_P`: Total Workers
   - Column `CL_P` + `AL_P`: Cultivators + Agricultural Labourers
   - Column `Area`: Total geographic area in $\text{km}^2$.

### Step B: C-Series Table C-14 (Five Year Age Group by Residence and Sex)
1. In the Census Table Repository, select Category: **"C-Series: Social and Cultural Tables"**.
2. Select **Table C-14**: *"Population in five year age-group by residence and sex"*.
3. Download the state/district workbook (e.g., `DDW-0000C-14.xlsx`).
4. Locate the target district row. Sum the population across age brackets:
   $$\text{Pop}_{60+} = \text{Age}_{60-64} + \text{Age}_{65-69} + \text{Age}_{70-74} + \text{Age}_{75-79} + \text{Age}_{80+}$$
5. Compute the genuine ratio:
   $$\text{Elderly Ratio} = \frac{\text{Pop}_{60+}}{\text{Total Population}}$$

### Step C: Municipal Ward Boundary Geometries (DataMeet)
1. Official boundaries released under open licenses are hosted by DataMeet Municipal Spatial Data:
   `https://github.com/datameet/Municipal_Spatial_Data`
2. Check `data/datameet_wards/manifest.json` for verified upstream URLs.
3. Note on Ahmedabad: The DataMeet file `Ahmedabad/Ward_office.geojson` provides point coordinates of ward administrative offices, not municipal ward boundary polygons. The 20-ward polygons in `data/sample/ahmedabad_wards.geojson` are illustrative delimitation units for prototype demonstration and are flagged accordingly.

---

## 4. Checksums of Raw Data Files (`data/raw/SHA256SUMS`)

When raw government files are placed in `data/raw/`, their cryptographic integrity is verified against `data/raw/SHA256SUMS`:

```bash
# Generate SHA256 checksums
sha256sum data/raw/* > data/raw/SHA256SUMS

# Verify integrity
sha256sum -c data/raw/SHA256SUMS
```
