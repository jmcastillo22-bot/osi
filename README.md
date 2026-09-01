# Ratio de endeudamiento — autónomo con SL

Calcula el ratio de endeudamiento a partir de los modelos **130** y **303** de
los dos últimos trimestres, y cuánto hay que facturar o cobrar este trimestre
para alcanzar un neto objetivo después de IRPF.

## Uso

```bash
python3 objetivo_3t.py        # analisis con los 303 de 2026 ya cargados
python3 objetivo_3t.py 750    # idem, fijando otra cuota de RETA mensual

python3 capacidad.py          # capacidad de endeudamiento (ratio de partida 0%)
python3 capacidad.py 0.30     # idem, con otro umbral bancario

python3 ratio.py --ejemplo    # ratio de endeudamiento, demo
python3 ratio.py datos.json   # ratio de endeudamiento, con tus cifras
```

`objetivo_3t.py` lleva incorporadas las cifras reales de 2026 (1T y 2T):
modelos 130 y 303 de José María Castillo como autónomo, y modelo 303 de
OSI Global Consulting SL. `ratio.py` es la herramienta genérica.

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
| `objetivo_3t.py` | Análisis del 3T 2026 con las cifras reales de los 130 y 303 |
| `capacidad.py`   | Cuota y capital financiables sin deuda previa |
| `ratio.py`       | Ratio de endeudamiento genérico (necesita el 130) |
| `irpf.py`        | Escalas IRPF y funciones fiscales |
| `datos.json`     | Plantilla para `ratio.py` |

## Hallazgos del ejercicio 2026 (1S)

- Como autónomo facturaste **15.000 € en el 1T y 0 € en el 2T**: la casilla 01
  del 130 no se mueve entre trimestres. El 2T solo suma gastos, así que el
  rendimiento neto acumulado **baja** de 11.424,14 € a **8.641,08 €**, es decir
  **1.440 €/mes** — lejos de los 5.000 €/mes que se quieren acreditar.
- Los gastos del 130 (6.358,92 €) superan en solo **5,10 €** a las compras con
  IVA del 303 (6.353,82 €). Como la cuota de RETA no soporta IVA, la diferencia
  debería ser de varios miles: **posiblemente no se está deduciendo**.
- La SL factura toda su actividad por **inversión del sujeto pasivo**
  (casilla 122, IVA devengado cero): 50.131,33 € en el semestre. Descontando
  los costes con terceros deja unos **33.116 € por semestre**, ~16.558 € por
  trimestre, disponibles para retribución.
- Para cerrar 2026 con una media de 5.000 €/mes netos harían falta
  **85.169 € facturados solo en el 3T**, frente a esos ~16.558 €.

## Capacidad de endeudamiento

Sin cuotas de deuda vivas el ratio de partida es **0 %**, así que todo el
margen del umbral bancario está disponible y el límite lo pone el ingreso
acreditable, no la deuda previa:

| Escenario | Neto/mes | Cuota máx. (35 %) | Capital al 3 % / 30 años |
|---|---|---|---|
| Ritmo real del 1S | 1.234,29 € | 432,00 € | 102.466 € |
| Techo de la SL hoy | 3.255,53 € | 1.139,44 € | 270.262 € |
| Objetivo declarado | 5.000,00 € | 1.750,00 € | 415.081 € |

El techo de la SL es lo máximo que da la estructura actual destinando a
retribución todo el margen de la sociedad.
