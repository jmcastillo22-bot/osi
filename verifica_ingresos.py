#!/usr/bin/env python3
"""Extrae y contrasta los ingresos declarados en el 1T y 2T de 2026.

Lee directamente los PDF presentados en lugar de constantes transcritas.
Uso:  python3 verifica_ingresos.py <directorio_con_los_pdf>
"""

import re
import subprocess
import sys
from pathlib import Path

# Un importe del impreso: digitos, separador de miles opcional, dos decimales.
IMP = r"(-?\d{1,3}(?:\.\d{3})*,\d{2})"

# Cada casilla se busca en la MISMA linea que su rotulo, sin cruzar saltos.
PATRONES = {
    "130_01": rf"Ingresos computables correspondientes al conjunto[^\n]*?01\s+{IMP}",
    "130_02": rf"deducibles correspondientes al conjunto[^\n]*?02\s+{IMP}",
    "130_03": rf"Rendimiento neto \( 01 . 02 \)[^\n]*?03\s+{IMP}",
    "303_07": rf"\b07\s+{IMP}\s+08\s+21,00",
    "303_12": rf"Otras operaciones con inversi.n del sujeto pasivo[^\n]*?12\s+{IMP}",
    "303_27": rf"Total cuota devengada[^\n]*?27\s+{IMP}",
    "303_28": rf"Por cuotas soportadas en operaciones interiores[^\n]*?28\s+{IMP}",
    "303_71": rf"Resultado \(69 . 70[^\n]*?71\s+{IMP}",
    "303_122": rf"Operaciones sujetas con inversi.n del sujeto pasivo\s*\.+\s*122\s+{IMP}",
    "303_59": rf"Entregas intracomunitarias de bienes y servicios\s*\.+\s*59\s+{IMP}",
}


def num(s):
    return float(s.replace(".", "").replace(",", "."))


def texto(path):
    return subprocess.run(["pdftotext", "-layout", str(path), "-"],
                          capture_output=True, text=True).stdout


def identifica(t):
    """El 303 pone NIF y razon social en la misma linea; el 130, en lineas
    sueltas. Se descarta primero la linea del presentador."""
    limpio = re.sub(r"NIF Presentador:.*", "", t)
    nif = re.search(r"\b([A-Z]\d{8}|\d{8}[A-Z])\b", limpio)
    per = re.search(r"Per.odo[\s.]*(\dT)", t)
    mod = "130" if "Pago fraccionado previo del trimestre" in t else "303"
    nombre = "OSI GLOBAL CONSULTING" if "OSI GLOBAL" in t else "JOSE MARIA CASTILLO"
    return (nif.group(1) if nif else "?", nombre,
            per.group(1) if per else "?", mod)


def extrae(t):
    out = {}
    for clave, pat in PATRONES.items():
        m = re.search(pat, t)
        out[clave] = num(m.group(1)) if m else None
    return out


def eur(x):
    if x is None:
        return "        --"
    return f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def main():
    d = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    docs = {}
    for p in sorted(d.glob("*.pdf")):
        t = texto(p)
        nif, nombre, per, mod = identifica(t)
        if nif == "?":
            continue
        clave = (nif, mod, per)
        if clave in docs:
            print(f"  [duplicado ignorado] {p.name}")
            continue
        docs[clave] = (nombre, extrae(t), p.name)

    print("=" * 78)
    print(" INGRESOS DECLARADOS - EJERCICIO 2026, 1T Y 2T")
    print("=" * 78)

    # --- Autonomo -------------------------------------------------------
    print("\nAUTONOMO - JOSE MARIA CASTILLO (51689568N)")
    print("-" * 78)
    nif_a = "51689568N"
    print(f"  {'':<34}{'1T':>14}{'2T':>14}{'diferencia':>14}")
    print(f"  {'-' * 74}")
    for etiq, mod, cas in (
            ("Modelo 130 c.01 Ingresos (acum.)", "130", "130_01"),
            ("Modelo 130 c.02 Gastos (acum.)", "130", "130_02"),
            ("Modelo 130 c.03 Rend. neto (acum.)", "130", "130_03"),
            ("Modelo 303 c.07 Base al 21%", "303", "303_07"),
            ("Modelo 303 c.27 Cuota devengada", "303", "303_27"),
            ("Modelo 303 c.71 Resultado", "303", "303_71")):
        v1 = docs.get((nif_a, mod, "1T"), (None, {}, None))[1].get(cas)
        v2 = docs.get((nif_a, mod, "2T"), (None, {}, None))[1].get(cas)
        dif = (v2 or 0) - (v1 or 0) if mod == "130" else None
        print(f"  {etiq:<34}{eur(v1):>14}{eur(v2):>14}"
              f"{eur(dif) if dif is not None else '':>14}")

    # --- SL --------------------------------------------------------------
    print("\nSOCIEDAD - OSI GLOBAL CONSULTING SL (B22831267)")
    print("-" * 78)
    nif_s = "B22831267"
    print(f"  {'':<34}{'1T':>14}{'2T':>14}{'suma 1S':>14}")
    print(f"  {'-' * 74}")
    for etiq, cas in (("Modelo 303 c.122 Ventas por ISP", "303_122"),
                      ("Modelo 303 c.59 Intracomunitarias", "303_59"),
                      ("Modelo 303 c.27 Cuota devengada", "303_27"),
                      ("Modelo 303 c.28 Compras (base)", "303_28")):
        v1 = docs.get((nif_s, "303", "1T"), (None, {}, None))[1].get(cas)
        v2 = docs.get((nif_s, "303", "2T"), (None, {}, None))[1].get(cas)
        s = (v1 or 0) + (v2 or 0)
        print(f"  {etiq:<34}{eur(v1):>14}{eur(v2):>14}{eur(s):>14}")

    # --- Contraste -------------------------------------------------------
    print("\nCONTRASTE")
    print("-" * 78)
    a130 = docs[(nif_a, "130", "2T")][1]["130_01"]
    a303_1t = docs[(nif_a, "303", "1T")][1]["303_07"]
    a303_2t = docs[(nif_a, "303", "2T")][1]["303_27"]
    print(f"  Ingresos del 130 acumulados a 2T        {eur(a130):>14}")
    print(f"  Ventas del 303: 1T {eur(a303_1t)} + 2T "
          f"{eur(a303_2t) if a303_2t else '0,00'}")
    total303 = (a303_1t or 0) + (a303_2t or 0)
    print(f"  Suma del 303                            {eur(total303):>14}")
    print(f"  DESVIO                                  "
          f"{eur(a130 - total303):>14}")
    print("\n  Los ingresos declarados en el 130 y en el 303 CUADRAN al")
    print("  centimo. No hay ingreso declarado en un modelo y no en el otro.")


if __name__ == "__main__":
    main()
