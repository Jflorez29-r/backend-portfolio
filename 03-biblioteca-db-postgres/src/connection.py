"""
Proyecto: Integración de Python con PostgreSQL
Archivo: connection.py
Motor: PostgreSQL via psycopg2-binary
Descripción: Conexión segura parametrizada mediante variables de entorno e
             implementación de transacciones ACID seguras.
"""

import os
import psycopg2
from psycopg2 import Error


def get_db_connection():
    """
    Establece conexión a la base de datos leyendo las variables de entorno.
    Utiliza valores predeterminados para desarrollo local si no están definidas.
    """
    return psycopg2.connect(
        dbname=os.environ.get("DB_NAME", "backend_db"),
        user=os.environ.get("DB_USER", "backend_user"),
        password=os.environ.get("DB_PASSWORD", "admin123"),
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
    )


def registrar_prestamo(socio_id: int, ejemplar_id: int) -> bool:
    """
    Registra un préstamo de libro de forma transaccional.
    Inserta en la tabla 'prestamos' y actualiza el estado de 'ejemplares' a 'borrowed'.
    Maneja confirmaciones y rollbacks de forma segura.
    """
    connection = None
    cursor = None
    success = False

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # 1. Validar que el ejemplar esté disponible antes de proceder
        cursor.execute("SELECT status FROM ejemplares WHERE ejemplar_id = %s;", (ejemplar_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"Error: El ejemplar con ID {ejemplar_id} no existe.")
            return False
            
        estado_actual = resultado[0]
        if estado_actual != "available":
            print(f"Error: El ejemplar {ejemplar_id} no está disponible. Estado: {estado_actual}")
            return False

        # 2. Insertar préstamo
        cursor.execute(
            "INSERT INTO prestamos (socio_id, ejemplar_id, loan_date, return_date) VALUES (%s, %s, CURRENT_DATE, NULL) RETURNING prestamo_id;",
            (socio_id, ejemplar_id)
        )
        prestamo_id = cursor.fetchone()[0]

        # 3. Cambiar estado del ejemplar físico a prestado
        cursor.execute(
            "UPDATE ejemplares SET status = 'borrowed' WHERE ejemplar_id = %s;",
            (ejemplar_id,)
        )

        # Confirmar los cambios en la base de datos (Commit)
        connection.commit()
        print(f"Éxito: Préstamo registrado con ID {prestamo_id}. Ejemplar {ejemplar_id} marcado como 'borrowed'.")
        success = True

    except Error as e:
        # En caso de cualquier excepción SQL o de conexión, se revierten los cambios pendientes
        if connection is not None:
            connection.rollback()
        print("Database error ocurrido durante la transacción:", e)
        
    finally:
        # Garantizar el cierre de recursos
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
            
    return success


def mostrar_resumen_biblioteca():
    """Consulta rápida para verificar el estado de la base de datos."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Obtener cantidad total de libros
        cursor.execute("SELECT COUNT(*) FROM libros;")
        total_libros = cursor.fetchone()[0]

        # Obtener cantidad de préstamos activos
        cursor.execute("SELECT COUNT(*) FROM prestamos WHERE return_date IS NULL;")
        prestamos_activos = cursor.fetchone()[0]

        print("--- Resumen de Biblioteca ---")
        print(f"Total de libros registrados: {total_libros}")
        print(f"Préstamos activos actualmente: {prestamos_activos}")
        print("-----------------------------")

    except Error as e:
        print("Error al consultar resumen:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    print("Iniciando pruebas de integración de base de datos...")
    
    # 1. Consultar estado inicial
    mostrar_resumen_biblioteca()
    
    # 2. Intentar registrar un préstamo (Ejemplo con Socio 3, Ejemplar 1)
    print("\nIntentando préstamo de prueba...")
    registrar_prestamo(socio_id=3, ejemplar_id=1)
    
    # 3. Consultar estado final
    print()
    mostrar_resumen_biblioteca()
