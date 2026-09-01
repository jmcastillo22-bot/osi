"""Escalas y funciones fiscales IRPF (estimacion).

AVISO: tipos y tramos son los de la escala general estatal + autonomica tipo.
La parte autonomica varia por comunidad. Ajusta ESCALA_GENERAL si tu CCAA
se desvia de la escala de referencia.
"""

# Escala general IRPF (estatal + autonomica de referencia).
# (limite superior del tramo, tipo marginal)
ESCALA_GENERAL = [
    (12450.00, 0.19),
    (20200.00, 0.24),
    (35200.00, 0.30),
    (60000.00, 0.37),
    (300000.00, 0.45),
    (float("inf"), 0.47),
]

# Escala del ahorro (dividendos, intereses).
ESCALA_AHORRO = [
    (6000.00, 0.19),
    (50000.00, 0.21),
    (200000.00, 0.23),
    (300000.00, 0.27),
    (float("inf"), 0.30),
]

MINIMO_PERSONAL = 5550.00
GASTOS_GENERICOS_TRABAJO = 2000.00


def aplica_escala(base, escala):
    """Aplica una escala progresiva por tramos a una base."""
    cuota = 0.0
    anterior = 0.0
    for limite, tipo in escala:
        if base <= anterior:
            break
        cuota += (min(base, limite) - anterior) * tipo
        anterior = limite
    return cuota


def cuota_irpf(base_liquidable, minimo_personal=MINIMO_PERSONAL):
    """Cuota IRPF de la base general, restando el minimo personal por escala."""
    bruta = aplica_escala(base_liquidable, ESCALA_GENERAL)
    minimo = aplica_escala(minimo_personal, ESCALA_GENERAL)
    return max(0.0, bruta - minimo)


def cuota_ahorro(base_ahorro):
    """Cuota IRPF de la base del ahorro (p.ej. dividendos de la SL)."""
    return aplica_escala(base_ahorro, ESCALA_AHORRO)


def rendimiento_neto_trabajo(bruto_anual, cotizaciones_deducibles=0.0):
    """Rendimiento neto del trabajo (nomina de administrador/socio)."""
    integro = bruto_anual - cotizaciones_deducibles
    return max(0.0, integro - GASTOS_GENERICOS_TRABAJO)


def resuelve_bruto(neto_objetivo, f_neto, lo=0.0, hi=2_000_000.0, iteraciones=200):
    """Biseccion: encuentra el bruto x tal que f_neto(x) == neto_objetivo.

    f_neto debe ser monotona creciente en x.
    """
    for _ in range(iteraciones):
        mid = (lo + hi) / 2
        if f_neto(mid) < neto_objetivo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
