import csv
import json
import os
from typing import Iterator
from collections import Counter
from datetime import datetime
from itertools import islice


MISSING = object()
TOKENS_MISSING = {"", "na", "n/a", "null", "none", "missing", "not provided"}
CATEGORIAS_AMOUNT = [
    "missing",
    "error_token",
    "negative",
    "currency_text",
    "currency_symbol",
    "decimal_comma",
    "decimal_dot",
    "integer",
    "malformed",
]
FORMATO_FECHAS = [
    # Año 4 dígitos con separadores numéricos
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y/%m/%d",
    "%d-%m-%Y",
    "%m-%d-%Y",
    "%Y.%m.%d",
    "%d.%m.%Y",
    "%m.%d.%Y",
    # Año 2 dígitos con separadores numéricos
    "%y-%m-%d",
    "%d/%m/%y",
    "%m/%d/%y",
    "%y/%m/%d",
    "%d-%m-%y",
    "%m-%d-%y",
    "%y.%m.%d",
    "%d.%m.%y",
    "%m.%d.%y",
    # Con espacios y mes numérico
    "%Y %m %d",
    "%y %m %d",
    "%d %m %Y",
    "%d %m %y",
    "%m %d %Y",
    "%m %d %y",
    # Mes abreviado (%b)
    "%d-%b-%Y",
    "%d-%b-%y",
    "%b-%d-%Y",
    "%b-%d-%y",
    "%Y-%b-%d",
    "%y-%b-%d",
    "%d %b %Y",
    "%d %b %y",
    "%b %d %Y",
    "%b %d %y",
    "%Y %b %d",
    "%y %b %d",
    # Mes completo (%B)
    "%d-%B-%Y",
    "%d-%B-%y",
    "%B-%d-%Y",
    "%B-%d-%y",
    "%Y-%B-%d",
    "%y-%B-%d",
    "%d %B %Y",
    "%d %B %y",
    "%B %d %Y",
    "%B %d %y",
    "%Y %B %d",
    "%y %B %d",
    "%B %d, %Y",
    "%B %d, %y",
    # Día Mes abreviado Año (con coma)
    "%b %d, %Y",
    "%b %d, %y",
    # Día Mes completo Año (sin coma, con espacio)
    "%B %d %Y",
    "%B %d %y",
    # Día Mes abreviado Año (sin coma, con espacio)
    "%b %d %Y",
    "%b %d %y",
    # Variantes con año primero
    "%Y %B %d",
    "%y %B %d",
    "%Y %b %d",
    "%y %b %d",
]

CAMPOS_OBLIGATORIOS = [
    "country",
    "category",
    "amount",
    "quantity",
    "transaction_date",
]


def explorar_fecha(ruta_archivo: str) -> tuple[list[str], list[str]]:
    """
    Detecta qué formatos de fecha existen y devuelve:
    1. Lista de formatos reconocidos.
    2. Lista de valores crudos que NO coincidieron con ningún formato.
    """
    formatos_encontrados = set()
    no_reconocidos = set()

    for fila in iterar_filas_csv(ruta_archivo):
        fecha_texto = normalizar_crudo(fila.get("transaction_date"))

        if not fecha_texto:
            continue

        coincidio = False
        for fmt in FORMATO_FECHAS:
            try:
                datetime.strptime(fecha_texto, fmt)
                formatos_encontrados.add(fmt)
                coincidio = True
                break
            except ValueError:
                continue

        if not coincidio:
            no_reconocidos.add(fecha_texto)

    return list(formatos_encontrados), list(no_reconocidos)


def clasificar_amount(valor: str) -> str:
    v = normalizar_crudo(valor)

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


def explorar_amount(ruta_archivo: str) -> dict[str, int]:
    contador = Counter()

    for fila in iterar_filas_csv(ruta_archivo):
        valor_crudo = fila.get("amount")
        categoria = clasificar_amount(valor_crudo)
        contador[categoria] += 1

    return dict(contador)


def normalizar_crudo(valor: object) -> str:
    if valor is MISSING or valor is None:
        return "null"
    return str(valor).strip().lower()


def iterar_filas_csv(ruta_archivo: str) -> Iterator[dict[str, str]]:
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")

    with open(ruta_archivo, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        # Limitamos a 500 filas para pruebas en el explorador
        for fila in islice(lector, 500):
            yield fila


def explorar_csv(ruta_archivo: str, columna: str) -> dict[str, object]:
    """Cuenta la frecuencia de cada valor en una columna específica de un archivo CSV."""
    if columna not in CAMPOS_OBLIGATORIOS:
        raise ValueError(
            f"La columna '{columna}' no es una columna válida. Opciones: {CAMPOS_OBLIGATORIOS}"
        )

    contador = Counter()
    for fila in iterar_filas_csv(ruta_archivo):
        valor_crudo = fila.get(columna)
        valor_normalizado = normalizar_crudo(valor_crudo)

        if valor_normalizado in TOKENS_MISSING:
            contador[MISSING] += 1
        else:
            contador[valor_normalizado] += 1

    resultado_final = {}
    for valor, conteo in contador.items():
        clave = "null" if valor is MISSING else valor
        resultado_final[clave] = conteo

    return resultado_final


def ensamblar_reporte(ruta_archivo: str) -> dict:
    reporte = {}

    for campo in CAMPOS_OBLIGATORIOS:
        if campo == "transaction_date":
            reconocidos, no_reconocidos = explorar_fecha(ruta_archivo)
            reporte[campo] = {
                "formatos_reconocidos": sorted(reconocidos),
                "no_reconocidos": sorted(no_reconocidos),
            }
        elif campo == "amount":
            conteos = explorar_amount(ruta_archivo)
            reporte[campo] = dict(
                sorted(conteos.items(), key=lambda x: x[1], reverse=True)
            )

        else:
            conteos = explorar_csv(ruta_archivo, campo)
            reporte[campo] = dict(
                sorted(conteos.items(), key=lambda x: x[1], reverse=True)
            )

    return reporte


def guardar_reporte_json(reporte: dict, ruta_salida: str) -> None:
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    ruta_csv = os.path.abspath(os.path.join(base_dir, "..", "data", "datos.csv"))
    ruta_reporte = os.path.abspath(os.path.join(base_dir, "..", "data", "reporte_exploracion.json"))

    try:
        reporte = ensamblar_reporte(ruta_csv)
        guardar_reporte_json(reporte, ruta_reporte)
        print(f"Reporte guardado en: {ruta_reporte}")
    except FileNotFoundError as e:
        print(f"Error al explorar: {e}")
