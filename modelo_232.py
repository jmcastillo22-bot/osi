#!/usr/bin/env python3
"""Umbrales del modelo 232 y coste de intentar quedarse por debajo.

Los umbrales del articulo 13.4 RIS se calculan sobre el CONJUNTO DE
OPERACIONES DEL PERIODO IMPOSITIVO, es decir sobre el ejercicio completo.
No existe un limite por trimestre.
"""

from irpf import cuota_irpf

INGRESOS_1S = 15000.00
FACTURA_3T = 40000.00
GASTOS_ANO = 6358.92 * 2
RETA_ANO = 88.00 * 12
UMBRAL_RATIO = 0.35

# Cifra de negocios de la SL en 2026 segun ritmo del 2S
SL_1S = 33891.33 + 16240.00
ESCENARIOS = [
    ("Prudente (interior al ritmo del 2T)", 16240.00 * 2 + 28000.00, 61579.81),
    ("Central (interior a la media del 1S)", 50131.33 + 28000.00, 79231.14),
]


def eur(x):
    return f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def principal(cuota, tipo=0.030, anos=30):
    i, n = tipo / 12, anos * 12
    return cuota * (1 - (1 + i) ** -n) / i


def perfil(ingresos):
    rn = ingresos - GASTOS_ANO - RETA_ANO
    return rn, (rn - cuota_irpf(max(0.0, rn))) / 12, rn / 12


def main():
    print("=" * 74)
    print(" Modelo 232: umbrales reales y coste de esquivarlos")
    print("=" * 74)

    seccion("1. EL UMBRAL ES ANUAL, NO TRIMESTRAL")
    print("  Art. 13.4 RIS. Hay que presentar el 232 cuando, EN EL PERIODO")
    print("  IMPOSITIVO (el ejercicio entero), se da alguno de estos casos:")
    print()
    print("    a) operaciones con la misma persona vinculada > 250.000 EUR")
    print("    b) operaciones especificas > 100.000 EUR")
    print("    c) operaciones del mismo tipo y metodo de valoracion que")
    print("       superen el 50% de la cifra de negocios de la entidad")
    print()
    print("  No se mira trimestre a trimestre: el 3T y el 4T SE SUMAN.")
    print(f"  Con {eur(FACTURA_3T)} en el 3T ya llevarias "
          f"{eur(INGRESOS_1S + FACTURA_3T)} en el ano.")

    seccion("2. CUANTO TE CABE EN EL 4T SIN CRUZAR EL 50%")
    print(f"  {'Escenario':<38}{'Cifra neg.':>13}{'50%':>12}{'Cabe 4T':>12}")
    print(f"  {'-' * 75}")
    margenes = []
    for etq, sl_2s, margen_2s in ESCENARIOS:
        cifra = SL_1S + sl_2s
        umbral = cifra * 0.50
        cabe = umbral - (INGRESOS_1S + FACTURA_3T)
        margenes.append((etq, cifra, umbral, cabe, margen_2s))
        print(f"  {etq:<38}{eur(cifra):>13}{eur(umbral):>12}{eur(cabe):>12}")
    print("\n  Es decir: para no presentar el 232 tendrias que renunciar a")
    print("  casi todo el 4T. La a) de 250.000 no la rozas en ningun caso.")

    seccion("3. LO QUE CUESTA ESQUIVARLO")
    print(f"  {'Escenario':<24}{'Facturado':>13}{'R.neto/mes':>12}"
          f"{'Neto/mes':>11}{'Hipoteca 3%/30a':>28}")
    print(f"  {'-' * 88}")
    for etq, cifra, umbral, cabe, margen_2s in margenes:
        corto = etq.split(" (")[0]
        for modo, ingresos in (("tope 232", umbral),
                               ("sin tope", INGRESOS_1S + margen_2s)):
            rn, neto_mes, rn_mes = perfil(ingresos)
            rango = (f"{eur(principal(neto_mes * UMBRAL_RATIO))} - "
                     f"{eur(principal(rn_mes * UMBRAL_RATIO))}")
            print(f"  {corto + ' / ' + modo:<24}{eur(ingresos):>13}"
                  f"{eur(rn_mes):>12}{eur(neto_mes):>11}{rango:>28}")

    seccion("4. LA CUENTA")
    for etq, cifra, umbral, cabe, margen_2s in margenes:
        _, neto_tope, rnmes_tope = perfil(umbral)
        _, neto_libre, rnmes_libre = perfil(INGRESOS_1S + margen_2s)
        dif_lo = principal(neto_libre * UMBRAL_RATIO) - principal(neto_tope * UMBRAL_RATIO)
        dif_hi = principal(rnmes_libre * UMBRAL_RATIO) - principal(rnmes_tope * UMBRAL_RATIO)
        print(f"  {etq.split(' (')[0]}: quedarte por debajo del 50% te cuesta")
        print(f"    entre {eur(dif_lo)} y {eur(dif_hi)} de hipoteca.")

    seccion("5. Y QUE GANAS A CAMBIO: NADA")
    print("  El 232 es una DECLARACION INFORMATIVA. No liquida impuesto, no")
    print("  cuesta dinero, no abre inspeccion por si mismo. Se presenta en")
    print("  noviembre del ano siguiente y ya esta.")
    print()
    print("  Y lo importante: la obligacion de valorar a precio de mercado")
    print("  (art. 18 LIS) y de tener documentacion que lo sostenga se aplica")
    print("  IGUAL estes por encima o por debajo del umbral. El 232 solo")
    print("  determina si ademas hay que DECLARARLO, no si las reglas rigen.")
    print()
    print("  >> Recortar la facturacion del 4T para no presentar un formulario")
    print("     te cuesta seis cifras de hipoteca y no te ahorra ni un euro")
    print("     de impuestos ni una sola obligacion.")


if __name__ == "__main__":
    main()
