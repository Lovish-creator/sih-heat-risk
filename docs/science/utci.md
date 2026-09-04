# Universal Thermal Climate Index (UTCI) - Scientific Documentation

## 1. Scientific Concept
The **Universal Thermal Climate Index (UTCI)** is an advanced biometeorological metric that characterizes the human physiological response to ambient thermal environments. Developed under the European COST Action 730 and the International Society of Biometeorology (ISB), UTCI is based on the multi-node Fiala thermoregulation model coupled with an adaptive clothing insulation model.

UTCI is defined as the equivalent ambient air temperature ($T_{\text{ref}}$) of a reference environment with $50\%$ relative humidity (or water vapor pressure $e = 20\text{ hPa}$ for $T_a > 29^\circ\text{C}$), calm air ($v_{10} = 0.5\text{ m/s}$), and mean radiant temperature equal to air temperature ($T_{mrt} = T_a$), which produces the same dynamic physiological strain in a walking person ($4\text{ km/h}$, metabolic rate $\approx 135\text{ W/m}^2$) as the actual complex environment.

---

## 2. Mathematical Formulation & Operational Polynomial
Because solving the underlying differential equations of the 187-node human heat balance model in real time is computationally prohibitive, Bröde et al. (2012) derived an operational 6th-order polynomial regression approximation:

$$\text{UTCI} = T_a + \Delta\text{UTCI}(T_a, T_{mrt} - T_a, v_{10}, e)$$

Where:
- $T_a$: Ambient dry-bulb air temperature ($^\circ\text{C}$)
- $T_{mrt}$: Mean Radiant Temperature ($^\circ\text{C}$)
- $v_{10}$: Wind speed at 10 meters height ($\text{m/s}$)
- $e$: Water vapor pressure ($\text{hPa}$ or $\text{kPa}$)
- $\Delta\text{UTCI}$: 6th-order polynomial expansion involving over 240 cross-term regression coefficients.

### Water Vapor Pressure Calculation (Magnus-Tetens Formula)
$$e = 6.112 \times \exp\left(\frac{17.67 \times T_a}{T_a + 243.5}\right) \times \frac{\text{RH}}{100}$$

### Mean Radiant Temperature ($T_{mrt}$) Estimation
When solar irradiance is available, $T_{mrt}$ is derived from surface solar flux ($S$, in $\text{W/m}^2$) using the Stefan-Boltzmann radiation balance:

$$T_{mrt} = \left[ (T_a + 273.15)^4 + \frac{f_p \cdot \alpha_k \cdot S}{\epsilon_p \cdot \sigma} \right]^{0.25} - 273.15$$

Where:
- $f_p$: Projection factor for a standing person ($\approx 0.28$)
- $\alpha_k$: Absorption coefficient of human skin/clothing for shortwave radiation ($\approx 0.70$)
- $\epsilon_p$: Emissivity of the human body ($\approx 0.97$)
- $\sigma$: Stefan-Boltzmann constant ($5.67 \times 10^{-8}\text{ W/m}^2\text{K}^4$)

---

## 3. Operational Validity Ranges & Clamping
The operational polynomial is scientifically validated strictly within:
- **Air Temperature ($T_a$)**: $-50.0^\circ\text{C} \le T_a \le +50.0^\circ\text{C}$
- **Radiant Temperature Difference ($\Delta T_{mrt} = T_{mrt} - T_a$)**: $-30.0^\circ\text{C} \le \Delta T_{mrt} \le +70.0^\circ\text{C}$
- **10m Wind Speed ($v_{10}$)**: $0.5\text{ m/s} \le v_{10} \le 17.0\text{ m/s}$ (values $< 0.5\text{ m/s}$ clamped to $0.5\text{ m/s}$)
- **Water Vapor Pressure ($e$)**: $0.0\text{ hPa} \le e \le 50.0\text{ hPa}$

---

## 4. UTCI Thermal Stress Categories

| UTCI Range ($^\circ\text{C}$) | Thermal Stress Category | Physiological Response / Health Impact |
|:---|:---|:---|
| **$> +46.0$** | **Extreme Heat Stress** | Severe risk of heat stroke, failure of core thermoregulation, immediate danger |
| **$+38.0 \text{ to } +46.0$** | **Very Strong Heat Stress** | Heavy physiological strain, elevated cardiovascular load, severe dehydration risk |
| **$+32.0 \text{ to } +38.0$** | **Strong Heat Stress** | Significant sweating, elevated core temperature, heat exhaustion risk |
| **$+26.0 \text{ to } +32.0$** | **Moderate Heat Stress** | Mild thermal discomfort, moderate thermoregulatory effort |
| **$+9.0 \text{ to } +26.0$** | **No Thermal Stress (Comfort)** | Thermoneutral zone, optimal thermal comfort |
| **$0.0 \text{ to } +9.0$** | **Slight Cold Stress** | Vasoconstriction, mild cool sensation |
| **$-13.0 \text{ to } 0.0$** | **Moderate Cold Stress** | Significant shivering, increased metabolic rate |
| **$-27.0 \text{ to } -13.0$** | **Strong Cold Stress** | Frostnip danger, rapid heat loss |
| **$-40.0 \text{ to } -27.0$** | **Very Strong Cold Stress** | High frostbite hazard |
| **$< -40.0$** | **Extreme Cold Stress** | Immediate hypothermia risk |

---

## 5. Validation Example
- **Case 1 (Hot & Humid)**: $T_a = 38^\circ\text{C}$, $\text{RH} = 70\%$, $v_{10} = 1.0\text{ m/s}$, $S = 600\text{ W/m}^2$
  - Calculated $e \approx 46.4\text{ hPa}$
  - Calculated $\Delta T_{mrt} \approx +16.8^\circ\text{C}$
  - Resulting $\text{UTCI} \approx 47.8^\circ\text{C}$ (**Extreme Heat Stress**)
- **Case 2 (Hot & Dry with Wind)**: $T_a = 38^\circ\text{C}$, $\text{RH} = 20\%$, $v_{10} = 5.0\text{ m/s}$, $S = 200\text{ W/m}^2$
  - Calculated $e \approx 13.3\text{ hPa}$
  - Resulting $\text{UTCI} \approx 34.2^\circ\text{C}$ (**Strong Heat Stress** vs Extreme)

---

## 6. Limitations
1. Does not account for individual physiological variation (age, obesity, chronic cardiovascular illness, pregnancy).
2. Assumes standard metabolic walking activity ($135\text{ W/m}^2$) and standard self-adapting seasonal clothing insulation.
