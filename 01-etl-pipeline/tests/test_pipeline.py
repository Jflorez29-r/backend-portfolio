import pytest
import sys
import os

# Asegurar que pytest encuentre los módulos de src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import validadores as val
import transformaciones as tr
from pipeline import procesar_fila

# Tests de validación de países
def test_validar_country():
    assert val.validar_country("Colombia")[0] is True
    assert val.validar_country("co")[0] is True
    assert val.validar_country("col")[0] is True
    assert val.validar_country("Alemania")[0] is False
    assert val.validar_country("na")[0] is False

# Tests de normalización de países
def test_normalizar_country():
    assert tr.normalizar_country("Colombia") == "CO"
    assert tr.normalizar_country("co") == "CO"
    assert tr.normalizar_country("mexico") == "MX"
    with pytest.raises(ValueError):
        tr.normalizar_country("invalid_country")

# Tests de validación de categorías
def test_validar_category():
    assert val.validar_category("food")[0] is True
    assert val.validar_category("B00ks")[0] is True
    assert val.validar_category("toys")[0] is False

# Tests de normalización de categorías
def test_normalizar_category():
    assert tr.normalizar_category("food") == "food"
    assert tr.normalizar_category("b00ks") == "books"
    with pytest.raises(ValueError):
        tr.normalizar_category("toys")

# Tests de clasificación e validación de amounts
def test_validar_amount():
    assert val.validar_amount("150.50")[0] is True
    assert val.validar_amount("150,50")[0] is True
    assert val.validar_amount("$100")[0] is True
    assert val.validar_amount("50 usd")[0] is True
    assert val.validar_amount("-10.00")[0] is False  # Negativos no son aceptados
    assert val.validar_amount("na")[0] is False

# Tests de normalización de amounts
def test_normalizar_amount():
    assert tr.normalizar_amount("150.50") == 150.50
    assert tr.normalizar_amount("150,50") == 150.50
    assert tr.normalizar_amount("$100") == 100.00
    assert tr.normalizar_amount("50 usd") == 50.00
    with pytest.raises(ValueError):
        tr.normalizar_amount("-10.00")
    with pytest.raises(ValueError):
        tr.normalizar_amount("0.0")

# Tests de validación de cantidades
def test_validar_quantity():
    assert val.validar_quantity("5")[0] is True
    assert val.validar_quantity("one")[0] is True
    assert val.validar_quantity("dos")[0] is True
    assert val.validar_quantity("-2")[0] is False
    assert val.validar_quantity("many")[0] is False

# Tests de normalización de cantidades
def test_normalizar_quantity():
    assert tr.normalizar_quantity("5") == 5
    assert tr.normalizar_quantity("one") == 1
    assert tr.normalizar_quantity("dos") == 2
    with pytest.raises(ValueError):
        tr.normalizar_quantity("-2")

# Tests de validación y normalización de fechas
def test_transaction_date():
    assert val.validar_transaction_date("2025-05-15")[0] is True
    assert val.validar_transaction_date("15/05/2025")[0] is True
    assert val.validar_transaction_date("invalid_date")[0] is False
    
    assert tr.normalizar_transaction_date("2025-05-15") == "2025-05-15"
    assert tr.normalizar_transaction_date("15/05/2025") == "2025-05-15"

# Test de procesar_fila completo (pipeline unitario)
def test_procesar_fila():
    fila_valida = {
        "country": "Colombia",
        "category": "food",
        "amount": "150,50",
        "quantity": "dos",
        "transaction_date": "15/05/2025"
    }
    ok, resultado = procesar_fila(fila_valida)
    assert ok is True
    assert resultado["country"] == "CO"
    assert resultado["category"] == "food"
    assert resultado["amount"] == 150.50
    assert resultado["quantity"] == 2
    assert resultado["transaction_date"] == "2025-05-15"

    fila_invalida = {
        "country": "Alemania",
        "category": "food",
        "amount": "150.50",
        "quantity": "2",
        "transaction_date": "2025-05-15"
    }
    ok, resultado = procesar_fila(fila_invalida)
    assert ok is False
    assert resultado == "invalid_country"
