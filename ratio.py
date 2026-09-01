#!/usr/bin/env python3
"""Ratio de endeudamiento y objetivo de retribucion para autonomo con SL.

Parte de los modelos 130 (acumulados) y 303 (trimestrales) de los dos
ultimos trimestres y calcula:

  1. Rendimiento neto real de cada trimestre (aislando el acumulado del 130)
  2. Ingreso neto mensual despues de IRPF
  3. Ratio de endeudamiento actual
  4. Cuanto hay que facturar / cobrar este trimestre para un neto objetivo

Uso:
    python3 ratio.py datos.json
    python3 ratio.py --ejemplo
"""

import json
import sys

from irpf import (
    cuota_irpf,
    rendimiento_neto_trabajo,
    resuelve_bruto,
)

MESES_TRIMESTRE = 3
MESES_ANO = 12


def eur(x):
    return f"{x:>12,.2f} EUR".replace(",", "@").replace(".", ",").replace("@", ".")


def linea(titulo=""):
    print()
    if titulo:
        print(titulo)
        print("-" * len(titulo))


def sin_comentarios(d):
    """Descarta las claves "_..." que la plantilla usa como comentarios."""
    return {k: v for k, v in d.items() if not k.startswith("_")}


def desacumula_130(m130):
    """El 130 es acumulado desde enero: aisla el trimestre mas reciente."""
    previo, actual = m130["previo"], m130["actual"]
    trimestre = {
        clave: actual[clave] - previo[clave]
        for clave in ("ingresos", "gastos")
    }
    trimestre["rendimiento_neto"] = trimestre["ingresos"] - trimestre["gastos"]
    return trimestre


def analiza(d):
    cfg = sin_comentarios(d.get("config", {}))
    objetivo_neto_mes = d.get("objetivo_neto_mensual", 5000.0)
    reta_aparte = cfg.get("reta_pagada_fuera_de_gastos_anual", 0.0)

    # --- 1. Actividad como autonomo (modelo 130) -------------------------
    m130 = d["modelo_130"]
    q_previo = {
        "ingresos": m130["previo"]["ingresos"],
        "gastos": m130["previo"]["gastos"],
        "rendimiento_neto": m130["previo"]["ingresos"] - m130["previo"]["gastos"],
    }
    q_actual = desacumula_130(m130)
    semestre_rn = q_previo["rendimiento_neto"] + q_actual["rendimiento_neto"]
    semestre_gastos = q_previo["gastos"] + q_actual["gastos"]

    linea("1. ACTIVIDAD DE AUTONOMO (modelo 130, desacumulado)")
    for nombre, q in (("Trimestre previo", q_previo), ("Ultimo trimestre", q_actual)):
        print(f"{nombre}:")
        print(f"  Ingresos computables   {eur(q['ingresos'])}")
        print(f"  Gastos deducibles      {eur(q['gastos'])}")
        print(f"  Rendimiento neto       {eur(q['rendimiento_neto'])}")
    print(f"Rendimiento neto del semestre {eur(semestre_rn)}")

    # --- 2. Contraste con el 303 -----------------------------------------
    m303 = d.get("modelo_303")
    if m303:
        linea("2. CONTRASTE CON EL MODELO 303 (IVA)")
        base_303 = m303["previo"]["base_devengada"] + m303["actual"]["base_devengada"]
        ingresos_130 = q_previo["ingresos"] + q_actual["ingresos"]
        print(f"  Base devengada 303 (semestre) {eur(base_303)}")
        print(f"  Ingresos 130 (semestre)       {eur(ingresos_130)}")
        desvio = ingresos_130 - base_303
        print(f"  Desvio                        {eur(desvio)}")
        if ingresos_130 and abs(desvio) / ingresos_130 > 0.05:
            print("  AVISO: desvio > 5%. Normal si hay ingresos exentos de IVA")
            print("         o intracomunitarios; revisalo si no es el caso.")

    # --- 3. Nomina de la SL ----------------------------------------------
    nomina = sin_comentarios(d.get("nomina_sl", {}))
    bruto_nomina_anual = nomina.get("bruto_anual", 0.0)

    # --- 4. Proyeccion anual e IRPF --------------------------------------
    rn_actividad_anual = semestre_rn * 2  # proyeccion lineal del semestre
    rn_trabajo = rendimiento_neto_trabajo(bruto_nomina_anual, reta_aparte)
    base_general = rn_actividad_anual + rn_trabajo
    irpf = cuota_irpf(base_general)
    neto_anual = rn_actividad_anual + bruto_nomina_anual - reta_aparte - irpf
    neto_mensual = neto_anual / MESES_ANO

    linea("3. PROYECCION ANUAL E IRPF")
    print(f"  Rend. neto actividad (x2 semestre) {eur(rn_actividad_anual)}")
    print(f"  Nomina bruta SL                    {eur(bruto_nomina_anual)}")
    print(f"  Base imponible general             {eur(base_general)}")
    print(f"  Cuota IRPF estimada                {eur(irpf)}")
    if base_general:
        print(f"  Tipo efectivo                      {100 * irpf / base_general:>11.2f} %")
    print(f"  NETO ANUAL despues de IRPF         {eur(neto_anual)}")
    print(f"  NETO MENSUAL                       {eur(neto_mensual)}")

    # --- 5. Ratio de endeudamiento ---------------------------------------
    deudas = sin_comentarios(d.get("deudas_mensuales", {}))
    cuota_deuda = sum(deudas.values())

    linea("4. RATIO DE ENDEUDAMIENTO")
    for concepto, importe in deudas.items():
        print(f"  {concepto:<32} {eur(importe)}")
    print(f"  {'TOTAL cuotas mensuales':<32} {eur(cuota_deuda)}")
    if neto_mensual > 0:
        ratio = 100 * cuota_deuda / neto_mensual
        print(f"\n  RATIO ACTUAL                     {ratio:>11.2f} %")
        veredicto = (
            "OK, dentro del umbral bancario habitual (<=35%)"
            if ratio <= 35
            else "POR ENCIMA del 35% que suele exigir el banco"
        )
        print(f"  {veredicto}")
    else:
        ratio = None
        print("  Neto mensual <= 0: ratio no calculable.")

    # --- 6. Objetivo: neto de X EUR/mes despues de IRPF -------------------
    linea(f"5. OBJETIVO: {objetivo_neto_mes:,.0f} EUR/mes NETOS DESPUES DE IRPF"
          .replace(",", "."))
    neto_objetivo_anual = objetivo_neto_mes * MESES_ANO

    # Escenario A: subir la facturacion como autonomo, nomina intacta.
    def neto_via_actividad(rn_act):
        base = rn_act + rn_trabajo
        return rn_act + bruto_nomina_anual - reta_aparte - cuota_irpf(base)

    rn_necesario = resuelve_bruto(neto_objetivo_anual, neto_via_actividad)
    falta_semestre = rn_necesario - semestre_rn
    gasto_medio_trim = semestre_gastos / 2

    print("A) Subiendo la facturacion como autonomo (nomina SL intacta)")
    print(f"  Rend. neto anual necesario         {eur(rn_necesario)}")
    print(f"  Ya acumulado (1S, casilla 03)      {eur(semestre_rn)}")
    print(f"  Falta en el 2o semestre            {eur(falta_semestre)}")
    if falta_semestre <= 0:
        print(f"  YA SUPERAS EL OBJETIVO: te sobran {eur(-falta_semestre)}")
        print("  en el semestre. No necesitas facturar mas para llegar al neto.")
    else:
        print(f"  -> ESTE TRIMESTRE, si lo repartes  {eur(falta_semestre / 2)}")
        print(f"  -> ESTE TRIMESTRE, si lo cargas ya {eur(falta_semestre)}")
        print(f"  Facturacion necesaria este trim.   "
              f"{eur(falta_semestre / 2 + gasto_medio_trim)}")
        print(f"     (rend. neto objetivo + gasto medio trimestral "
              f"{eur(gasto_medio_trim).strip()})")

    # Escenario B: subir la nomina de la SL, actividad intacta.
    def neto_via_nomina(bruto):
        base = rn_actividad_anual + rendimiento_neto_trabajo(bruto, reta_aparte)
        return rn_actividad_anual + bruto - reta_aparte - cuota_irpf(base)

    print("\nB) Subiendo la nomina de la SL (actividad intacta)")
    if neto_via_nomina(0.0) >= neto_objetivo_anual:
        print("  Solo con la actividad ya superas el objetivo: no hace falta")
        print("  subir la nomina. Cualquier subida va por encima de los "
              f"{objetivo_neto_mes:,.0f} EUR/mes.".replace(",", "."))
    else:
        bruto_necesario = resuelve_bruto(neto_objetivo_anual, neto_via_nomina)
        subida = bruto_necesario - bruto_nomina_anual
        tipo_is = cfg.get("tipo_impuesto_sociedades", 0.23)
        print(f"  Nomina bruta anual necesaria       {eur(bruto_necesario)}")
        print(f"  Nomina bruta mensual (x12)         "
              f"{eur(bruto_necesario / MESES_ANO)}")
        if subida >= 0:
            print(f"  SUBIDA sobre la nomina actual      {eur(subida)}")
            print(f"  Ahorro en Sociedades al {100 * tipo_is:.0f}%        "
                  f"{eur(subida * tipo_is)}")
            print("     (la nomina es gasto deducible en el IS de la SL)")
        else:
            print(f"  BAJADA posible sobre la actual     {eur(-subida)}")
            print("  Con tu actividad ya cubres el objetivo casi entero: esa")
            print("  parte de la nomina puedes dejarla en la SL (tributa al")
            print(f"  {100 * tipo_is:.0f}% de Sociedades en vez de a tu marginal de IRPF).")

    if cuota_deuda:
        ratio_obj = 100 * cuota_deuda / objetivo_neto_mes
        print(f"\n  Ratio de endeudamiento con {objetivo_neto_mes:,.0f} EUR/mes: "
              f"{ratio_obj:.2f} %".replace(",", "."))

    linea("AVISOS")
    print("  - La proyeccion anual multiplica el semestre x2. Si tu")
    print("    facturacion es estacional, sustituyela por tu previsión real.")
    print("  - El 20% del modelo 130 es un pago a cuenta, NO el IRPF final.")
    print("    Aqui se usa el IRPF anual por escala, que es el que manda.")
    print("  - La escala autonomica varia por CCAA: ajusta irpf.py si hace falta.")
    print("  - Estimacion orientativa; confirma con tu asesor antes de decidir.")


EJEMPLO = {
    "_nota": "CIFRAS INVENTADAS. Sustituyelas por las tuyas.",
    "modelo_130": {
        "previo": {"ingresos": 20000.0, "gastos": 7000.0},
        "actual": {"ingresos": 42000.0, "gastos": 15000.0},
    },
    "modelo_303": {
        "previo": {"base_devengada": 20000.0, "base_soportada": 7000.0},
        "actual": {"base_devengada": 22000.0, "base_soportada": 8000.0},
    },
    "nomina_sl": {"bruto_anual": 12000.0},
    "deudas_mensuales": {
        "hipoteca": 950.0,
        "prestamo_coche": 280.0,
        "tarjetas": 0.0,
    },
    "objetivo_neto_mensual": 5000.0,
    "config": {
        "reta_pagada_fuera_de_gastos_anual": 0.0,
        "tipo_impuesto_sociedades": 0.23,
    },
}


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    if args[0] == "--ejemplo":
        print("*** EJEMPLO CON CIFRAS INVENTADAS ***")
        analiza(EJEMPLO)
        return 0
    with open(args[0], encoding="utf-8") as fh:
        analiza(json.load(fh))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
