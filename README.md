# Ratio de endeudamiento — autónomo con SL

Calcula el ratio de endeudamiento a partir de los modelos **130** y **303** de
los dos últimos trimestres, y cuánto hay que facturar o cobrar este trimestre
para alcanzar un neto objetivo después de IRPF.

## Uso

```bash
python3 objetivo_3t.py        # analisis con los 303 de 2026 ya cargados
python3 objetivo_3t.py 750    # idem, fijando otra cuota de RETA mensual

python3 ratio.py --ejemplo    # ratio de endeudamiento, demo
python3 ratio.py datos.json   # ratio de endeudamiento, con tus cifras
```

`objetivo_3t.py` lleva incorporadas las cifras de los modelos 303 de 2026
(1T y 2T) de José María Castillo como autónomo y de OSI Global Consulting SL.
`ratio.py` es la herramienta genérica, y necesita el modelo 130.

Rellena `datos.json` con las casillas de tus modelos. Sin dependencias
externas: solo Python 3.

## Qué datos necesitas

**Modelo 130** (los dos últimos trimestres) — es **acumulado desde enero**, así
que hacen falta los dos para poder aislar el trimestre. El script desacumula solo.

| Casilla | Concepto        | Campo en `datos.json` |
|---------|-----------------|-----------------------|
| 01      | Ingresos computables | `ingresos` |
| 02      | Gastos deducibles    | `gastos`   |

**Modelo 303** (mismos trimestres) — sirve de contraste, no es acumulado.

| Casilla    | Concepto                       | Campo |
|------------|--------------------------------|-------|
| 01+04+07   | Bases imponibles devengadas    | `base_devengada` |
| 28         | Base de IVA soportado deducible| `base_soportada` |

Más: nómina bruta anual de la SL y las cuotas mensuales de deuda.

## Cómo calcula

**Rendimiento neto del trimestre** — desacumulando el 130:

```
trimestre = casilla_03(actual) − casilla_03(previo)
```

**Ratio de endeudamiento** (criterio bancario, umbral habitual ≤ 35 %):

```
ratio = cuotas mensuales de deuda / ingreso neto mensual × 100
```

**Ingreso neto mensual** — proyecta el semestre a año completo, suma la nómina
de la SL, y aplica el IRPF anual **por escala**:

```
base general  = rend. neto actividad + rend. neto trabajo
neto anual    = rend. neto actividad + nómina bruta − IRPF
neto mensual  = neto anual / 12
```

**Objetivo de neto mensual** — resuelve por bisección el bruto necesario, en
dos escenarios alternativos: (A) subiendo la facturación como autónomo con la
nómina intacta, y (B) subiendo la nómina de la SL con la actividad intacta.
Ambos deben converger en la misma base imponible.

## Notas fiscales

- **El 20 % del modelo 130 es un pago a cuenta, no el IRPF final.** El cálculo
  usa la escala anual del IRPF, que es la que determina lo que realmente queda.
- **La escala autonómica varía por CCAA.** `irpf.py` usa la escala general
  estatal + una autonómica de referencia; ajústala a tu comunidad.
- **La cuota de autónomos** normalmente ya va dentro de la casilla 02 como gasto
  deducible. Solo rellena `reta_pagada_fuera_de_gastos_anual` si no es tu caso,
  para no restarla dos veces.
- **La proyección anual multiplica el semestre × 2.** Si tu facturación es
  estacional, sustitúyela por tu previsión real.
- Estimación orientativa. Confírmala con tu asesor antes de tomar decisiones.

## Estructura

| Fichero          | Contenido |
|------------------|-----------|
| `objetivo_3t.py` | Análisis del 3T 2026 con las cifras reales de los 303 |
| `ratio.py`       | Ratio de endeudamiento genérico (necesita el 130) |
| `irpf.py`        | Escalas IRPF y funciones fiscales |
| `datos.json`     | Plantilla para `ratio.py` |

## Hallazgos del ejercicio 2026 (1S)

- Como autónomo facturaste **15.000 € en el 1T y 0 € en el 2T**. El
  rendimiento neto del semestre queda en unos **5.046 €**, es decir
  **841 €/mes** — muy lejos de los 5.000 €/mes que se quieren acreditar.
- La SL factura toda su actividad por **inversión del sujeto pasivo**
  (casilla 122, IVA devengado cero): 50.131,33 € en el semestre.
- Descontando los costes con terceros, la SL deja unos **33.116 € por
  semestre** disponibles para retribuirte, ~16.558 € por trimestre.
- Para cerrar 2026 con una media de 5.000 €/mes netos harían falta unos
  **90.562 € facturados solo en el 3T**, frente a los ~16.558 € que da la
  sociedad al ritmo actual.
