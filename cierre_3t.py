#!/usr/bin/env python3
"""Cierre del 3T de 2026: que entra, que no, y con que fechas.

El 3T va del 1 de julio al 30 de septiembre. Una factura emitida el 30 de
septiembre entra en el trimestre; la fecha de cobro es irrelevante.

Pero conviene separar dos cosas distintas:
    - las ventas de la SL a Irlanda   -> 303 y modelo 349 de la SL
    - tus facturas de autonomo a la SL -> tu 130 y tu 303
Solo las segundas acreditan ingresos a tu nombre.
"""

from irpf import cuota_irpf

INGRESOS_1S = 15000.00     # c.01 del 130, acumulado a 2T
GASTOS_1S = 6358.92        # c.02 del 130, acumulado a 2T
GASTO_TRIM = GASTOS_1S / 2
RETA_MES = 88.00
UMBRAL = 0.35

# Margen que la SL puede pagarte en el 2S (escenario prudente / central)
MARGEN_2S = (61579.81, 79231.14)


def eur(x):
    return f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def principal(cuota, tipo=0.030, anos=30):
    i, n = tipo / 12, anos * 12
    return cuota * (1 - (1 + i) ** -n) / i


def main():
    print("=" * 74)
    print(" Cierre del 3T 2026 - efecto de facturar el 30 de septiembre")
    print("=" * 74)

    seccion("1. CALENDARIO")
    print("  3T 2026                    1 julio - 30 septiembre (miercoles)")
    print("  Factura del 30 de sept.    ENTRA en el 3T")
    print("  Cobro del 12 de octubre    irrelevante para el devengo")
    print("  Presentacion 303/130 3T    1 - 20 de octubre (martes)")
    print("    con domiciliacion        hasta el 15 de octubre (jueves)")
    print("  Modelo 349 del 3T          mismo plazo")

    seccion("2. LA CONDICION QUE NO SE PUEDE SALTAR")
    print("  El IVA de un servicio se devenga cuando el servicio SE PRESTA")
    print("  (art. 75.Uno.2 LIVA), no cuando se emite la factura. En IRPF")
    print("  rige igualmente el criterio de devengo.")
    print()
    print("  Emitir el 30 de septiembre solo es correcto si el trabajo esta")
    print("  hecho a esa fecha. Si el servicio se presta en octubre, la")
    print("  factura es de octubre por mucho que lleve fecha de septiembre.")
    print()
    print("  Si el servicio SI esta prestado en septiembre, de hecho tienes")
    print("  obligacion de facturar antes del 16 de octubre, y la operacion")
    print("  es del 3T aunque emitas en octubre.")

    seccion("3. PERO ESA FACTURA ES DE LA SL, NO TUYA")
    print("  Los 17.000 a Irlanda son ventas de OSI Global Consulting.")
    print("  Adelantarlos al 3T mueve:")
    print("    - el 303 de la SL (casilla 59) y su modelo 349")
    print("    - el pago fraccionado del Impuesto de Sociedades")
    print("    - la tesoreria de la sociedad")
    print("  NO mueve tu modelo 130 ni un euro.")
    print()
    print("  Lo que acredita ingresos A TU NOMBRE es TU factura a la SL.")
    print("  Si quieres que el 3T se vea fuerte en tu 130, la que tiene que")
    print("  estar emitida antes del 30 de septiembre es esa.")

    seccion("4. TUS FACTURAS A LA SL LLEVAN RETENCION DEL 7%")
    print("  La casilla 06 de tus dos 130 vale 1.050,00, que es exactamente")
    print("  el 7% de los 15.000 facturados. Es el tipo reducido del art.")
    print("  101.5 LIRPF, aplicable el ano de alta y los DOS siguientes.")
    print()
    print("  Dos consecuencias:")
    print("    - cobras el 93% de cada factura; el 7% lo ingresa la SL por")
    print("      el modelo 111 y a ti te descuenta el pago del 130")
    print("    - confirma que eres autonomo reciente, justo lo que el banco")
    print("      mira cuando exige dos ejercicios de antiguedad")

    seccion("5. TU 130 DEL 3T SEGUN LO QUE LE FACTURES A LA SL")
    print(f"  {'Le facturas en el 3T':>22}{'c.01 acum.':>13}{'c.03 acum.':>13}"
          f"{'R.neto/mes':>13}{'Pago 130':>12}")
    print(f"  {'-' * 73}")
    for importe in (0, 15000, 20000, 25000, 30789.91, 39615.57):
        ing = INGRESOS_1S + importe
        rn = ing - (GASTOS_1S + GASTO_TRIM)
        c04 = rn * 0.20                 # 20% del rendimiento neto acumulado
        c05 = 1234.83                   # suma de c.07 positivas anteriores
        c06 = ing * 0.07                # retenciones acumuladas al 7%
        c07 = c04 - c05 - c06
        c15 = 556.61                    # resultado negativo del 2T
        pago = max(0.0, max(0.0, c07) - c15)
        print(f"  {eur(importe):>22}{eur(ing):>13}{eur(rn):>13}"
              f"{eur(rn / 9):>13}{eur(pago):>12}")
    print("\n  (R.neto/mes divide entre 9 meses: enero-septiembre)")
    print("  (Pago 130 = 20% de c.03, menos el pago del 1T, menos las")
    print("   retenciones del 7% acumuladas, menos los 556,61 negativos del 2T)")

    seccion("6. Y EL CIERRE DEL ANO")
    print(f"  {'Facturado a la SL 2S':>22}{'Total 2026':>13}{'Rend. neto':>13}"
          f"{'Neto/mes':>12}{'Hipoteca 3%/30a':>18}")
    print(f"  {'-' * 78}")
    for etq, margen in (("prudente", MARGEN_2S[0]), ("central", MARGEN_2S[1])):
        ing = INGRESOS_1S + margen
        rn = ing - GASTOS_1S * 2 - RETA_MES * 12
        neto_mes = (rn - cuota_irpf(max(0.0, rn))) / 12
        print(f"  {eur(margen) + ' (' + etq + ')':>22}{eur(ing):>13}{eur(rn):>13}"
              f"{eur(neto_mes):>12}{eur(principal(neto_mes * UMBRAL)):>18}")
    print("\n  Repartirlo entre 3T y 4T o cargarlo todo en el 3T da el mismo")
    print("  total anual. Solo cambia si el banco mira un trimestre suelto.")


if __name__ == "__main__":
    main()
