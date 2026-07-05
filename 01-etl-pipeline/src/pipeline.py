from explorador import iterar_filas_csv
import validadores as val
import transformaciones as tr
from explorador import CAMPOS_OBLIGATORIOS
from typing import Tuple
import csv
import os

VALIDADORES = {
    "country": val.validar_country,
    "category": val.validar_category,
    "amount": val.validar_amount,
    "quantity": val.validar_quantity,
    "transaction_date": val.validar_transaction_date,
}
TRANSFORMACIONES = {
    "country": tr.normalizar_country,
    "category": tr.normalizar_category,
    "amount": tr.normalizar_amount,
    "quantity": tr.normalizar_quantity,
    "transaction_date": tr.normalizar_transaction_date,
}


def procesar_fila(fila: dict[str, object]) -> Tuple[bool, dict[str, object] | str]:
    ok, motivo = val.validar_campos_obligatorios(fila, CAMPOS_OBLIGATORIOS)
    if not ok:
        return False, motivo

    for campo, fn_validadora in VALIDADORES.items():
        ok, motivo = fn_validadora(fila.get(campo))
        if not ok:
            return False, motivo
    try:
        fila_limpia = {}
        for campo, fn_transformadora in TRANSFORMACIONES.items():
            fila_limpia[campo] = fn_transformadora(fila.get(campo))
    except ValueError as e:
        return False, str(e)
    return True, fila_limpia


def aplicar_pipeline(
    ruta_archivo: str,
) -> dict[str, object]:
    """
    Ejecuta el pipeline completo:
    - lee filas del CSV
    - valida
    - transforma
    - escribe en clean.csv o rejects.csv (en el directorio ../data/)
    """
    base_dir = os.path.dirname(__file__)
    ruta_clean = os.path.abspath(os.path.join(base_dir, "..", "data", "clean.csv"))
    ruta_rejects = os.path.abspath(os.path.join(base_dir, "..", "data", "rejects.csv"))

    # Asegurar que el directorio de salida exista
    os.makedirs(os.path.dirname(ruta_clean), exist_ok=True)

    fieldnames_clean = list(CAMPOS_OBLIGATORIOS)
    fieldnames_rejects = list(CAMPOS_OBLIGATORIOS) + ["motivo"]

    total_ok = 0
    total_reject = 0

    with open(ruta_clean, "w", newline="", encoding="utf-8") as f_clean, open(
        ruta_rejects, "w", newline="", encoding="utf-8"
    ) as f_reject:
        writer_clean = csv.DictWriter(f_clean, fieldnames=fieldnames_clean)
        writer_reject = csv.DictWriter(f_reject, fieldnames=fieldnames_rejects)
        writer_clean.writeheader()
        writer_reject.writeheader()

        for fila in iterar_filas_csv(ruta_archivo):
            ok, resultado = procesar_fila(fila)
            if ok:
                writer_clean.writerow(resultado)
                total_ok += 1
            else:
                reject_row = {c: fila.get(c) for c in CAMPOS_OBLIGATORIOS}
                reject_row["motivo"] = resultado
                writer_reject.writerow(reject_row)
                total_reject += 1

    return {"ok": total_ok, "rejects": total_reject}


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    ruta_csv = os.path.abspath(os.path.join(base_dir, "..", "data", "datos.csv"))
    
    print("Iniciando pipeline ETL...")
    try:
        resultado = aplicar_pipeline(ruta_csv)
        print(f"Ejecución completada exitosamente: {resultado}")
    except Exception as e:
        print(f"Error al ejecutar el pipeline: {e}")
