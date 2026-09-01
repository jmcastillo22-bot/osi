#!/usr/bin/env python3
"""Cuanto facturar en el 3T de 2026 para acreditar 5.000 EUR/mes de media.

Datos leidos de los modelos 303 presentados (ejercicio 2026, 1T y 2T):

  - JOSE MARIA CASTILLO, NIF 51689568N        -> actividad como autonomo
  - OSI GLOBAL CONSULTING SL, NIF B22831267   -> la sociedad

Uso:  python3 objetivo_3t.py [cuota_reta_mensual]
"""

import sys

from irpf import cuota_irpf, resuelve_bruto

# --- Modelo 303 del autonomo (51689568N) ------------------------------------
# 1T: casilla 07 base 21% = 15.000,00 / casilla 27 = 3.196,77 / c.71 = 2.674,86
# 2T: casilla 27 EN BLANCO -> facturacion cero / c.71 = -809,77 a compensar
AUTONOMO = {
    "1T": {"ventas": 15000.00, "compras": 2497.78, "resultado": 2674.86},
    "2T": {"ventas": 0.00, "compras": 3856.04, "resultado": -809.77},
}

# --- Modelo 303 de la SL (B22831267) ----------------------------------------
# casilla 122 = ventas por inversion del sujeto pasivo; casilla 27 = 0
SL = {
    "1T": {"ventas": 33891.33, "compras": 16459.62},
    "2T": {"ventas": 16240.00, "compras": 15556.14},
}

OBJETIVO_MES = 5000.00
RETA_MENSUAL_POR_DEFECTO = 600.00  # ajustable por argumento


def eur(x):
    return f"{x:>13,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def main():
    reta_mes = float(sys.argv[1]) if len(sys.argv) > 1 else RETA_MENSUAL_POR_DEFECTO

    print("=" * 74)
    print(" 3T 2026 - cuanto cobrar para acreditar 5.000 EUR/mes de media")
    print(" Jose Maria Castillo (51689568N) / OSI Global Consulting SL")
    print("=" * 74)

    # --- 1. Situacion del autonomo en el 1S ---------------------------------
    seccion("1. TU ACTIVIDAD COMO AUTONOMO (303 del 1T y 2T)")
    print(f"{'':<6}{'Facturado':>14}{'Gastos c/IVA':>15}{'Result. 303':>14}")
    for q, t in AUTONOMO.items():
        print(f"{q:<6}{eur(t['ventas'])}{eur(t['compras'])[:15]:>15}"
              f"{eur(t['resultado'])[:14]:>14}")
    ventas_1s = sum(t["ventas"] for t in AUTONOMO.values())
    compras_1s = sum(t["compras"] for t in AUTONOMO.values())
    reta_1s = reta_mes * 6
    rn_1s = ventas_1s - compras_1s - reta_1s
    print(f"{'1S':<6}{eur(ventas_1s)}{eur(compras_1s)[:15]:>15}")
    print(f"\n  Facturado en el semestre           {eur(ventas_1s)}")
    print(f"  Gastos con IVA (casilla 28)        {eur(compras_1s)}")
    print(f"  Cuota RETA estimada ({reta_mes:.0f}/mes x6)  {eur(reta_1s)}")
    print(f"  RENDIMIENTO NETO del semestre      {eur(rn_1s)}")
    print(f"  Equivalente mensual                {eur(rn_1s / 6)}")
    print("\n  >> El 2T lo has facturado a CERO. Esa es la raiz del problema:")
    print("     seis meses de actividad sostenidos por un solo trimestre.")

    # --- 2. Neto ya percibido ------------------------------------------------
    seccion("2. NETO YA PERCIBIDO EN EL 1S (despues de IRPF)")
    # El IRPF es anual: esta es la cuota que corresponderia si el ejercicio
    # cerrase hoy con este rendimiento (no es un prorrateo del trimestre).
    irpf_1s = cuota_irpf(max(0.0, rn_1s))
    neto_1s = rn_1s - irpf_1s
    print(f"  Rendimiento neto 1S                {eur(rn_1s)}")
    print(f"  IRPF si el ano cerrase hoy         {eur(irpf_1s)}")
    print(f"  NETO EN BOLSILLO 1S                {eur(neto_1s)}")
    print(f"  Media mensual real del 1S          {eur(neto_1s / 6)}")

    # --- 3. Objetivo segun la ventana que mire el banco ---------------------
    seccion("3. CUANTO FACTURAR EN EL 3T, SEGUN LA VENTANA DEL BANCO")

    def neto_anual(rn):
        return rn - cuota_irpf(max(0.0, rn))

    gasto_trim = compras_1s / 2 + reta_mes * 3

    print(f"  Gasto estimado del 3T (media 1S + RETA)  {eur(gasto_trim)}\n")
    print(f"  {'Ventana':<28}{'Neto objetivo':>15}{'Falta neto':>14}"
          f"{'A FACTURAR 3T':>16}")
    print(f"  {'-' * 71}")

    ventanas = [
        ("Ano natural 2026 (12 meses)", 12),
        ("Enero-septiembre (9 meses)", 9),
        ("Solo el 3T (3 meses)", 3),
    ]
    for etiqueta, meses in ventanas:
        neto_obj = OBJETIVO_MES * meses
        # Ventanas de 9 y 12 meses: el objetivo absorbe lo ya percibido.
        # Ventana del 3T aislado: el objetivo se suma a lo ya percibido.
        neto_total_objetivo = neto_obj if meses > 3 else neto_1s + neto_obj
        falta = neto_total_objetivo - neto_1s
        # Siempre sobre el total anual: el IRPF es progresivo, no trimestral.
        rn_total = resuelve_bruto(neto_total_objetivo, neto_anual)
        rn_3t = rn_total - rn_1s
        facturar = rn_3t + gasto_trim
        print(f"  {etiqueta:<28}{eur(neto_obj)[:15]:>15}{eur(falta)[:14]:>14}"
              f"{eur(facturar)[:16]:>16}")

    # --- 4. Puede la SL pagarlo? --------------------------------------------
    seccion("4. PUEDE TU SL PAGARTELO?")
    sl_ventas = sum(t["ventas"] for t in SL.values())
    sl_compras = sum(t["compras"] for t in SL.values())
    # De las compras de la SL, 15.000 son tu factura del 1T.
    sl_compras_ajenas = sl_compras - ventas_1s
    disponible_1s = sl_ventas - sl_compras_ajenas
    print(f"  Ventas de la SL en el 1S (c.122)   {eur(sl_ventas)}")
    print(f"  Compras de la SL en el 1S (c.28)   {eur(sl_compras)}")
    print(f"    de las que son factura tuya      {eur(ventas_1s)}")
    print(f"    costes con terceros              {eur(sl_compras_ajenas)}")
    print(f"  DISPONIBLE para pagarte (1S)       {eur(disponible_1s)}")
    print(f"  Al mismo ritmo, en un trimestre    {eur(disponible_1s / 2)}")
    print("\n  (Sin contar gastos de la SL sin IVA: nominas, seguros,")
    print("   cuotas bancarias. El disponible real sera algo menor.)")

    # --- 5. Veredicto --------------------------------------------------------
    seccion("5. VEREDICTO")
    rn_necesario_ano = resuelve_bruto(OBJETIVO_MES * 12, neto_anual)
    facturar_ano = rn_necesario_ano - rn_1s + gasto_trim
    print(f"  Para cerrar 2026 con media de 5.000/mes netos necesitas")
    print(f"  facturar en el 3T:                 {eur(facturar_ano)}")
    print(f"  La SL genera por trimestre:        {eur(disponible_1s / 2)}")
    brecha = facturar_ano - disponible_1s / 2
    if brecha > 0:
        print(f"  BRECHA                             {eur(brecha)}")
        print("\n  >> No sale con la facturacion actual. Para acreditar")
        print("     5.000/mes de media en 2026 la SL tendria que facturar")
        print(f"     bastante mas de lo que lleva, o hay que rebajar el")
        print("     objetivo o ampliar la ventana que mira el banco.")
    else:
        print(f"  Holgura                            {eur(-brecha)}")

    print("\n  AVISOS")
    print("  - Falta el modelo 130: los gastos reales pueden ser mayores que")
    print("    la casilla 28 (hay gastos deducibles sin IVA).")
    print(f"  - Cuota RETA asumida en {reta_mes:.0f} EUR/mes. Pasala como argumento")
    print("    si la tuya es otra:  python3 objetivo_3t.py 750")
    print("  - Estimacion orientativa; contrastala con tu asesor.")


if __name__ == "__main__":
    main()
