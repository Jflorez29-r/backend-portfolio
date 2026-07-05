from datetime import datetime
from explorador import FORMATO_FECHAS
from typing import Tuple, Optional

TOKENS_MISSING = {"", "na", "n/a", "null", "none", "missing", "not provided"}

MAPA_PAISES = {
    # Colombia ISO "CO"
    "col": "CO",
    "co": "CO",
    "colombia": "CO",
    # Mexico ISO "MX"
    "mexico": "MX",
    "méxico": "MX",
    "mex": "MX",
    "mx": "MX",
    # Brasil ISO "BR"
    "brasil": "BR",
    "brazil": "BR",
    "br": "BR",
    # Argentina ISO "AR"
    "argentina": "AR",
    "arg": "AR",
    # Chile ISO "CL"
    "chile": "CL",
    "ch1le": "CL",
    "cl": "CL",
}

MAPA_CATEGORIAS = {
    "food": "food",
    "books": "books",
    "b00ks": "books",
    "electronics": "electronics",
    "electrónics": "electronics",
    "home": "home",
    "home & garden": "home",
    "sports": "sports",
    "sport": "sports",
    "clothing": "clothing",
}

MAPA_QTY_TEXTO = {
    "one": 1,
    "dos": 2,
}

CATEGORIAS_AMOUNT_ACEPTADAS = {
    "decimal_dot",
    "decimal_comma",
    "currency_text",
    "currency_symbol",
    "integer",
}

# función que normaliza texto sin importar el valor, devuelve un solo valor
def normalizar_texto(valor: object) -> str:
    if valor is None:  # el valor es None, no vino como valor
        return "null"  # definimos "null"  como  valor de ausencia
    return str(valor).strip().lower()  # devolvemos el valor normalizado


# función que verifica valores de ausencia en la fila
def is_missing(valor: object) -> bool:
    return normalizar_texto(valor) in TOKENS_MISSING


# función que validará los campos obligatorios
def validar_campos_obligatorios(
    fila: dict, campos: list[str]
) -> Tuple[bool, Optional[str]]:
    for campo in campos:  # recorrer la lista de campos obligatorios
        if is_missing(
            fila.get(campo)
        ):  # validar si algún campo obligatorio no vino en el dict
            return False, f"missing_required:{campo}"
    return True, None


# función que valida el country
def validar_country(valor: object) -> Tuple[bool, Optional[str]]:
    v = normalizar_texto(valor)  # normalizar el valor
    if v in TOKENS_MISSING:  # validar si el valor es un token missing
        return False, "invalid_country"
    if v not in MAPA_PAISES:  # validar si está en el mapa de países identificados
        return False, "invalid_country"
    return True, None  # devolver una tupla


# función que valida la categoría
def validar_category(valor: object) -> tuple[bool, Optional[str]]:
    v = normalizar_texto(valor)  # normalizar el valor
    if v in TOKENS_MISSING:
        return False, "invalid_category"
    if v not in MAPA_CATEGORIAS:
        return False, "invalid_category"
    return True, None


# función que calsifica
def clasificar_amount(valor: object) -> str:
    v = normalizar_texto(valor)

    if v in TOKENS_MISSING:
        return "missing"
    if v in ("error", "duplicate_row"):
        return "error_token"
    if v.startswith("-"):
        return "negative"
    if any(moneda in v for moneda in ("usd", "eur", "gbp")):
        return "currency_text"
    if any(simbolo in v for simbolo in ("$", "€", "£")):
        return "currency_symbol"
    if "," in v and "." not in v:
        return "decimal_comma"
    if "." in v and "," not in v:
        return "decimal_dot"
    if v.isdigit():
        return "integer"

    return "malformed"


# función que valida el amount
def validar_amount(valor: str) -> tuple[bool, Optional[str]]:
    categoria = clasificar_amount(valor)

    if categoria in CATEGORIAS_AMOUNT_ACEPTADAS:
        return True, None
    return False, "invalid_amount"


def validar_quantity(valor: object) -> tuple[bool, Optional[str]]:
    v = normalizar_texto(valor)
    if v in TOKENS_MISSING:
        return False, "invalid_quantity"
    if v in MAPA_QTY_TEXTO:
        return True, None
    if v.isdigit() and int(v) > 0:
        return True, None
    return False, "invalid_quantity"


def validar_transaction_date(valor: object) -> tuple[bool, Optional[str]]:
    v = normalizar_texto(valor)
    if v in TOKENS_MISSING:
        return False, "invalid_transaction_date"
    for fmt in FORMATO_FECHAS:
        try:
            datetime.strptime(v, fmt)
            return True, None
        except ValueError:
            continue
    return False, "invalid_transaction_date"


if __name__ == "__main__":
    # pruebas rápidas
    print(normalizar_texto("7551.13 USD"))
