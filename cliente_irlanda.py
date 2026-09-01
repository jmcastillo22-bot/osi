#!/usr/bin/env python3
"""Efecto del nuevo cliente irlandes sobre lo que puedes acreditar en 2026.

El cliente es NUEVO, asi que sus 28.000 EUR se SUMAN a la facturacion
interior de la SL, no la sustituyen.

    11.000 EUR  factura de 12 de septiembre   -> 3T
    17.000 EUR  a cobrar el 12 de octubre     -> 4T (o 3T si se emite antes)

Facturado sin IVA: servicio B2B intracomunitario, el cliente autoliquida.
Los importes son base imponible; no hay 21% que descontar.
"""

from irpf import cuota_irpf

IRLANDA_3T, IRLANDA_4T = 11000.00, 17000.00
SL_VENTAS_1T, SL_VENTAS_2T = 33891.33, 16240.00
SL_COSTES_TERCEROS_1S = 32015.76 - 15000.00   # compras SL menos tu factura
INGRESOS_1S = 15000.00        # c.01 del 130
GASTOS_1S = 6358.92           # c.02 del 130
RETA_MES = 88.00
UMBRAL = 0.35


def eur(x):
    return f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def principal(cuota, tipo=0.030, anos=30):
    i, n = tipo / 12, anos * 12
    return cuota * (1 - (1 + i) ** -n) / i


def perfil(ingresos_ano):
    gastos = GASTOS_1S * 2 + RETA_MES * 12
    rn = ingresos_ano - gastos
    irpf = cuota_irpf(max(0.0, rn))
    return rn, (rn - irpf) / 12, rn / 12


def main():
    print("=" * 78)
    print(" Nuevo cliente en Irlanda: 11.000 (sep) + 17.000 (oct), sin IVA")
    print("=" * 78)

    irlanda = IRLANDA_3T + IRLANDA_4T
    disponible_1s = (SL_VENTAS_1T + SL_VENTAS_2T) - SL_COSTES_TERCEROS_1S

    seccion("1. FACTURACION DE LA SL EN EL 2S")
    print("  El cliente irlandes se SUMA a la actividad interior. Dos ritmos")
    print("  posibles para esa actividad interior en el 2S:\n")
    escenarios = [
        ("Prudente (ritmo del 2T)", SL_VENTAS_2T * 2),
        ("Central (media del 1S)", (SL_VENTAS_1T + SL_VENTAS_2T)),
    ]
    print(f"  {'Escenario':<26}{'Interior 2S':>14}{'Irlanda':>12}"
          f"{'Ventas 2S':>14}")
    print(f"  {'-' * 66}")
    for etq, interior in escenarios:
        print(f"  {etq:<26}{eur(interior):>14}{eur(irlanda):>12}"
              f"{eur(interior + irlanda):>14}")

    seccion("2. CUANTO PUEDE PAGARTE LA SL EN TODO 2026")
    print(f"  Disponible ya generado en el 1S      {eur(disponible_1s):>13}")
    resultados = []
    for etq, interior in escenarios:
        disp_2s = (interior + irlanda) - SL_COSTES_TERCEROS_1S
        disp_ano = disponible_1s + disp_2s
        a_facturar_2s = disp_ano - INGRESOS_1S
        resultados.append((etq, disp_ano, a_facturar_2s))
        print(f"\n  {etq}")
        print(f"    Disponible en el 2S                {eur(disp_2s):>13}")
        print(f"    Disponible en todo 2026            {eur(disp_ano):>13}")
        print(f"    Ya facturado por ti en el 1S       {eur(INGRESOS_1S):>13}")
        print(f"    TE QUEDA POR FACTURAR EN EL 2S     {eur(a_facturar_2s):>13}")
        print(f"      repartido entre 3T y 4T          {eur(a_facturar_2s / 2):>13}")

    seccion("3. QUE ACREDITARIAS SI FACTURAS TODO ESE MARGEN")
    print(f"  {'Escenario':<26}{'Facturado':>13}{'Rend. neto':>13}"
          f"{'Neto/mes':>11}{'R.neto/mes':>12}")
    print(f"  {'-' * 75}")
    perfiles = []
    for etq, disp_ano, _ in resultados:
        rn, neto_mes, rn_mes = perfil(disp_ano)
        perfiles.append((etq, neto_mes, rn_mes))
        print(f"  {etq:<26}{eur(disp_ano):>13}{eur(rn):>13}"
              f"{eur(neto_mes):>11}{eur(rn_mes):>12}")

    seccion("4. HIPOTECA AL 3% A 30 ANOS (cuota al 35%)")
    print(f"  {'Escenario':<26}{'Criterio neto':>18}{'Criterio r.neto':>18}")
    print(f"  {'-' * 62}")
    for etq, neto_mes, rn_mes in perfiles:
        print(f"  {etq:<26}{eur(principal(neto_mes * UMBRAL)):>18}"
              f"{eur(principal(rn_mes * UMBRAL)):>18}")

    seccion("5. COMPARATIVA CON NO HACER NADA")
    rn_p, neto_p, rnmes_p = perfil(INGRESOS_1S + irlanda)
    print(f"  Si solo facturas a la SL los 28.000 del cliente irlandes")
    print(f"  (total 43.000 en el ano): acreditas {eur(neto_p)} EUR/mes")
    print(f"  y la hipoteca se queda en {eur(principal(neto_p * UMBRAL))} - "
          f"{eur(principal(rnmes_p * UMBRAL))} EUR.")
    mejor = perfiles[0]
    print(f"\n  Facturando todo el margen disponible (escenario prudente)")
    print(f"  subes a {eur(mejor[1])} EUR/mes y "
          f"{eur(principal(mejor[1] * UMBRAL))} - "
          f"{eur(principal(mejor[2] * UMBRAL))} EUR de hipoteca.")

    seccion("6. ANTES DE EMITIR LA FACTURA DE SEPTIEMBRE")
    print("  1. Alta en el ROI (modelo 036, casilla 582) y NIF-IVA validado")
    print("     en VIES. Sin eso NO puedes facturar sin IVA: tendrias que")
    print("     repercutir el 21% al cliente irlandes.")
    print("  2. Valida tambien el NIF-IVA irlandes del cliente en VIES y")
    print("     guarda el justificante de la consulta.")
    print("  3. La factura llevara la mencion 'inversion del sujeto pasivo'")
    print("     / 'reverse charge', art. 196 Directiva 2006/112/CE.")
    print("  4. En el 303 va en la CASILLA 59, no en la 122 (que es para")
    print("     operaciones interiores).")
    print("  5. Presenta el MODELO 349 del periodo. Se cruza via VIES con lo")
    print("     que declare el cliente irlandes.")


if __name__ == "__main__":
    main()
