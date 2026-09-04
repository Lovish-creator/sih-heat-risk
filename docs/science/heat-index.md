# NOAA/NWS Heat Index - Scientific Documentation

## 1. Scientific Concept & History
The **Heat Index (HI)**, colloquially known as the "Feels Like" temperature or apparent temperature, was developed by Robert G. Steadman (1979) and adopted by the US National Weather Service (NWS). It measures the perceived thermal discomfort caused by the combined effect of dry-bulb air temperature and relative humidity.

When relative humidity is high, the evaporation rate of perspiration from the human skin is severely reduced, hindering the body's primary thermoregulatory cooling mechanism and elevating internal core body temperature.

---

## 2. Mathematical Formulation (Rothfusz Regression Equation)
The operational calculation utilizes Lans P. Rothfusz's (1990) 9-term multiple regression polynomial, fitted for temperature in degrees Fahrenheit ($T_F$) and relative humidity ($\text{RH}$ in $\%$):

$$\text{HI}_F = c_1 + c_2 T_F + c_3 \text{RH} + c_4 T_F \text{RH} + c_5 T_F^2 + c_6 \text{RH}^2 + c_7 T_F^2 \text{RH} + c_8 T_F \text{RH}^2 + c_9 T_F^2 \text{RH}^2$$

Where constants are:
- $c_1 = -42.379$
- $c_2 = 2.04901523$
- $c_3 = 10.14333127$
- $c_4 = -0.22475541$
- $c_5 = -6.83783 \times 10^{-3}$
- $c_6 = -5.481717 \times 10^{-2}$
- $c_7 = 1.22874 \times 10^{-3}$
- $c_8 = 8.5282 \times 10^{-4}$
- $c_9 = -1.99 \times 10^{-6}$

### Adjustments:
1. **Low Humidity Adjustment** (If $\text{RH} < 13\%$ and $80^\circ\text{F} \le T_F \le 112^\circ\text{F}$):
   $$\text{Adj}_{\text{low}} = -\frac{13 - \text{RH}}{4} \times \sqrt{\frac{17 - |T_F - 95|}{17}}$$
2. **High Humidity Adjustment** (If $\text{RH} > 85\%$ and $80^\circ\text{F} \le T_F \le 87^\circ\text{F}$):
   $$\text{Adj}_{\text{high}} = +\frac{\text{RH} - 85}{10} \times \frac{87 - T_F}{5}$$

The final Fahrenheit value is converted to Celsius: $\text{HI}_C = \frac{\text{HI}_F - 32}{1.8}$.

---

## 3. NWS Heat Index Categories

| Heat Index ($^\circ\text{C}$) | Heat Index ($^\circ\text{F}$) | Classification | Potential Health Effects |
|:---|:---|:---|:---|
| **$27.0 \text{ to } 32.0$** | $80 \text{ to } 90$ | **Caution** | Fatigue possible with prolonged exposure and activity |
| **$32.0 \text{ to } 41.0$** | $90 \text{ to } 105$ | **Extreme Caution** | Sunstroke, muscle cramps, and heat exhaustion possible |
| **$41.0 \text{ to } 54.0$** | $105 \text{ to } 130$ | **Danger** | Sunstroke, heat cramps, or heat exhaustion likely; heat stroke possible |
| **$> 54.0$** | $> 130$ | **Extreme Danger** | Heat stroke highly likely / imminent |

---

## 4. Scientific Limitations Compared to UTCI & WBGT
1. **In-Shade & Light Wind Assumption**: Heat Index explicitly assumes a person in the shade with a light wind ($v \approx 1.5\text{ m/s}$ or $5\text{ knots}$). It completely neglects direct solar radiation.
2. **Fixed Clothing & Metabolic Rate**: Assumes fixed clothing insulation and walking at $3.1\text{ mph}$.
3. **Upper Bound Instability**: At extreme temperatures ($> 48^\circ\text{C}$) and high humidity, the polynomial extrapolates rapidly.
