#!/usr/bin/env python3
"""Efecto de las facturas previstas del 2S sobre lo que puedes acreditar.

Facturas comunicadas:
    11.000 EUR  -  12 de septiembre  -> 3T
    17.000 EUR  -  cobro 12 octubre  -> 4T si se emite en octubre,
                                        3T si se emite en septiembre

Datos de partida (ejercicio 2026, ya presentados):
    modelo 130   c.01 15.000,00 / c.02 6.358,92 / c.03 8.641,08  (2T acum.)
    modelo 303 SL   ventas 50.131,33 / compras 32.015,76  (1S)
    RETA 88 EUR/mes
"""

from irpf import cuota_irpf

FACT_3T = 11000.00
FACT_4T = 17000.00
INGRESOS_1S = 15000.00
GASTOS_1S = 6358.92
RETA_MES = 88.00
SL_VENTAS_1S = 50131.33
SL_COMPRAS_1S = 32015.76
UMBRAL = 0.35


def eur(x):
    return f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def principal(cuota, tipo=0.030, anos=30):
    i, n = tipo / 12, anos * 12
    return cuota * (1 - (1 + i) ** -n) / i


def perfil(ingresos_ano, gastos_ano):
    rn = ingresos_ano - gastos_ano - RETA_MES * 12
    irpf = cuota_irpf(max(0.0, rn))
    return rn, irpf, (rn - irpf) / 12, rn / 12


def informe(titulo, ingresos_ano, gastos_ano):
    rn, irpf, neto_mes, rn_mes = perfil(ingresos_ano, gastos_ano)
    print(f"\n  {titulo}")
    print(f"    Facturado en 2026                {eur(ingresos_ano):>12}")
    print(f"    Gastos + RETA                    {eur(gastos_ano + RETA_MES * 12):>12}")
    print(f"    Rendimiento neto (c.03 cierre)   {eur(rn):>12}")
    print(f"    IRPF                             {eur(irpf):>12}")
    print(f"    Acreditas neto/mes               {eur(neto_mes):>12}")
    print(f"    Acreditas rend.neto/mes          {eur(rn_mes):>12}")
    print(f"    Hipoteca 3%/30a (neto - r.neto)  "
          f"{eur(principal(neto_mes * UMBRAL))} - "
          f"{eur(principal(rn_mes * UMBRAL))}")
    return rn, neto_mes, rn_mes


def main():
    gastos_ano = GASTOS_1S * 2  # se mantiene el ritmo de gasto del 1S

    print("=" * 76)
    print(" Facturas del 2S: 11.000 (12-sep) + 17.000 (cobro 12-oct)")
    print("=" * 76)

    # --- Lectura A: son TUS facturas a la SL -----------------------------
    seccion("LECTURA A: son tus facturas de autonomo a la SL")
    ingresos = INGRESOS_1S + FACT_3T + FACT_4T
    rn_a, neto_a, rnmes_a = informe(
        f"Facturas por {eur(INGRESOS_1S)} (1S) + {eur(FACT_3T)} (3T) "
        f"+ {eur(FACT_4T)} (4T)",
        ingresos, gastos_ano)

    print("\n    Facturacion por trimestre:")
    for etq, imp in (("1T", INGRESOS_1S), ("2T", 0.0),
                     ("3T", FACT_3T), ("4T", FACT_4T)):
        print(f"      {etq}  {eur(imp):>10}")

    # --- Cuanto margen queda sin usar ------------------------------------
    seccion("MARGEN QUE DEJAS SIN USAR")
    costes_terceros = SL_COMPRAS_1S - INGRESOS_1S
    disponible_ano = (SL_VENTAS_1S - costes_terceros) * 2
    sin_usar = disponible_ano - ingresos
    print(f"  La SL puede pagarte en 2026 (proyeccion) {eur(disponible_ano):>12}")
    print(f"  Con estas facturas le facturas            {eur(ingresos):>12}")
    print(f"  SIN FACTURAR                              {eur(sin_usar):>12}")
    if sin_usar > 0:
        rn_max, _, neto_max, rnmes_max = perfil(disponible_ano, gastos_ano)
        print(f"\n  Si facturases todo el disponible:")
        print(f"    neto/mes      {eur(neto_max)}  (vs {eur(neto_a)})")
        print(f"    rend.neto/mes {eur(rnmes_max)}  (vs {eur(rnmes_a)})")
        print(f"    hipoteca      {eur(principal(neto_max * UMBRAL))} - "
              f"{eur(principal(rnmes_max * UMBRAL))}")

    # --- Lectura B: son ingresos de la SL --------------------------------
    seccion("LECTURA B: son ventas de la SL a sus clientes")
    sl_ventas_2s = FACT_3T + FACT_4T
    disponible_b = (SL_VENTAS_1S - costes_terceros) + (sl_ventas_2s - costes_terceros)
    tope_b = max(0.0, disponible_b)
    print(f"  Ventas SL 1S                              {eur(SL_VENTAS_1S):>12}")
    print(f"  Ventas SL 2S segun lo que dices           {eur(sl_ventas_2s):>12}")
    print(f"  Costes con terceros por semestre          {eur(costes_terceros):>12}")
    print(f"  Disponible para pagarte en todo 2026      {eur(tope_b):>12}")
    print(f"  Ya facturado por ti en el 1S              {eur(INGRESOS_1S):>12}")
    print(f"  Margen para facturar en el 2S             "
          f"{eur(max(0.0, tope_b - INGRESOS_1S)):>12}")
    informe("Si agotas ese margen", tope_b, gastos_ano)
    print("\n  >> Las ventas del 2S caen a la mitad que en el 1S, asi que")
    print("     bajo esta lectura la capacidad de la SL se reduce bastante.")

    # --- El detalle del devengo ------------------------------------------
    seccion("LA FECHA QUE CUENTA ES LA DE EMISION")
    print("  El IVA y el IRPF se devengan por FECHA DE EMISION, no de cobro")
    print("  (salvo criterio de caja, y en tus 303 no esta marcado).")
    print()
    print("  Factura de 17.000 'para cobrar el 12 de octubre':")
    print("    - emitida en OCTUBRE -> 4T. 303 y 130 del 4T (enero 2027).")
    print("    - emitida en SEPTIEMBRE -> 3T, aunque la cobres en octubre.")
    print()
    print(f"  Si la emites en septiembre, el 3T pasa de {eur(FACT_3T)} a")
    print(f"  {eur(FACT_3T + FACT_4T)}. El total de 2026 no cambia: solo importa")
    print("  si el banco mira un trimestre suelto en vez del ano completo.")

    seccion("PENDIENTE DE ACLARAR")
    print("  Los 11.000 y 17.000, son BASE IMPONIBLE o con IVA incluido?")
    print("  Si llevan el 21% dentro, las bases reales serian:")
    print(f"    11.000 -> {eur(FACT_3T / 1.21)}   17.000 -> {eur(FACT_4T / 1.21)}")
    ingresos_civa = INGRESOS_1S + FACT_3T / 1.21 + FACT_4T / 1.21
    informe("Con los importes tomados como IVA incluido", ingresos_civa, gastos_ano)


if __name__ == "__main__":
    main()
