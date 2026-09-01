#!/usr/bin/env python3
"""Quien factura al cliente irlandes: tu o la SL. Las dos estructuras.

A) La SL factura a Irlanda. Tu solo facturas a la SL.
B) TU facturas a Irlanda directamente, ademas de a la SL.

Cambia tu 130, tu 303, la retencion, el umbral del 232 y la hipoteca.
"""

from irpf import cuota_irpf

SL_Q1 = 15000.00          # tu factura a la SL, 1T (21% IVA + 7% retencion)
SL_Q3 = 40000.00          # tu factura a la SL, 30 de septiembre
IRL_Q3 = 11000.00         # 12 de septiembre
IRL_Q4 = 17000.00         # cobro 12 de octubre
GASTOS_1S = 6358.92
GASTOS_ANO = GASTOS_1S * 2
RETA_ANO = 88.00 * 12
RETENCION = 0.07
UMBRAL = 0.35
PAGO_1T, NEG_2T = 1234.83, 556.61
SL_INTERIOR_2026 = 50131.33 + 16240.00 * 2   # ritmo prudente


def eur(x):
    return f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def principal(cuota, tipo=0.030, anos=30):
    i, n = tipo / 12, anos * 12
    return cuota * (1 - (1 + i) ** -n) / i


def cierre(ingresos_ano):
    rn = ingresos_ano - GASTOS_ANO - RETA_ANO
    return rn, (rn - cuota_irpf(max(0.0, rn))) / 12, rn / 12


def m130_3t(ing_3t_acum, base_con_retencion):
    """Modelo 130 del 3T: rendimiento neto acumulado y pago fraccionado."""
    rn = ing_3t_acum - (GASTOS_1S + GASTOS_1S / 2)
    c07 = rn * 0.20 - PAGO_1T - base_con_retencion * RETENCION
    return rn, max(0.0, max(0.0, c07) - NEG_2T)


def main():
    print("=" * 76)
    print(" Quien factura al cliente irlandes: dos estructuras")
    print("=" * 76)

    # ---------------- Estructura A ----------------
    seccion("A) LA SL FACTURA A IRLANDA (lo que he venido asumiendo)")
    ing_a_3t = SL_Q1 + SL_Q3
    rn_a3, pago_a3 = m130_3t(ing_a_3t, ing_a_3t)
    print(f"  Tus ingresos son solo tus facturas a la SL.")
    print(f"  130 del 3T:  c.01 {eur(ing_a_3t)}   c.03 {eur(rn_a3)}")
    print(f"               rend. neto / 9 meses  {eur(rn_a3 / 9)}")
    print(f"               a ingresar            {eur(pago_a3)}")
    print(f"  303 del 3T:  repercutes 21% sobre {eur(SL_Q3)} = "
          f"{eur(SL_Q3 * 0.21)}")
    print(f"  Retencion:   7% sobre todo ({eur(ing_a_3t * RETENCION)})")
    ing_a_ano = SL_Q1 + 61579.81      # margen prudente del 2S
    rn_a, neto_a, rnmes_a = cierre(ing_a_ano)
    print(f"\n  Cierre 2026 agotando el margen de la SL:")
    print(f"    facturado {eur(ing_a_ano)}   rend. neto {eur(rn_a)}")
    print(f"    {eur(neto_a)}/mes neto   {eur(rnmes_a)}/mes rend. neto")
    print(f"    hipoteca {eur(principal(neto_a * UMBRAL))} - "
          f"{eur(principal(rnmes_a * UMBRAL))}")

    # ---------------- Estructura B ----------------
    seccion("B) TU FACTURAS A IRLANDA DIRECTAMENTE")
    ing_b_3t = SL_Q1 + SL_Q3 + IRL_Q3
    rn_b3, pago_b3 = m130_3t(ing_b_3t, SL_Q1 + SL_Q3)
    print(f"  Sumas a tus ingresos las facturas a Irlanda, sin IVA")
    print(f"  y SIN RETENCION (un cliente irlandes no retiene IRPF espanol).")
    print(f"  130 del 3T:  c.01 {eur(ing_b_3t)}   c.03 {eur(rn_b3)}")
    print(f"               rend. neto / 9 meses  {eur(rn_b3 / 9)}")
    print(f"               a ingresar            {eur(pago_b3)}")
    print(f"  303 del 3T:  repercutes 21% solo sobre la factura a la SL")
    print(f"               los {eur(IRL_Q3)} van a la CASILLA 59 + modelo 349")
    print(f"  Retencion:   7% solo sobre {eur(SL_Q1 + SL_Q3)} = "
          f"{eur((SL_Q1 + SL_Q3) * RETENCION)}")
    ing_b_ano = SL_Q1 + SL_Q3 + IRL_Q3 + IRL_Q4
    rn_b, neto_b, rnmes_b = cierre(ing_b_ano)
    print(f"\n  Cierre 2026 sin facturar nada mas a la SL:")
    print(f"    facturado {eur(ing_b_ano)}   rend. neto {eur(rn_b)}")
    print(f"    {eur(neto_b)}/mes neto   {eur(rnmes_b)}/mes rend. neto")
    print(f"    hipoteca {eur(principal(neto_b * UMBRAL))} - "
          f"{eur(principal(rnmes_b * UMBRAL))}")

    # ---------------- Comparativa ----------------
    seccion("COMPARATIVA")
    print(f"  {'':<26}{'A) factura la SL':>22}{'B) facturas tu':>22}")
    print(f"  {'-' * 70}")
    filas = [
        ("Rend. neto 3T / 9 meses", rn_a3 / 9, rn_b3 / 9),
        ("Pago del 130 en el 3T", pago_a3, pago_b3),
        ("Facturado en 2026", ing_a_ano, ing_b_ano),
        ("Rend. neto/mes del ano", rnmes_a, rnmes_b),
        ("Neto/mes del ano", neto_a, neto_b),
    ]
    for etq, a, b in filas:
        print(f"  {etq:<26}{eur(a):>22}{eur(b):>22}")

    # ---------------- Efecto en el 232 ----------------
    seccion("EFECTO EN EL MODELO 232")
    for etq, cifra_sl, tus_facturas in (
            ("A", SL_INTERIOR_2026 + IRL_Q3 + IRL_Q4, SL_Q1 + 61579.81),
            ("B", SL_INTERIOR_2026, SL_Q1 + SL_Q3)):
        umbral = cifra_sl * 0.50
        estado = "SE SUPERA" if tus_facturas > umbral else "no se supera"
        print(f"  {etq})  cifra de negocios SL {eur(cifra_sl)}  "
              f"50% {eur(umbral)}")
        print(f"      tus facturas a la SL {eur(tus_facturas)}  -> {estado}")
    print("\n  >> En B la SL factura menos (no tiene los ingresos irlandeses),")
    print("     asi que el umbral del 50% BAJA y lo cruzas con mas holgura.")

    seccion("EN AMBOS CASOS, SI FACTURAS TU A IRLANDA")
    print("  - Alta en el ROI y NIF-IVA propio validado en VIES, a tu nombre")
    print("    de autonomo, no el de la SL.")
    print("  - Casilla 59 de TU 303 y TU modelo 349.")
    print("  - Sin retencion: el pago fraccionado del 130 sube, porque no hay")
    print("    7% adelantado sobre esa parte. Preve la caja.")


if __name__ == "__main__":
    main()
