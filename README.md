## Diccionario de variables






















| Variable | Descripción | Unidad | Rango típico normal |
|---|---|---|---|
| `Age` | Edad de la paciente en el momento del embarazo | años | — |
| `SystolicBP` | Presión arterial sistólica (la cifra "alta" al medir la tensión) | mmHg | ~90–120 |
| `DiastolicBP` | Presión arterial diastólica (la cifra "baja" al medir la tensión) | mmHg | ~60–80 |
| `BS` | Nivel de glucosa (azúcar) en sangre | mmol/L* | ~4–6 (ayunas) |
| `BodyTemp` | Temperatura corporal | °C | ~36.1–37.2 |
| `HeartRate` | Frecuencia cardíaca en reposo | latidos por minuto (bpm) | ~60–100 |
| `RiskLevel` | Nivel de riesgo de la paciente durante el embarazo (variable objetivo) | categórica | low / mid / high risk |

\* **Nota sobre `BS`:** el dataset original expresa la glucosa en mmol/L, la unidad estándar 
en Europa y en la literatura médica internacional (a diferencia de mg/dL, más común en 
EE.UU.). Se mantiene la unidad original del dataset por fidelidad a la fuente; para 
convertir a mg/dL, multiplica por 18 (ej. 8.7 mmol/L ≈ 157 mg/dL).

**Nota sobre `BodyTemp`:** el dataset original de UCI expresa la temperatura en grados 
Fahrenheit. Se convirtió a Celsius en el preprocesamiento (`src/preprocessing.py`, función 
`convertir_fahrenheit_a_celsius`) por ser la unidad estándar en el contexto clínico europeo 
y más intuitiva para la mayoría de lectores del proyecto.

