# PostgreSQL para Biblioteca Pública (SQL & Python Integration)

Este proyecto demuestra el diseño lógico y físico de una base de datos relacional para un sistema de biblioteca pública escolar utilizando **PostgreSQL**. Incluye el esquema de relaciones, consultas analíticas avanzadas, optimización de consultas mediante índices, control transaccional robusto y un script de integración segura en Python con `psycopg2`.

## Esquema Entidad-Relación (Diagrama ASCII)

```text
  ┌──────────────┐             ┌──────────────┐
  │  CATEGORIAS  │             │   AUTORES    │
  ├──────────────┤             ├──────────────┤
  │ PK category_id ◄──┐        │ PK autor_id  │
  │    name      │    │        └──────▲───────┘
  └──────────────┘    │               │
                      │               │ (N:M) via libros_autores
  ┌──────────────┐    │        ┌──────┴───────┐
  │    LIBROS    │    │        │LIBROS_AUTORES│
  ├──────────────┤    │        ├──────────────┤
  │ PK libro_id  │    │        │ FK libro_id  │
  │    title     │    │        │ FK autor_id  │
  │    isbn      │    │        └──────────────┘
  │    year_pub  │    │
  │ FK category_id ───┘
  └──────▲───────┘
         │
         │ (1:N)
  ┌──────┴───────┐             ┌──────────────┐
  │  EJEMPLARES  │             │    SOCIOS    │
  ├──────────────┤             ├──────────────┤
  │ PK ejemplar_id◄───┐        │ PK socio_id  │
  │    stock_code│    │        │    full_name │
  │    status    │    │        │    email     │
  │ FK libro_id  │    │        └──────▲───────┘
  └──────────────┘    │               │
                      │               │ (1:N)
                      │        ┌──────┴───────┐
                      │        │  PRESTAMOS   │
                      │        ├──────────────┤
                      └────────│ FK ejemplar_id│
                               │ FK socio_id  │
                               │    loan_date │
                               │   return_date│
                               └──────────────┘
```

## Estructura del Código

- `sql/01_esquema.sql`: DDL de creación de tablas, llaves primarias, llaves foráneas, CHECK constraints y carga de datos iniciales.
- `sql/02_queries.sql`: Consultas analíticas (agregaciones, JOINs internos/externos, HAVING y subconsultas).
- `sql/03_indices.sql`: Definición de índices B-Tree de rendimiento para optimizar los accesos a datos.
- `sql/04_transacciones.sql`: Lógica transaccional para préstamos, retornos y simulación de rollbacks (ACID).
- `sql/05_explain_analyze.sql`: Ejemplos reales de cómo auditar el rendimiento usando `EXPLAIN ANALYZE`.
- `src/connection.py`: Script de Python usando `psycopg2` para ejecutar transacciones automáticas y seguras contra PostgreSQL.

## Optimización de Rendimiento
Se definieron índices en las llaves foráneas de mayor uso analítico:
- `idx_prestamos_socio_id`: Optimiza la búsqueda de historial de préstamos por socio.
- `idx_ejemplares_libro_id`: Agiliza la búsqueda de copias de un libro en particular.
- `idx_prestamos_ejemplar_id`: Optimiza el rastreo del historial de préstamo de un ejemplar físico.
- Un índice parcial `idx_ejemplares_disponibles` (filtrado por `status = 'available'`) para acelerar búsquedas de catálogo de libros que se pueden prestar inmediatamente.

## Configuración y Ejecución

### 1. Correr los Scripts SQL en PostgreSQL
Crea una base de datos en tu PostgreSQL (ej: `backend_db`) y ejecuta los scripts en orden:
```bash
psql -U tu_usuario -d backend_db -f sql/01_esquema.sql
psql -U tu_usuario -d backend_db -f sql/02_queries.sql
psql -U tu_usuario -d backend_db -f sql/03_indices.sql
```

### 2. Ejecutar la Integración de Python
El script utiliza `psycopg2` para comunicarse de forma segura con la base de datos.
Puedes definir las credenciales utilizando variables de entorno. En caso contrario, usará los valores de desarrollo local por defecto:

```bash
# Variables de entorno opcionales (Linux/macOS)
export DB_NAME="backend_db"
export DB_USER="backend_user"
export DB_PASSWORD="tu_password"
export DB_HOST="localhost"
export DB_PORT="5432"

# En Windows (PowerShell)
$env:DB_NAME="backend_db"
$env:DB_USER="backend_user"
$env:DB_PASSWORD="tu_password"

# Ejecutar el script
python src/connection.py
```
*El script realizará una consulta general de la biblioteca y simulará una transacción completa de préstamo (inserción + actualización de estado).*
