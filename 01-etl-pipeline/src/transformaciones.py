from datetime import datetime
from validadores import (
    normalizar_texto,
    validar_country,
    validar_category,
    clasificar_amount,
    validar_quantity,
    MAPA_PAISES,
    MAPA_CATEGORIAS,
    CATEGORIAS_AMOUNT_ACEPTADAS,
    MAPA_QTY_TEXTO,
)
from explorador import FORMATO_FECHAS

# función que normaliza el country
def normalizar_country(dato: object) -> str:
    """
    Normaliza el campo country a codigo ISO usando el mapa de paises.
    Lanza ValueError si el valor no es valido.
    """
    d = normalizar_texto(dato)  # normalizar el valor
    ok, motivo = validar_country(d)  # recibir la tupla
    if ok is False:
        raise ValueError(f"country no válido: {dato} ({motivo})")
    return MAPA_PAISES[d]


# función que  normaliza la categorí­a
def normalizar_category(dato: object) -> str:
    """
    Normaliza el campo category a su forma estandar.
    Lanza ValueError si el valor no es valido.
    """
    d = normalizar_texto(dato)
    ok, motivo = validar_category(d)
    if ok is False:
        raise ValueError(f"Category no válido: {dato} ({motivo})")
    return MAPA_CATEGORIAS[d]


# función que normaliza el amount
def normalizar_amount(dato: object) -> float:
    """
    Normaliza el campo amount segun su categoria.
    Lanza ValueError si la categoria no es aceptada.
    """
    d = normalizar_texto(dato)
    d_limpio = d
    categoria = clasificar_amount(d)
    if not categoria in CATEGORIAS_AMOUNT_ACEPTADAS:
        raise ValueError(f"Amount no válido: {dato}")
    if categoria == "currency_text":
        simbolos = ["usd", "eur", "gbp"]
        d_limpio = d
        for s in simbolos:
            d_limpio = d_limpio.replace(s, "").strip()
        d_limpio = d_limpio.replace(",", ".").strip()
    if categoria == "currency_symbol":
        simbolos = ["$", "€", "£"]
        d_limpio = d
        for s in simbolos:
            d_limpio = d_limpio.replace(s, "").strip()
        d_limpio = d_limpio.replace(",", ".").strip()
    if categoria == "decimal_comma":
        d_limpio = d.replace(",", ".").strip()
    valor = float(d_limpio)
    if valor == 0.0:
        raise ValueError("invalid_amount_zero")

    return valor


# función que normaliza quanity
def normalizar_quantity(valor: object) -> int:
    v = normalizar_texto(valor)
    ok, motivo = validar_quantity(v)
    if ok is False:
        raise ValueError(f"Quantity no válido: {valor} ({motivo})")
    if v in MAPA_QTY_TEXTO:
        return MAPA_QTY_TEXTO[v]
    return int(v)


# función que normaliza la transaction_date
def normalizar_transaction_date(valor: object) -> str:
    v = normalizar_texto(valor)
    for fmt in FORMATO_FECHAS:
        try:
            fecha_limpia = datetime.strptime(v, fmt)
            return fecha_limpia.strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError("invalid_transaction_date")
