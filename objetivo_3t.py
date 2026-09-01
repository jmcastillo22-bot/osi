#!/usr/bin/env python3
"""Cuanto facturar en el 3T de 2026 para acreditar 5.000 EUR/mes de media.

Datos leidos de las autoliquidaciones presentadas del ejercicio 2026:

  modelo 130  JOSE MARIA CASTILLO (51689568N)   1T y 2T   -> fuente principal
  modelo 303  JOSE MARIA CASTILLO (51689568N)   1T y 2T   -> contraste
  modelo 303  OSI GLOBAL CONSULTING SL (B22831267)        -> capacidad de pago

Uso:  python3 objetivo_3t.py [reta_mensual_pagada_fuera_del_130]
"""

import sys

from irpf import cuota_irpf, resuelve_bruto

# --- Modelo 130 del autonomo: ACUMULADO desde enero -------------------------
M130 = {
    "1T": {"ingresos": 15000.00, "gastos": 3575.86, "rn": 11424.14, "result": 1234.83},
    "2T": {"ingresos": 15000.00, "gastos": 6358.92, "rn": 8641.08, "result": 0.00},
}

# --- Modelo 303 del autonomo: por trimestre, para contraste -----------------
M303_AUT = {"ventas_1s": 15000.00, "compras_28_1s": 6353.82}

# --- Modelo 303 de la SL: casilla 122 (ventas) y 28 (compras) ---------------
SL = {
    "1T": {"ventas": 33891.33, "compras": 16459.62},
    "2T": {"ventas": 16240.00, "compras": 15556.14},
}

OBJETIVO_MES = 5000.00


def eur(x):
    return f"{x:>13,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def neto_anual(rn):
    """Neto en bolsillo de un rendimiento neto anual, tras IRPF por escala."""
    return rn - cuota_irpf(max(0.0, rn))


def main():
    reta_fuera = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0

    print("=" * 74)
    print(" 3T 2026 - cuanto facturar para acreditar 5.000 EUR/mes netos de media")
    print(" Jose Maria Castillo (51689568N) / OSI Global Consulting SL")
    print("=" * 74)

    # --- 1. El 130, desacumulado ----------------------------------------
    seccion("1. TU MODELO 130 (acumulado) Y EL TRIMESTRE REAL")
    q1, q2 = M130["1T"], M130["2T"]
    d2 = {k: q2[k] - q1[k] for k in ("ingresos", "gastos", "rn")}
    print(f"  {'':<20}{'1T acum.':>13}{'2T acum.':>13}{'2T real':>13}")
    for etiq, k in (("Ingresos (c.01)", "ingresos"), ("Gastos (c.02)", "gastos"),
                    ("Rend. neto (c.03)", "rn")):
        print(f"  {etiq:<20}{eur(q1[k])}{eur(q2[k])}{eur(d2[k])}")
    print(f"\n  Rendimiento neto del semestre (c.03 del 2T) {eur(q2['rn'])}")
    print(f"  Media mensual                               {eur(q2['rn'] / 6)}")
    print("\n  >> El 2T no aporta ingresos: la casilla 01 no se mueve de")
    print("     15.000,00. Solo suma gastos, asi que el rendimiento neto")
    print(f"     acumulado BAJA de {q1['rn']:,.2f} a {q2['rn']:,.2f}.")

    # --- 2. Contraste 130 contra 303 ------------------------------------
    seccion("2. CONTRASTE ENTRE EL 130 Y EL 303")
    print(f"  Ingresos 130 (c.01) 1S        {eur(q2['ingresos'])}")
    print(f"  Ventas 303 1S                 {eur(M303_AUT['ventas_1s'])}")
    print(f"  {'-' * 44}")
    print(f"  Gastos 130 (c.02) 1S          {eur(q2['gastos'])}")
    print(f"  Compras 303 (c.28) 1S         {eur(M303_AUT['compras_28_1s'])}")
    dif = q2["gastos"] - M303_AUT["compras_28_1s"]
    print(f"  Diferencia                    {eur(dif)}")
    print("\n  >> Los ingresos cuadran al centimo. Pero los gastos del 130")
    print(f"     solo superan en {dif:,.2f} EUR a las compras con IVA del 303.")
    print("     La cuota de RETA no soporta IVA: si la estuvieras deduciendo,")
    print("     la diferencia deberia rondar los 3.000-4.000 EUR. REVISALO:")
    print("     podrias estar dejando de deducir tu propia cuota de autonomos.")

    # --- 3. Neto realmente percibido ------------------------------------
    seccion("3. NETO REALMENTE PERCIBIDO EN EL 1S")
    rn_1s = q2["rn"]
    reta_1s = reta_fuera * 6
    irpf_1s = cuota_irpf(max(0.0, rn_1s))
    neto_1s = rn_1s - irpf_1s - reta_1s
    print(f"  Rendimiento neto (c.03)            {eur(rn_1s)}")
    print(f"  IRPF si el ano cerrase hoy         {eur(irpf_1s)}")
    if reta_1s:
        print(f"  RETA pagada fuera del 130          {eur(reta_1s)}")
    print(f"  NETO EN BOLSILLO                   {eur(neto_1s)}")
    print(f"  Media mensual real                 {eur(neto_1s / 6)}")
    print(f"  Ya pagado a cuenta (c.19 del 1T)   {eur(q1['result'])}")

    # --- 4. Objetivo por ventana ----------------------------------------
    seccion("4. CUANTO FACTURAR EN EL 3T, SEGUN LA VENTANA DEL BANCO")
    gasto_trim = q2["gastos"] / 2
    print(f"  Gasto medio por trimestre (c.02 / 2)   {eur(gasto_trim)}\n")
    print(f"  {'Ventana':<30}{'Neto objetivo':>15}{'Rend. neto 3T':>15}"
          f"{'A FACTURAR 3T':>16}")
    print(f"  {'-' * 74}")
    filas = []
    for etiqueta, meses in (("Ano natural 2026 (12 meses)", 12),
                            ("Enero-septiembre (9 meses)", 9),
                            ("Solo el 3T (3 meses)", 3)):
        neto_obj = OBJETIVO_MES * meses
        objetivo_total = neto_obj if meses > 3 else neto_1s + neto_obj
        rn_total = resuelve_bruto(objetivo_total, neto_anual)
        rn_3t = rn_total - rn_1s
        facturar = rn_3t + gasto_trim
        filas.append((etiqueta, facturar))
        print(f"  {etiqueta:<30}{eur(neto_obj)[:15]:>15}{eur(rn_3t)[:15]:>15}"
              f"{eur(facturar)[:16]:>16}")

    # --- 5. Capacidad de la SL ------------------------------------------
    seccion("5. PUEDE TU SL PAGARTELO?")
    sl_v = sum(t["ventas"] for t in SL.values())
    sl_c = sum(t["compras"] for t in SL.values())
    ajenos = sl_c - M303_AUT["ventas_1s"]
    disponible = sl_v - ajenos
    print(f"  Ventas de la SL 1S (c.122)         {eur(sl_v)}")
    print(f"  Compras de la SL 1S (c.28)         {eur(sl_c)}")
    print(f"    de las que son factura tuya      {eur(M303_AUT['ventas_1s'])}")
    print(f"    costes con terceros              {eur(ajenos)}")
    print(f"  DISPONIBLE para pagarte (semestre) {eur(disponible)}")
    print(f"  Equivalente por trimestre          {eur(disponible / 2)}")

    # --- 6. Veredicto ----------------------------------------------------
    seccion("6. VEREDICTO")
    por_trim = disponible / 2
    for etiqueta, facturar in filas:
        brecha = facturar - por_trim
        estado = f"BRECHA {brecha:>12,.2f}" if brecha > 0 else \
            f"CABE, holgura {-brecha:>10,.2f}"
        print(f"  {etiqueta:<30} facturar {facturar:>11,.2f}   {estado}")
    print(f"\n  Capacidad de la SL por trimestre: {por_trim:,.2f} EUR")
    print("  (sin descontar sus gastos sin IVA: nominas, seguros, comisiones)")

    print("\n  AVISOS")
    print("  - La cuota de RETA no aparece deducida en el 130 (ver seccion 2).")
    print("    Si la pagas tu, pasala como argumento: python3 objetivo_3t.py 600")
    print("  - Escala autonomica de referencia; ajustala en irpf.py segun CCAA.")
    print("  - Estimacion orientativa; contrastala con tu asesor.")


if __name__ == "__main__":
    main()
