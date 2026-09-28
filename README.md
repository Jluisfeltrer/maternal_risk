# Predicción de riesgo materno con Machine Learning

Clasificación del nivel de riesgo en el embarazo (**low / mid / high risk**) a partir de seis signos vitales, con un flujo completo y documentado: ingesta reproducible → limpieza trazable → EDA → modelado con Random Forest → app interactiva en Streamlit.

El foco del proyecto no es solo el modelo, sino **entender el dato**: cada decisión de limpieza y modelado está justificada y documentada, incluidas las limitaciones.

> ⚠️ **Aviso:** proyecto educativo y de portafolio. **No es una herramienta de diagnóstico ni sustituye el criterio clínico.**

---

## Pregunta del proyecto

¿Es posible estimar el nivel de riesgo de una paciente embarazada a partir de edad, presión arterial, glucosa, temperatura y frecuencia cardíaca? Y, sobre todo: ¿qué variables pesan más y dónde se equivoca el modelo?

## Resultados clave

- **Modelo:** Random Forest (baseline sin ajuste de hiperparámetros), split 80/20 estratificado.
- **Accuracy en test: 0.84** (203 pacientes).
- **High risk** se identifica muy bien (F1 = 0.95). El error se concentra en el par **low ↔ mid**, consistente con el solapamiento que ya mostraba el EDA.
- **Variable más importante: glucosa en sangre (`BS`)**, coherente con la hipótesis clínica de diabetes gestacional como factor de riesgo.
- Hallazgos de calidad de datos: temperatura en Fahrenheit, un valor fisiológicamente imposible (7 bpm), 562 filas duplicadas y un patrón generalizado de redondeo en signos vitales ("digit preference").

---

## Fuente de datos

**Dataset:** Maternal Health Risk, UCI Machine Learning Repository.

**Cita recomendada:**

> Ahmed, M. (2020). *Maternal Health Risk* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5DP5D

**Artículo introductorio del dataset:**

> Ahmed, M., Kashem, M. A., Rahman, M., & Khatun, S. (2020). *Review and Analysis of Risk Factor of Maternal Health in Remote Area Using the Internet of Things (IoT)*. Lecture Notes in Electrical Engineering, vol. 632. Springer. https://doi.org/10.1007/978-981-15-2317-5_30

- **Origen de los datos:** recogidos en hospitales, clínicas comunitarias y centros de salud materna de zonas rurales de Bangladesh mediante un sistema de monitorización de riesgo basado en IoT.
- **Página del dataset:** https://archive.ics.uci.edu/dataset/863/maternal+health+risk
- **Licencia:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Permite compartir y adaptar el dataset con cualquier fin, citando la fuente.
- **Cambios realizados sobre el dataset original** (requisito de CC BY 4.0): conversión de `BodyTemp` de °F a °C, exclusión de 2 filas con `HeartRate` inválido y creación de la variable derivada `tiene_fiebre`. El archivo original se conserva sin modificar en `data/raw/`.
- **Nota sobre el número de filas:** la ficha de UCI indica 1013 instancias; la descarga vía `ucimlrepo` (id=863) devolvió **1014 filas**, que son las que se usan como punto de partida.

---

## Diccionario de variables

| Variable | Descripción | Unidad | Rango típico normal |
|---|---|---|---|
| `Age` | Edad de la paciente | años | — |
| `SystolicBP` | Presión arterial sistólica (la cifra "alta" al medir la tensión) | mmHg | ~90–120 |
| `DiastolicBP` | Presión arterial diastólica (la cifra "baja" al medir la tensión) | mmHg | ~60–80 |
| `BS` | Nivel de glucosa (azúcar) en sangre | mmol/L* | ~4–6 (ayunas) |
| `BodyTemp` | Temperatura corporal | °C** | ~36.1–37.2 |
| `HeartRate` | Frecuencia cardíaca en reposo | latidos por minuto (bpm) | ~60–100 |
| `RiskLevel` | Nivel de riesgo durante el embarazo (**variable objetivo**) | categórica | low / mid / high risk |
| `tiene_fiebre` | *(derivada)* 1 si `BodyTemp` > 37.2 °C, 0 en caso contrario | binaria | — |

\* **Sobre `BS`:** el dataset expresa la glucosa en mmol/L, la unidad estándar en Europa y en la literatura médica internacional (en EE. UU. es más habitual mg/dL). **Se mantiene la unidad original** por fidelidad a la fuente. Para convertir a mg/dL, multiplica por 18 (ej. 8.7 mmol/L ≈ 157 mg/dL).

\*\* **Sobre `BodyTemp`:** el dataset original publica la temperatura en **grados Fahrenheit**. Se convirtió a Celsius en el preprocesamiento (`src/preprocessing.py`, función `convertir_fahrenheit_a_celsius`) por ser la unidad estándar en el contexto clínico europeo y más intuitiva para la mayoría de lectores.

---

## Estructura del repositorio

```
maternal-health-risk/
├── data/
│   ├── raw/                  # dataset original, sin tocar
│   └── processed/            # datos limpios y evidencia de exclusiones
│       ├── maternal_health_clean.csv
│       └── excluded_heartrate_outliers.csv
├── notebooks/
│   ├── 01_eda.ipynb          # limpieza + análisis exploratorio
│   └── 02_modeling.ipynb     # feature engineering, modelo y evaluación
├── src/
│   ├── eda.py                # funciones de resumen numérico
│   └── preprocessing.py      # limpieza y feature engineering
├── app/
│   └── app.py                # app Streamlit
├── models/
│   └── model.pkl             # Random Forest serializado
├── requirements.txt
├── .gitignore
└── README.md
```

**Por qué esta estructura:** `raw/` vs `processed/` da trazabilidad (siempre se puede volver al dato original); separar EDA y modelado hace que cada notebook cuente una historia distinta; `app/` consume el modelo ya entrenado en lugar de reentrenar, separando investigación de producto.

---

## Cómo reproducirlo

```bash
git clone https://github.com/Jluisfeltrer/maternal_risk.git
cd maternal_risk

python3 -m venv venv
source venv/bin/activate          # macOS / Linux
pip install -r requirements.txt

# Ejecutar los notebooks en orden: 01_eda.ipynb → 02_modeling.ipynb
jupyter notebook

# Lanzar la app (desde la raíz del proyecto)
streamlit run app/app.py
```

**Notas de entorno:**

- Los notebooks importan desde `src/` mediante `sys.path.append('..')` (se ejecutan desde `notebooks/`). La app calcula la ruta base a partir de su propio archivo (`__file__`), por lo que funciona sin importar desde dónde se lance.
- **Error SSL en macOS** (`CERTIFICATE_VERIFY_FAILED`) al descargar con `ucimlrepo`: ocurre con Python instalado desde python.org. Se resuelve ejecutando `Install Certificates.command` de la carpeta de Python en `/Applications`. Alternativa: usar el CSV ya guardado en `data/raw/`.
- Al ejecutar un notebook: comprobar que el kernel seleccionado es el del `venv`, y **ejecutar las celdas una sola vez y en orden** (ver lección sobre re-ejecución más abajo).

---

## Metodología y decisiones

### 1. Ingesta reproducible
El dato se descarga con el paquete oficial `ucimlrepo` (`fetch_ucirepo(id=863)`) dentro del propio notebook: la procedencia queda documentada en código, no como un paso manual invisible. Se guarda una copia en `data/raw/` para no depender de la red ni de que el servidor cambie.

### 2. Limpieza (`data/processed/`)

| Problema detectado | Decisión | Por qué |
|---|---|---|
| `BodyTemp` en °F (valores 98–103 parecían imposibles en °C) | Convertir a °C | Unidad estándar clínica en Europa. Documentado en el diccionario. |
| `HeartRate = 7` bpm en 2 filas (incompatible con la vida; posible error del sensor IoT) | **Excluir** y guardar evidencia en `excluded_heartrate_outliers.csv` | Coste mínimo (2 de 1014) y limpieza trazable: se conserva qué se quitó y con qué criterio. |
| 562 filas duplicadas (~55%) | **Conservar**, documentar | Las variables son muy discretas (edad entera, presión en saltos de 5–10 mmHg…), por lo que coincidencias entre pacientes distintas son estadísticamente esperables. Eliminarlas supondría perder más de la mitad de un dataset ya pequeño. La distribución de `RiskLevel` entre duplicados (mid 38.8 %, low 33.7 %, high 27.5 %) es similar a la global (low 40.0 %, mid 33.1 %, high 26.8 %). |
| `BS` en mmol/L | **Mantener** la unidad | Es la unidad usada en Europa; se documenta la conversión a mg/dL. |

Resultado: **1012 filas** en `maternal_health_clean.csv`.

> Las funciones de limpieza devuelven copias (`df.copy()`) para no modificar el DataFrame original por sorpresa, y la exclusión devuelve además las filas excluidas para poder auditarlas.

### 3. Análisis exploratorio (`01_eda.ipynb`)

- **Univariado:** `SystolicBP`, `DiastolicBP`, `HeartRate` y `BodyTemp` muestran picos en valores redondos (120, 80, 70, 36.7 °C…): *digit preference*, típico de toma manual o de equipos poco precisos. Es una limitación del dato, no un error a corregir.
- **`BodyTemp`:** ~79 % de las pacientes comparte un único valor (≈36.67 °C). Como variable continua aporta poco, pero **contiene señal si se interpreta como fiebre**: 11.1 % de fiebre (> 37.2 °C) en low risk frente a 26.8 % en mid y 26.5 % en high.
- **Bivariado vs. `RiskLevel`:** `SystolicBP`, `DiastolicBP` y `BS` separan mejor las clases. En casi todas las variables, **low y mid se solapan entre sí más que cualquiera de ellas con high**. Se anticipó que el modelo tendría más dificultad entre low y mid.
- **Correlaciones:** `SystolicBP`–`DiastolicBP` r = 0.79 (esperable clínicamente); `Age`–`BS` r ≈ 0.47; `BodyTemp` con correlaciones negativas débiles con el resto (≈ –0.26 a –0.29).

### 4. Feature engineering (`02_modeling.ipynb`)
Se crea `tiene_fiebre = (BodyTemp > 37.2)` **en el notebook de modelado y no en el dataset limpio**: la limpieza es objetiva y reutilizable para cualquier propósito; la binarización es una hipótesis orientada a este modelo (el umbral podría ajustarse). Mantener `processed/` neutral permite iterar sin deshacer transformaciones.

### 5. Codificación del target
`RiskLevel` es ordinal (low < mid < high), pero **se trata como clasificación multiclase con categorías independientes**, usando las etiquetas de texto directamente. Justificación: el EDA mostró que "mid" no se comporta como punto intermedio equidistante entre low y high (se solapa con low en varias variables). Una codificación 0/1/2 asumiría una relación lineal que los datos no respaldan.

### 6. Modelo
- **Split:** 80/20 con `stratify=y` y `random_state=42` (mismas proporciones de clase en train y test; reproducible).
- **Algoritmo:** Random Forest (baseline, sin ajuste de hiperparámetros). Elegido porque tolera bien la multicolinealidad entre presiones, no asume relaciones lineales y ofrece importancia de variables.
- **Features finales:** `Age`, `SystolicBP`, `DiastolicBP`, `BS`, `HeartRate`, `tiene_fiebre`. Se eliminó `BodyTemp` cruda: al quitarla, la accuracy pasó de 0.85 a 0.84 (diferencia dentro del ruido con 203 muestras de test), sin cambiar el patrón de errores.

### 7. Evaluación

**Modelo final (6 features), conjunto de test:**

| Clase | Precision | Recall | F1 | Soporte |
|---|---|---|---|---|
| high risk | 0.95 | 0.95 | 0.95 | 55 |
| low risk | 0.89 | 0.77 | 0.82 | 81 |
| mid risk | 0.73 | 0.85 | 0.79 | 67 |
| **Accuracy** | | | **0.84** | 203 |
| Macro avg | 0.85 | 0.85 | 0.85 | |

**Matriz de confusión del modelo base** (con `BodyTemp` incluida; filas = real, columnas = predicho):

| Real \ Predicho | low | mid | high |
|---|---|---|---|
| **low** | 63 | 17 | 1 |
| **mid** | 7 | 58 | 2 |
| **high** | 0 | 3 | 52 |

**Lectura:** el error se concentra en el par low ↔ mid (24 de los errores cruzados); apenas hay confusión entre extremos (low↔high). Es exactamente el solapamiento anticipado en el EDA: una limitación del propio dato más que un fallo del modelo.

### 8. Importancia de variables
Modelo base (7 variables, antes de eliminar `BodyTemp`):

| Variable | Importancia |
|---|---|
| `BS` | 0.337 |
| `SystolicBP` | 0.197 |
| `Age` | 0.164 |
| `DiastolicBP` | 0.124 |
| `HeartRate` | 0.107 |
| `BodyTemp` | 0.050 |
| `tiene_fiebre` | 0.021 |

**Cómo interpretarlo:** `BS` domina, en línea con la hipótesis de diabetes gestacional. `SystolicBP` obtiene ~el doble de importancia que `DiastolicBP` pese a mostrar separación similar en el EDA: es un efecto de la **multicolinealidad** (r = 0.79). Random Forest tolera la multicolinealidad para *predecir*, pero la métrica de importancia se reparte de forma desigual entre variables redundantes. **Esto no implica que `DiastolicBP` sea clínicamente menos relevante:** ambas presiones no son intercambiables terapéuticamente, por lo que se conserva.

### 9. App interactiva (Streamlit)
Formulario con deslizadores (edad, presión sistólica y diastólica, glucosa en mmol/L, frecuencia cardíaca y temperatura) y botón **"Predecir el nivel de riesgo"**.

- La app pide la **temperatura en °C** (más natural que "¿tiene fiebre?") y la convierte a `tiene_fiebre` reutilizando `crear_indicador_fiebre` de `src/preprocessing.py`: **una sola fuente de verdad** para el umbral.
- Los rangos de los deslizadores se basan en los rangos observados en los datos limpios, para no pedir predicciones fuera de lo que el modelo ha visto.
- El botón evita recalcular en cada movimiento de un deslizador.

---

## Limitaciones

- **Calidad del dato:** redondeo generalizado (*digit preference*) y `BodyTemp` casi constante. Los signos vitales pueden no ser mediciones exactas.
- **Duplicados conservados y posible fuga de datos (*data leakage*):** con 562 filas repetidas y un split aleatorio, filas idénticas pueden caer a la vez en train y test, lo que puede **inflar la accuracy**. La cifra de 0.84 debe leerse con esta cautela; ver trabajo futuro.
- **Edades extremas:** el dataset incluye edades de 10 a 70 años. Los extremos son clínicamente inusuales para una gestación y no se han excluido porque la fuente no permite confirmarlos como error; conviene tenerlo presente.
- **Procedencia y generalización:** datos de zonas rurales de Bangladesh recogidos vía IoT; no está validado que el modelo generalice a otras poblaciones (por ejemplo, contextos europeos).
- **Target ordinal tratado como nominal:** no se aprovecha el orden real entre clases (confundir low con high es clínicamente peor que low con mid).
- **Tamaño y evaluación:** ~1000 filas y una única partición train/test (203 muestras): las métricas tienen incertidumbre.
- **Importancia de variables** afectada por multicolinealidad (ver arriba).
- **Sin calibración ni validación clínica:** las salidas no son probabilidades calibradas ni orientación médica.

## Trabajo futuro

- Ajuste de hiperparámetros (`GridSearchCV`); se estima ganancia modesta porque el error viene del solapamiento real de clases.
- **Validación cruzada** y evaluación sobre datos **deduplicados** (o *split* agrupado) para cuantificar el efecto de los duplicados en la accuracy.
- Explorar otros umbrales de fiebre (p. ej. 37.5 °C) y comparar con Regresión Logística como modelo de referencia.
- Clasificación **ordinal** específica (respeta low < mid < high).
- Explicabilidad adicional (p. ej. SHAP) y matriz de confusión del modelo final.
- Usar `%load_ext autoreload` / `%autoreload 2` al iterar sobre módulos de `src/`.

---

## Gobernanza y seguridad del dato

- **Trazabilidad:** dato original intacto en `raw/`; transformaciones en código versionado; exclusiones guardadas en un CSV propio; decisiones documentadas en los notebooks.
- **Reproducibilidad:** entorno virtual, `requirements.txt` congelado con `pip freeze`, `random_state=42` en split y modelo, ingesta desde fuente oficial con DOI.
- **Una sola fuente de verdad:** la lógica de limpieza y de umbral de fiebre vive en `src/preprocessing.py` y se reutiliza en notebooks y app.
- **Datos:** dataset abierto (CC BY 4.0), sin identificadores personales; este proyecto no maneja credenciales ni claves de API. Al trabajar con APIs o bases de datos privadas, las credenciales irían en variables de entorno (`.env` fuera del repositorio, listado en `.gitignore`).
- **Serialización:** `model.pkl` se carga con `joblib`; no cargar archivos `.pkl` de procedencia desconocida (pueden ejecutar código arbitrario).
- **Control de versiones:** `.gitignore` excluye `venv/`, `__pycache__/` y `.ipynb_checkpoints/`.

## Lecciones aprendidas

- **Documentar unidades** evita "errores" fantasma (la temperatura en °F parecía imposible en °C).
- **Notebooks:** re-ejecutar una celda que reasigna `df` puede aplicar dos veces una transformación (la conversión de temperatura dio valores ≈ 2.6 °C). Ejecutar en orden, o reiniciar el kernel y usar *Run All*.
- **Rutas:** en scripts, anclar las rutas al propio archivo (`__file__`) en vez de a `'..'`.
- El boxplot por grupos puede **crear "outliers" artificiales** cuando un grupo tiene casi cero dispersión: cuantificar antes de concluir.

---

## Autor y licencias

**Jose Luis Morales Feltrer** — [github.com/Jluisfeltrer](https://github.com/Jluisfeltrer). La revisión clínica de los datos (unidades, plausibilidad fisiológica) fue realizada por el autor, Licenciado en Enfermería.

- **Datos:** CC BY 4.0 (Ahmed, M., 2020; ver [Fuente de datos](#fuente-de-datos)).
- **Código:** [MIT](LICENSE). La licencia MIT cubre únicamente el código de este repositorio; los datos conservan su licencia original (CC BY 4.0).
