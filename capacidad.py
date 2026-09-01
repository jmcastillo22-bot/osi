#!/usr/bin/env python3
"""Capacidad de endeudamiento con ratio de partida del 0%.

Sin cuotas de deuda vivas, el ratio actual es 0% y todo el margen del
umbral bancario (35% por defecto) esta disponible. Lo que limita no es
la deuda previa, sino el ingreso neto acreditable.

Uso:  python3 capacidad.py [umbral_ratio]   (por defecto 0.35)
"""

import sys

from irpf import cuota_irpf

# --- Datos reales del ejercicio 2026 ----------------------------------------
RN_1S = 8641.08          # casilla 03 del modelo 130 del 2T (acumulado)
GASTOS_1S = 6358.92      # casilla 02 del modelo 130 del 2T (acumulado)
SL_DISPONIBLE_1S = 33115.57   # ventas SL - costes con terceros
OBJETIVO_MES = 5000.00

ESCENARIOS_HIPOTECA = [(0.025, 30), (0.030, 30), (0.030, 25), (0.035, 25)]


def eur(x):
    return f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def neto_mensual(rn_anual):
    return (rn_anual - cuota_irpf(max(0.0, rn_anual))) / 12


def principal(cuota, tipo_anual, anos):
    """Capital de un prestamo frances para una cuota mensual dada."""
    i, n = tipo_anual / 12, anos * 12
    return cuota * (1 - (1 + i) ** -n) / i


def main():
    umbral = float(sys.argv[1]) if len(sys.argv) > 1 else 0.35

    print("=" * 70)
    print(" Capacidad de endeudamiento - Jose Maria Castillo")
    print(f" Ratio actual: 0,00 % (sin cuotas de deuda) | umbral {umbral:.0%}")
    print("=" * 70)

    # Tres niveles de ingreso: el real, el techo de la estructura, el objetivo.
    rn_real = RN_1S * 2                              # proyeccion del 1S
    rn_techo = SL_DISPONIBLE_1S * 2 - GASTOS_1S * 2  # todo lo que da la SL
    niveles = [
        ("Ritmo real del 1S", neto_mensual(rn_real)),
        ("Techo de la SL hoy", neto_mensual(rn_techo)),
        ("Objetivo declarado", OBJETIVO_MES),
    ]

    seccion("1. CUOTA MAXIMA SEGUN INGRESO ACREDITADO")
    print(f"  {'Escenario':<22}{'Neto/mes':>13}{'Cuota max':>13}")
    print(f"  {'-' * 48}")
    for etiqueta, neto in niveles:
        print(f"  {etiqueta:<22}{eur(neto):>13}{eur(neto * umbral):>13}")

    seccion("2. CAPITAL FINANCIABLE CON ESA CUOTA")
    cab = "".join(f"{f'{t:.1%}/{a}a':>13}" for t, a in ESCENARIOS_HIPOTECA)
    print(f"  {'Escenario':<22}{cab}")
    print(f"  {'-' * (22 + 13 * len(ESCENARIOS_HIPOTECA))}")
    for etiqueta, neto in niveles:
        cuota = neto * umbral
        fila = "".join(f"{eur(principal(cuota, t, a)):>13}"
                       for t, a in ESCENARIOS_HIPOTECA)
        print(f"  {etiqueta:<22}{fila}")

    seccion("3. LECTURA")
    neto_real, neto_techo = niveles[0][1], niveles[1][1]
    print(f"  Con el ritmo actual acreditas {eur(neto_real)} EUR/mes: el banco")
    print(f"  te admitiria una cuota de {eur(neto_real * umbral)} EUR.")
    print(f"\n  Exprimiendo toda la facturacion de la SL llegarias a")
    print(f"  {eur(neto_techo)} EUR/mes netos, o sea una cuota de")
    print(f"  {eur(neto_techo * umbral)} EUR. Ese es el techo real de tu")
    print("  estructura mientras la SL facture lo que factura.")
    print(f"\n  Los {eur(OBJETIVO_MES)} EUR/mes requieren facturar mas en la SL,")
    print("  no repartir distinto lo que ya entra.")
    print("\n  AVISO: el banco pondera tambien antiguedad, estabilidad y el")
    print("  historico de dos ejercicios. Un 2026 irregular (2T a cero) pesa")
    print("  en contra aunque el ratio sea 0%.")


if __name__ == "__main__":
    main()
