# SIH26083 - Scientific Calculations, Mathematical Models & Derivations Reference

**Problem Statement:** SIH26083 - Extreme Heatwave Early Warning and Human Thermal Stress Index  
**Organization:** Ministry of Earth Sciences (MoES) / National Centre for Medium Range Weather Forecasting (NCMRWF)  
**Standard Compliance:** COST Action 730 (UTCI), ISO 7243 / NIOSH 2016 (WBGT), NOAA / NWS (Heat Index), Census of India 2011 Primary Census Abstract (PCA), IMD 4-Tier Warning System.

---

## 1. Universal Thermal Climate Index (UTCI)

### A. Scientific Basis & Concept
UTCI is defined as the equivalent ambient temperature (deg C) of an isothermal reference environment (RH = 50%, v10 = 0.5 m/s, Tmrt = Ta) that produces the exact same physiological dynamic response (core body temperature, mean skin temperature, sweat rate, skin wettedness) in the advanced multi-node Fiala thermo-physiological model as the actual outdoor environment.

### B. Input Physical Variables
1. Dry-bulb air temperature: Ta (deg C), valid within [-50, +50] deg C
2. Relative humidity: RH (%), valid within [0, 100]%
3. Wind speed at 10m height: v10 (m/s), valid within [0.5, 17.0] m/s
4. Mean radiant temperature difference: Delta_Tmrt = Tmrt - Ta (deg C), valid within [-30, +70] deg C
5. Water vapor pressure: e (hPa)

### C. Atmospheric Moisture (Magnus-Tetens Formulation)
Saturation Vapor Pressure:
    es(Ta) = 6.112 * exp((17.67 * Ta) / (Ta + 243.5))  [hPa]

Actual Water Vapor Pressure:
    e = es(Ta) * (RH / 100.0)  [hPa]

### D. Mean Radiant Temperature (Tmrt) via Outdoor Stefan-Boltzmann Radiation Flux
    Tmrt = [ (Ta + 273.15)^4 + (fp * alpha_k * S) / (epsilon_p * sigma) ]^0.25 - 273.15  [deg C]

Where:
- S: All-sky shortwave solar irradiance (W/m^2)
- fp = 0.28: Human body projection area factor (standing posture)
- alpha_k = 0.70: Human solar absorption coefficient (skin & summer clothing)
- epsilon_p = 0.97: Human body surface emissivity
- sigma = 5.670374e-8 W/(m^2 K^4): Stefan-Boltzmann physical constant

### E. The 6th-Order Brode Operational Polynomial
    UTCI(Ta, Delta_Tmrt, v10, e) = Ta + Offset(Ta, Delta_Tmrt, v10, e)

Offset Polynomial:
    Offset = (
        0.607562052 - 0.0227712343*Ta + 8.06470249e-4*Ta^2 - 1.54271372e-6*Ta^3
        - 3.25080447e-8*Ta^4 + 2.717732e-10*Ta^5 + 0.448553589*Delta_Tmrt
        - 3.60773681e-3*Ta*Delta_Tmrt + 2.16442583e-5*Ta^2*Delta_Tmrt + 9.40347118e-8*Ta^3*Delta_Tmrt
        - 1.00656308e-9*Ta^4*Delta_Tmrt - 2.24640824e-3*Delta_Tmrt^2 + 6.20807844e-5*Ta*Delta_Tmrt^2
        - 3.16136728e-7*Ta^2*Delta_Tmrt^2 + 2.61350473e-9*Ta^3*Delta_Tmrt^2 + 1.47983125e-5*Delta_Tmrt^3
        - 2.11514421e-7*Ta*Delta_Tmrt^3 + 2.01121004e-9*Ta^2*Delta_Tmrt^3 - 4.97398124e-8*Delta_Tmrt^4
        + 4.79006694e-10*Ta*Delta_Tmrt^4 + 6.39408766e-11*Delta_Tmrt^5 - 2.85620943*v10
        + 0.0984834802*Ta*v10 - 2.06141358e-3*Ta^2*v10 + 2.64023241e-5*Ta^3*v10
        - 1.5894151e-7*Ta^4*v10 - 4.75787685e-3*Delta_Tmrt*v10 + 4.03362994e-4*Ta*Delta_Tmrt*v10
        - 3.8878229e-6*Ta^2*Delta_Tmrt*v10 + 2.58230441e-8*Ta^3*Delta_Tmrt*v10 - 2.28510804e-5*Delta_Tmrt^2*v10
        + 1.09965939e-6*Ta*Delta_Tmrt^2*v10 - 7.87830387e-9*Ta^2*Delta_Tmrt^2*v10 + 3.8288544e-8*Delta_Tmrt^3*v10
        - 1.44187317e-9*Ta*Delta_Tmrt^3*v10 + 0.380507347*v10^2 - 0.0150157035*Ta*v10^2
        + 3.56515384e-4*Ta^2*v10^2 - 3.73286544e-6*Ta^3*v10^2 + 9.81676264e-4*Delta_Tmrt*v10^2
        - 4.579084e-5*Ta*Delta_Tmrt*v10^2 + 5.14107188e-7*Ta^2*Delta_Tmrt*v10^2 + 1.24977174e-6*Delta_Tmrt^2*v10^2
        - 6.13208034e-8*Ta*Delta_Tmrt^2*v10^2 - 0.0260333364*v10^3 + 1.08808166e-3*Ta*v10^3
        - 2.43474878e-5*Ta^2*v10^3 - 6.28383923e-5*Delta_Tmrt*v10^3 + 2.47794439e-6*Ta*Delta_Tmrt*v10^3
        + 7.03487493e-4*v10^4 - 2.88521854e-5*Ta*v10^4 + 0.0179009851*e
        + 6.85712781e-4*Ta*e - 3.78107204e-5*Ta^2*e + 8.43535262e-7*Ta^3*e
        - 7.68759111e-9*Ta^4*e + 1.05744577e-4*Delta_Tmrt*e - 7.9319928e-6*Ta*Delta_Tmrt*e
        + 1.39648967e-7*Ta^2*Delta_Tmrt*e - 1.37016003e-9*Ta^3*Delta_Tmrt*e - 4.56581883e-7*Delta_Tmrt^2*e
        + 1.7043531e-8*Ta*Delta_Tmrt^2*e - 8.49242932e-3*v10*e + 4.78519471e-4*Ta*v10*e
        - 1.22240854e-5*Ta^2*v10*e + 1.24598582e-7*Ta^3*v10*e - 3.50912722e-5*Delta_Tmrt*v10*e
        + 2.06418716e-6*Ta*Delta_Tmrt*v10*e + 8.43664584e-4*v10^2*e - 4.84382306e-5*Ta*v10^2*e
        + 9.47643608e-7*Ta^2*v10^2*e + 2.30237139e-6*Delta_Tmrt*v10^2*e - 2.70631994e-5*v10^3*e
        - 4.12034135e-5*e^2 + 3.88792866e-6*Ta*e^2 - 1.93760678e-7*Ta^2*e^2
        + 4.03061445e-9*Ta^3*e^2 - 8.03582947e-8*Delta_Tmrt*e^2 + 2.87019842e-9*Ta*Delta_Tmrt*e^2
        + 2.72198967e-7*v10*e^2 - 2.85083129e-8*Ta*v10*e^2 - 1.6839121e-8*v10^2*e^2
        + 1.80966787e-7*e^3 - 4.58555358e-9*Ta*e^3
    )

### F. Standard UTCI International Stress Scale
- > +46.0 deg C: Extreme Heat Stress (Hazard = 100.0)
- +38.0 to +46.0 deg C: Very Strong Heat Stress (Hazard = 80.0)
- +32.0 to +38.0 deg C: Strong Heat Stress (Hazard = 60.0)
- +26.0 to +32.0 deg C: Moderate Heat Stress (Hazard = 35.0)
- +9.0 to +26.0 deg C: No Thermal Stress / Comfort (Hazard = 0.0)

---

## 2. Wet Bulb Globe Temperature (WBGT - ISO 7243 & NIOSH 2016)

### A. Psychrometric Wet Bulb (Tw) via Roland Stull (2011) Formulation
    Tw = Ta * atan(0.151977 * sqrt(RH + 8.313659)) + atan(Ta + RH) - atan(RH - 1.676331) + 0.00391838 * (RH^1.5) * atan(0.023101 * RH) - 4.686035  [deg C]

### B. Surface Wind Scaling via Atmospheric Boundary Layer Power Law
    v2 = v10 * (2.0 / 10.0)^0.2 = v10 * 0.724779  [m/s]

### C. Natural Wet Bulb (Tnw) with Solar Irradiance
    Tnw = Tw + min(2.5, (0.0025 * S) / (v2^0.4 + 0.1))  [deg C]

### D. Matte-Black 150mm Globe Temperature (Tg) via Liljegren / Bernard
    Tg = Ta + (0.0149 * S) / (v2^0.6 + 0.05)  [deg C]

### E. Composite WBGT Formulations
    Outdoor (Direct Solar):  WBGT = 0.7 * Tnw + 0.2 * Tg + 0.1 * Ta  [deg C]
    Indoor / Complete Shade: WBGT = 0.7 * Tw + 0.3 * Tg  [deg C]

### F. NIOSH 2016 Occupational Work-Rest Regimen
- >= 32.0 deg C: Extreme Danger (25% Work / 75% Rest per hour or Halt Heavy Labor; >= 1.0 L/hr water)
- 30.0 to 32.0 deg C: High Risk (50% Work / 50% Rest per hour in designated shade; 1.0 L/hr water)
- 28.0 to 30.0 deg C: Moderate Risk (75% Work / 25% Rest per hour under shade; 0.75 L/hr water)
- < 28.0 deg C: Low Risk (Continuous work permissible; 0.5 L/hr water)

---

## 3. NOAA / National Weather Service Heat Index

### A. Lans P. Rothfusz (1990) 9-Term Polynomial Regression (T_F >= 80 deg F)
    HI_F = (
        -42.379
        + 2.04901523 * TF
        + 10.14333127 * RH
        - 0.22475541 * TF * RH
        - 0.00683783 * TF^2
        - 0.05481717 * RH^2
        + 0.00122874 * TF^2 * RH
        + 0.00085282 * TF * RH^2
        - 0.00000199 * TF^2 * RH^2
    )  [deg F]

Where TF = Ta * 1.8 + 32.0.

### B. High & Low Humidity Adjustments
    If RH < 13% and 80 <= TF <= 112 deg F:
        Delta_HI = -((13 - RH) / 4) * sqrt((17 - |TF - 95|) / 17)
    If RH > 85% and 80 <= TF <= 87 deg F:
        Delta_HI = +((RH - 85) / 10) * ((87 - TF) / 5)
    If TF < 80 deg F (Steadman):
        HI_F = 0.5 * (TF + 61.0 + (TF - 68.0)*1.2 + RH*0.094)

    HI_C = (HI_F - 32.0) / 1.8  [deg C]

---

## 4. Multi-Criteria Composite Thermal Hazard (H)
    H = 0.60 * H_UTCI + 0.25 * H_WBGT + 0.15 * H_HI  [0 to 100]

---

## 5. Census of India 2011 PCA Demographic Vulnerability (V)

Calculated from official Census of India 2011 Primary Census Abstract (PCA) tables:

### Indicator Normalization (Min-Max Empirical Bounds across Indian Districts)
1. Elderly Population Share (>= 60 yrs):
    Norm_eld = max(0, min(100, ((Elderly_pct - 4.0) / (16.0 - 4.0)) * 100))

2. Outdoor Labor Share (Agricultural Laborers + Cultivators + Construction/Marginal):
    Norm_wrk = max(0, min(100, ((Outdoor_pct - 10.0) / (45.0 - 10.0)) * 100))

3. Population Density (persons/km^2):
    Norm_den = max(0, min(100, ((Density - 200) / (25000 - 200)) * 100))

### Composite Vulnerability Equation
    V = 0.40 * Norm_eld + 0.35 * Norm_wrk + 0.25 * Norm_den  [0 to 100]

---

## 6. Composite Relative Heat-Health Risk Score (R)
    R = w_H * H + w_V * V + w_D * D  [0 to 100]

Where:
- w_H = 0.55: Thermal Hazard weight
- w_V = 0.30: Demographic Vulnerability weight
- w_D = 0.15: Cumulative Heat Duration weight
- D: Duration factor (D+1 = 0.0, D+2 = 33.0, D+3 = 66.0, D+4 = 100.0, D+5 = 100.0)

### 4-Tier Warning Decision Matrix
- R > 75.0: RED (Emergency Action Plan Activated; Halt outdoor heavy labor 11:00-16:00)
- 50.0 < R <= 75.0: ORANGE (Alert / Be Prepared; 50% work-rest cycle in designated shade)
- 25.0 < R <= 50.0: YELLOW (Watch / Be Updated; Frequent hydration; public drinking water points active)
- <= 25.0: GREEN (Normal / Low Risk; Routine summer precautions)

---

## 7. Step-by-Step Worked Numerical Proof (Pune District Case Study)

Input: Ta = 42.0 deg C, RH = 35.0%, v10 = 2.0 m/s, S = 700.0 W/m^2, Day = 3

1. Vapor Pressure: es(42.0) = 82.26 hPa => e = 82.26 * 0.35 = 28.79 hPa
2. Tmrt = [(315.15)^4 + (0.28*0.70*700.0)/(0.97*5.670374e-8)]^0.25 - 273.15 = 60.27 deg C (Delta_Tmrt = +18.27 deg C)
3. UTCI(42.0, 18.27, 2.0, 28.79) = 48.46 deg C => Extreme Heat Stress (H_UTCI = 100.0)
4. Tw(Stull) = 28.87 deg C, v2 = 1.45 m/s, Tnw = 30.26 deg C, Tg = 50.03 deg C => WBGT = 35.39 deg C (H_WBGT = 100.0)
5. TF = 107.6 deg F => HI_F = 122.47 deg F => HI_C = 50.26 deg C (H_HI = 80.0)
6. Composite Hazard H = 0.60(100.0) + 0.25(100.0) + 0.15(80.0) = 97.0 / 100
7. Pune Census 2011 PCA: Elderly 9.40%, Outdoor Labor 31.00%, Density 602.8 /km^2
   Norm_eld = 45.0, Norm_wrk = 60.0, Norm_den = 1.62 => V = 0.40(45.0) + 0.35(60.0) + 0.25(1.62) = 39.4 / 100
8. Duration factor D = 66.0 / 100 (Day 3)
9. Final Composite Risk R = 0.55(97.0) + 0.30(39.4) + 0.15(66.0) = 53.35 + 11.82 + 9.90 = 75.1 / 100 => RED ALERT

---

## 8. Standalone Verifier Script
To independently compute and verify these equations in 1 second, run:
`ash
python calculations_verifier.py
`
