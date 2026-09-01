# Ratio de endeudamiento — autónomo con SL

Calcula el ratio de endeudamiento a partir de los modelos **130** y **303** de
los dos últimos trimestres, y cuánto hay que facturar o cobrar este trimestre
para alcanzar un neto objetivo después de IRPF.

## Uso

```bash
python3 objetivo_3t.py        # analisis con los 303 de 2026 ya cargados
python3 objetivo_3t.py 750    # idem, fijando otra cuota de RETA mensual

python3 verifica_ingresos.py <dir_pdf>   # extrae y contrasta los importes de los PDF
python3 quien_factura.py      # las dos estructuras posibles del cliente irlandes
python3 modelo_232.py         # umbrales del 232 y coste de esquivarlos
python3 factura_40000.py      # efecto de la factura de 40.000 del 30 de septiembre
python3 cierre_3t.py          # cierre del 3T: fechas, devengo y pago fraccionado
python3 cliente_irlanda.py    # efecto del nuevo cliente irlandes
python3 escenario_2s.py       # efecto de las facturas previstas del 2S
python3 maximo_hipoteca.py    # cifra realista para maximizar la hipoteca
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
| `verifica_ingresos.py` | Extrae los importes de los PDF presentados y los contrasta |
| `quien_factura.py` | Las dos estructuras posibles frente al cliente irlandés |
| `modelo_232.py` | Umbrales del modelo 232 y coste de quedarse por debajo |
| `factura_40000.py` | Efecto de la factura de 40.000 € del 30 de septiembre |
| `cierre_3t.py` | Cierre del 3T: calendario, devengo y pago fraccionado |
| `cliente_irlanda.py` | Efecto del nuevo cliente irlandés sobre 2026 |
| `escenario_2s.py` | Efecto de las facturas previstas del segundo semestre |
| `maximo_hipoteca.py` | Cifra realista de facturación para maximizar la hipoteca |
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
  IVA del 303 (6.353,82 €). Con una cuota de RETA de 88 €/mes (tarifa plana),
  la diferencia debería rondar los 528 € en el semestre: **no se está
  deduciendo**, unos 1.056 € anuales de gasto sin aplicar.
- La casilla 06 del 130 (1.050,00 €) es el **7 % de retención** sobre los 15.000 €
  facturados: el tipo reducido de nuevo autónomo (art. 101.5 LIRPF), aplicable
  el año de alta y los dos siguientes.
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

## Cifra realista para la hipoteca

Con la SL facturando lo que factura, el techo es facturar **25.615,57 € en el
3T y otro tanto en el 4T** (66.231,14 € en el año), que dejan un rendimiento
neto de 52.457,30 €:

| Base que use el banco | €/mes | Cuota al 35 % | Capital al 3 % / 30 años |
|---|---|---|---|
| Neto después de IRPF | 3.200,09 € | 1.120,03 € | 265.660 € |
| Rendimiento neto / 12 | 4.371,44 € | 1.530,00 € | 362.901 € |

Los 5.000 €/mes netos exigirían facturar 104.404,75 € en el año, por encima de
lo que la sociedad genera.

## Estructura confirmada

- Al cliente irlandés le factura **la SL** (B22831267), sin IVA, por inversión
  del sujeto pasivo. No pasa por el modelo 130 personal.
- El contribuyente factura **solo a la SL**, con 21 % de IVA y 7 % de retención
  (tipo reducido de nuevo autónomo, art. 101.5 LIRPF).
- La SL está dada de alta en el ROI con NIF-IVA validado en VIES.

### Calendario de cierre

| Fecha | Quién | Acción |
|---|---|---|
| 12 sep | SL | Factura 11.000 € a Irlanda → 3T, **casilla 59** y modelo 349 |
| 30 sep | Tú | Emites 40.000 € + 8.400 € IVA a la SL (servicio ya prestado) |
| 1–20 oct | Tú | Modelo 130 del 3T: **3.450,88 €** · Modelo 303 del 3T: **6.924,39 €** |
| 1–20 oct | SL | Modelo 349 del 3T (11.000 €) y modelo 111 (2.800 € de retención) |
| 12 oct | SL | Factura 17.000 € a Irlanda → 4T |
| 4T | Tú | Hasta **21.579,81 €** más a la SL para agotar su margen |
| ene 2027 | SL | 303 del 4T: solicitar devolución del crédito de IVA (~15.000 €) |
| nov 2027 | SL | **Modelo 232** de operaciones vinculadas |

Atención: la facturación irlandesa va en la **casilla 59**, no en la 122 donde
figura la actividad interior. Si se declara en la 122 el modelo 349 no cuadrará
en el cruce VIES.
