# Ratio de endeudamiento — autónomo con SL

Calcula el ratio de endeudamiento a partir de los modelos **130** y **303** de
los dos últimos trimestres, y cuánto hay que facturar o cobrar este trimestre
para alcanzar un neto objetivo después de IRPF.

## Uso

```bash
python3 ratio.py --ejemplo    # demo con cifras inventadas
python3 ratio.py datos.json   # con tus cifras reales
```

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

| Fichero      | Contenido |
|--------------|-----------|
| `ratio.py`   | Cálculo y report por consola |
| `irpf.py`    | Escalas IRPF y funciones fiscales |
| `datos.json` | Plantilla para tus cifras |
