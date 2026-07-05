import csv
import random
import os
from datetime import datetime, timedelta

# Listas de datos realistas basados en los validadores
COUNTRIES = ["Colombia", "CO", "col", "Mexico", "MX", "mex", "Brasil", "Brazil", "br", "Argentina", "arg", "Chile", "cl", "invalid_country"]
CATEGORIES = ["food", "books", "electronics", "home", "sports", "clothing", "invalid_category"]
AMOUNTS = [
    "150.50", "200,75", "10 usd", "25.00 eur", "£99.99", "$120.50", "50", "-15.00", "na", "error", "duplicate_row", "malformed_amount"
]
QUANTITIES = ["1", "2", "5", "10", "one", "dos", "0", "-5", "na", "many"]
DATE_FORMATS = [
    "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y",
    "%d-%b-%Y", "%b %d, %Y", "%B %d, %Y", "invalid_date_format"
]

def generate_row():
    # 90% de probabilidad de generar datos válidos para la mayoría de los campos
    country = random.choice(COUNTRIES)
    category = random.choice(CATEGORIES)
    amount = random.choice(AMOUNTS)
    quantity = random.choice(QUANTITIES)
    
    # Generar una fecha aleatoria en un formato aleatorio
    start_date = datetime(2025, 1, 1)
    random_days = random.randint(0, 365)
    random_date = start_date + timedelta(days=random_days)
    
    date_fmt = random.choice(DATE_FORMATS)
    if date_fmt == "invalid_date_format":
        transaction_date = "2025/13/45"
    else:
        try:
            transaction_date = random_date.strftime(date_fmt)
        except Exception:
            transaction_date = "2025-05-15"

    return {
        "country": country,
        "category": category,
        "amount": amount,
        "quantity": quantity,
        "transaction_date": transaction_date
    }

def main(num_rows=1000, filename="mock_datos.csv"):
    base_dir = os.path.dirname(__file__)
    output_path = os.path.abspath(os.path.join(base_dir, "..", "data", filename))
    
    # Asegurar que el directorio de salida exista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fields = ["country", "category", "amount", "quantity", "transaction_date"]
    
    print(f"Generando {num_rows} registros mock en {output_path}...")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for _ in range(num_rows):
            writer.writerow(generate_row())
            
    print("Generación completada con éxito.")

if __name__ == "__main__":
    import sys
    rows = 10000
    if len(sys.argv) > 1:
        try:
            rows = int(sys.argv[1])
        except ValueError:
            pass
    main(rows)
