#!/usr/bin/env python3
"""Factura de 40.000 EUR a la SL con fecha 30 de septiembre de 2026.

Calcula el efecto en el 130 y el 303 del 3T, la tesoreria de ambas partes
y lo que queda por facturar en el 4T.
"""

from irpf import cuota_irpf

FACTURA = 40000.00
IVA = 0.21
RETENCION = 0.07          # tipo reducido de nuevo autonomo, art. 101.5 LIRPF

INGRESOS_1S = 15000.00    # c.01 del 130 a 2T
GASTOS_1S = 6358.92       # c.02 del 130 a 2T
IVA_SOP_1S = 521.91 + 809.77   # c.29 del 303, cuotas reales del 1S
PAGO_1T = 1234.83         # c.19 del 130 del 1T
NEG_2T = 556.61           # c.07 negativa del 2T
COMPENSAR_2T = 809.77     # c.71 del 303 del 2T, a compensar
RETA_MES = 88.00
UMBRAL = 0.35

SL_MARGEN_2S = (61579.81, 79231.14)   # prudente / central
SL_IVA_ACUMULADO = 3325.28 + 3266.79  # credito de IVA de la SL a cierre de 2T


def eur(x):
    return f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def seccion(t):
    print(f"\n{t}\n{'-' * len(t)}")


def principal(cuota, tipo=0.030, anos=30):
    i, n = tipo / 12, anos * 12
    return cuota * (1 - (1 + i) ** -n) / i


def main():
    print("=" * 72)
    print(f" Factura de {eur(FACTURA)} a la SL - 30 de septiembre de 2026")
    print("=" * 72)

    gasto_3t = GASTOS_1S / 2
    iva_sop_3t = IVA_SOP_1S / 2   # media trimestral de cuota soportada

    seccion("1. LA FACTURA")
    print(f"  Base imponible                     {eur(FACTURA):>12}")
    print(f"  IVA repercutido 21%                {eur(FACTURA * IVA):>12}")
    print(f"  Retencion IRPF 7%                 -{eur(FACTURA * RETENCION):>12}")
    print(f"  {'-' * 44}")
    print(f"  TOTAL A COBRAR                     "
          f"{eur(FACTURA * (1 + IVA - RETENCION)):>12}")

    seccion("2. TU MODELO 130 DEL 3T")
    ing = INGRESOS_1S + FACTURA
    gastos = GASTOS_1S + gasto_3t
    rn = ing - gastos
    c04 = rn * 0.20
    c06 = ing * RETENCION
    c07 = c04 - PAGO_1T - c06
    pago130 = max(0.0, max(0.0, c07) - NEG_2T)
    print(f"  c.01 Ingresos acumulados           {eur(ing):>12}")
    print(f"  c.02 Gastos acumulados             {eur(gastos):>12}")
    print(f"  c.03 RENDIMIENTO NETO              {eur(rn):>12}")
    print(f"  c.04 20% de c.03                   {eur(c04):>12}")
    print(f"  c.05 Pago del 1T                  -{eur(PAGO_1T):>12}")
    print(f"  c.06 Retenciones al 7%            -{eur(c06):>12}")
    print(f"  c.15 Negativo del 2T              -{eur(NEG_2T):>12}")
    print(f"  c.19 A INGRESAR                    {eur(pago130):>12}")
    print(f"\n  Rendimiento neto / 9 meses         {eur(rn / 9):>12}  <-- lo que")
    print("                                                      acreditas")

    seccion("3. TU MODELO 303 DEL 3T")
    iva_rep = FACTURA * IVA
    res303 = iva_rep - iva_sop_3t - COMPENSAR_2T
    print(f"  c.03 IVA repercutido               {eur(iva_rep):>12}")
    print(f"  c.29 IVA soportado (estimado)     -{eur(iva_sop_3t):>12}")
    print(f"  c.110 A compensar del 2T          -{eur(COMPENSAR_2T):>12}")
    print(f"  c.71 A INGRESAR                    {eur(res303):>12}")

    seccion("4. TU CAJA")
    cobras = FACTURA * (1 + IVA - RETENCION)
    pagas = pago130 + res303
    print(f"  Cobras de la SL                    {eur(cobras):>12}")
    print(f"  Pagas el 20 de octubre:")
    print(f"    modelo 130                      -{eur(pago130):>12}")
    print(f"    modelo 303                      -{eur(res303):>12}")
    print(f"  {'-' * 44}")
    print(f"  TE QUEDA                           {eur(cobras - pagas):>12}")

    seccion("5. LA CAJA DE LA SL")
    print(f"  Tiene que desembolsar              {eur(cobras):>12}")
    print(f"  mas la retencion via modelo 111    {eur(FACTURA * RETENCION):>12}")
    print(f"  {'-' * 44}")
    print(f"  COSTE TOTAL PARA LA SL             "
          f"{eur(FACTURA * (1 + IVA)):>12}")
    print(f"\n  Su IVA soportado sube en           {eur(iva_rep):>12}")
    print(f"  Credito de IVA que ya arrastraba    {eur(SL_IVA_ACUMULADO):>12}")
    print(f"  CREDITO ACUMULADO APROXIMADO        "
          f"{eur(SL_IVA_ACUMULADO + iva_rep):>12}")
    print("\n  >> La SL no repercute IVA (ventas por ISP e intracomunitarias),")
    print("     asi que ese credito no se compensa solo. Se pide la devolucion")
    print("     en el 303 del 4T, en enero de 2027. Hasta entonces es caja")
    print("     inmovilizada. Valora darla de alta en el REDEME para cobrarlo")
    print("     mensualmente.")

    seccion("6. QUE TE QUEDA PARA EL 4T")
    print(f"  {'Objetivo de cierre':<34}{'Facturar 4T':>14}{'Total 2026':>13}")
    print(f"  {'-' * 61}")
    gastos_ano = GASTOS_1S * 2 + RETA_MES * 12
    for etq, rn_obj in (("Rend. neto de 5.000/mes", 60000.00),
                        ("Neto de 5.000/mes tras IRPF", None)):
        if rn_obj is None:
            from irpf import resuelve_bruto
            rn_obj = resuelve_bruto(60000.0, lambda r: r - cuota_irpf(max(0.0, r)))
        ing_total = rn_obj + gastos_ano
        print(f"  {etq:<34}{eur(ing_total - ing):>14}{eur(ing_total):>13}")
    print(f"\n  Margen que te deja la SL en el 2S:")
    for etq, m in (("prudente", SL_MARGEN_2S[0]), ("central", SL_MARGEN_2S[1])):
        print(f"    {etq:<10} {eur(m):>12}  ->  te quedan "
              f"{eur(m - FACTURA)} para el 4T")

    seccion("7. CIERRE DEL ANO SI AGOTAS EL MARGEN PRUDENTE")
    ing_ano = INGRESOS_1S + SL_MARGEN_2S[0]
    rn_ano = ing_ano - gastos_ano
    neto_mes = (rn_ano - cuota_irpf(rn_ano)) / 12
    print(f"  Facturado en 2026                  {eur(ing_ano):>12}")
    print(f"  Rendimiento neto                   {eur(rn_ano):>12}")
    print(f"  Neto/mes tras IRPF                 {eur(neto_mes):>12}")
    print(f"  Rendimiento neto/mes               {eur(rn_ano / 12):>12}")
    print(f"  Hipoteca 3%/30a                    "
          f"{eur(principal(neto_mes * UMBRAL))} - "
          f"{eur(principal(rn_ano / 12 * UMBRAL))}")

    seccion("8. AVISOS DE CUMPLIMIENTO")
    sl_cifra = 50131.33 + (16240.00 * 2 + 28000.00)   # 1S + 2S prudente
    umbral_232 = sl_cifra * 0.50
    tus_facturas = INGRESOS_1S + SL_MARGEN_2S[0]
    print("  - OPERACIONES VINCULADAS / MODELO 232.")
    print(f"    Cifra de negocios de la SL en 2026 (prudente) {eur(sl_cifra)}")
    print(f"    Umbral del 50%                                {eur(umbral_232)}")
    print(f"    Tus facturas si agotas el margen              {eur(tus_facturas)}")
    if tus_facturas > umbral_232:
        print("    -> SE SUPERA: modelo 232 OBLIGATORIO, a presentar en")
        print("       noviembre de 2027 por el ejercicio 2026.")
    else:
        print("    -> no se supera por poco; vigilalo al cerrar el 4T.")
    print(f"    (Solo con los 40.000 del 3T iras a {eur(INGRESOS_1S + FACTURA)},")
    print(f"     un {100 * (INGRESOS_1S + FACTURA) / sl_cifra:.1f}% de la cifra de negocios.)")
    print("    Necesitas documentacion que sostenga el valor de mercado:")
    print("    horas, entregables, comparables.")
    print("  - Pasar de 0,00 en el 2T a 40.000,00 en el 3T es un salto que")
    print("    pide justificacion documental solida. Que la factura describa")
    print("    el periodo de servicio y el trabajo real prestado.")
    print("  - El servicio debe estar PRESTADO a 30 de septiembre. Si no, la")
    print("    factura es del 4T por mucha fecha que lleve.")


if __name__ == "__main__":
    main()
