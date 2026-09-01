#!/usr/bin/env python3
"""Cifra realista de facturacion para maximizar la hipoteca.

Datos reales del ejercicio 2026:
  modelo 130 (51689568N)  c.01 15.000,00 / c.02 6.358,92 / c.03 8.641,08 (2T acum.)
  modelo 303 SL (B22831267)  ventas 50.131,33 / compras 32.015,76 (1S)
  cuota RETA declarada por el contribuyente: 88 EUR/mes (tarifa plana)

Uso:  python3 maximo_hipoteca.py [umbral_ratio]
"""

import sys

from irpf import cuota_irpf

RETA_MES = 88.00
GASTOS_1S = 6358.92          # casilla 02 del 130, 2T acumulado
INGRESOS_1S = 15000.00       # casilla 01 del 130, 2T acumulado
SL_VENTAS_1S = 50131.33
SL_COMPRAS_1S = 32015.76
UMBRAL = 0.35

ESCENARIOS = [(0.025, 30), (0.030, 30), (0.030, 25), (0.035, 25)]


def eur(x):
    return f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def principal(cuota, tipo, anos):
    i, n = tipo / 12, anos * 12
    return cuota * (1 - (1 + i) ** -n) / i


def main():
    umbral = float(sys.argv[1]) if len(sys.argv) > 1 else UMBRAL

    print("=" * 78)
    print(" Cifra realista para maximizar la hipoteca - ejercicio 2026")
    print(f" RETA 88 EUR/mes | ratio de partida 0% | umbral {umbral:.0%}")
    print("=" * 78)

    # --- 1. Capacidad real de la SL --------------------------------------
    seccion("1. LO QUE LA SL PUEDE PAGARTE EN TODO 2026")
    costes_terceros_1s = SL_COMPRAS_1S - INGRESOS_1S
    disponible_1s = SL_VENTAS_1S - costes_terceros_1s
    disponible_ano = disponible_1s * 2
    resto_2s = disponible_ano - INGRESOS_1S
    print(f"  Ventas SL 1S                         {eur(SL_VENTAS_1S):>12}")
    print(f"  Costes con terceros 1S               {eur(costes_terceros_1s):>12}")
    print(f"  Disponible para retribuirte 1S       {eur(disponible_1s):>12}")
    print(f"  Proyectado a 2026 completo (x2)      {eur(disponible_ano):>12}")
    print(f"  Ya facturado por ti en el 1S         {eur(INGRESOS_1S):>12}")
    print(f"  QUEDA POR FACTURAR EN EL 2S          {eur(resto_2s):>12}")
    print(f"    repartido entre 3T y 4T            {eur(resto_2s / 2):>12}")

    # --- 2. Escenarios ----------------------------------------------------
    gastos_ano = GASTOS_1S * 2
    reta_ano = RETA_MES * 12

    def perfil(ingresos):
        rn = ingresos - gastos_ano - reta_ano
        irpf = cuota_irpf(max(0.0, rn))
        return rn, irpf, (rn - irpf) / 12, rn / 12

    escenarios = [
        ("Ritmo actual (sin 2S)", INGRESOS_1S * 2),
        ("REALISTA (techo SL)", disponible_ano),
        ("Objetivo 5.000 netos", 0.0),  # se calcula abajo
    ]

    # Ingresos necesarios para 5.000 EUR/mes netos.
    from irpf import resuelve_bruto
    rn_obj = resuelve_bruto(60000.0, lambda r: r - cuota_irpf(max(0.0, r)))
    escenarios[2] = ("Objetivo 5.000 netos", rn_obj + gastos_ano + reta_ano)

    seccion("2. QUE ACREDITAS EN CADA ESCENARIO")
    print(f"  {'Escenario':<24}{'Facturar/ano':>14}{'Rend. neto':>13}"
          f"{'Neto/mes':>11}{'R.neto/mes':>12}")
    print(f"  {'-' * 74}")
    perfiles = []
    for etiqueta, ingresos in escenarios:
        rn, irpf, neto_mes, rn_mes = perfil(ingresos)
        perfiles.append((etiqueta, ingresos, rn, neto_mes, rn_mes))
        print(f"  {etiqueta:<24}{eur(ingresos):>14}{eur(rn):>13}"
              f"{eur(neto_mes):>11}{eur(rn_mes):>12}")

    # --- 3. Hipoteca -------------------------------------------------------
    seccion("3. HIPOTECA SEGUN EL CRITERIO DEL BANCO (cuota al 35%)")
    for criterio, idx in (("A) Neto despues de IRPF (conservador)", 3),
                          ("B) Rendimiento neto / 12 (mas favorable)", 4)):
        print(f"\n  {criterio}")
        cab = "".join(f"{f'{t:.1%}/{a}a':>12}" for t, a in ESCENARIOS)
        print(f"  {'Escenario':<24}{'Cuota max':>11}{cab}")
        print(f"  {'-' * (35 + 12 * len(ESCENARIOS))}")
        for p in perfiles:
            base = p[idx]
            cuota = base * umbral
            fila = "".join(f"{eur(principal(cuota, t, a)):>12}"
                           for t, a in ESCENARIOS)
            print(f"  {p[0]:<24}{eur(cuota):>11}{fila}")

    # --- 4. Respuesta ------------------------------------------------------
    seccion("4. LA CIFRA")
    _, ingresos_r, rn_r, neto_r, rnmes_r = perfiles[1]
    print(f"  Factura en el 3T:                    {eur(resto_2s / 2):>12}")
    print(f"  Y otro tanto en el 4T:               {eur(resto_2s / 2):>12}")
    print(f"  Total facturado en 2026:             {eur(ingresos_r):>12}")
    print(f"  Rendimiento neto (c.03 de cierre):   {eur(rn_r):>12}")
    print(f"  Acreditas:  {eur(neto_r)} EUR/mes netos")
    print(f"              {eur(rnmes_r)} EUR/mes de rendimiento neto")
    print(f"\n  Cuota asumible: {eur(neto_r * umbral)} - {eur(rnmes_r * umbral)} EUR")
    lo = principal(neto_r * umbral, 0.030, 30)
    hi = principal(rnmes_r * umbral, 0.030, 30)
    print(f"  HIPOTECA al 3% a 30 anos: {eur(lo)} - {eur(hi)} EUR")


if __name__ == "__main__":
    main()
