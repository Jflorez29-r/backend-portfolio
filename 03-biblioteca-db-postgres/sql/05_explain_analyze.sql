-- ============================================================================
-- Proyecto: Base de Datos de Biblioteca Pública / Escolar
-- Archivo: 05_explain_analyze.sql
-- Motor: PostgreSQL
-- Descripción: Guía práctica de optimización de consultas y análisis de
--              planes de ejecución mediante EXPLAIN y EXPLAIN ANALYZE.
-- ============================================================================

-- El comando EXPLAIN muestra el plan de ejecución que el planificador de consultas
-- de PostgreSQL genera. EXPLAIN ANALYZE ejecuta realmente la consulta, midiendo
-- tiempos reales y recursos utilizados.

-- ============================================================================
-- Análisis 1: Búsqueda de préstamos por socio ANTES y DESPUÉS del índice
-- ============================================================================

-- Consulta objetivo:
-- SELECT * FROM prestamos WHERE socio_id = 3;

-- 1. Ejecución ANTES de crear el índice:
-- (Para simular, eliminamos temporalmente el índice)
-- DROP INDEX IF EXISTS idx_prestamos_socio_id;
-- EXPLAIN ANALYZE SELECT * FROM prestamos WHERE socio_id = 3;

-- Resultado esperado en base de datos poblada con volumen (Seq Scan):
-- -> Seq Scan on prestamos  (cost=0.00..15.50 rows=15 width=32) (actual time=0.015..0.120 rows=15 loops=1)
--      Filter: (socio_id = 3)
--      Rows Removed by Filter: 24985
-- Planning Time: 0.082 ms
-- Execution Time: 2.145 ms
--
-- Explicación: PostgreSQL se ve obligado a hacer un "Sequential Scan" (escanear
-- fila por fila todo el disco) leyendo miles de registros innecesarios y descartándolos.

-- 2. Ejecución DESPUÉS de crear el índice:
-- CREATE INDEX idx_prestamos_socio_id ON prestamos(socio_id);
-- EXPLAIN ANALYZE SELECT * FROM prestamos WHERE socio_id = 3;

-- Resultado esperado (Index Scan):
-- -> Index Scan using idx_prestamos_socio_id on prestamos  (cost=0.15..8.30 rows=15 width=32) (actual time=0.010..0.022 rows=15 loops=1)
--      Index Cond: (socio_id = 3)
-- Planning Time: 0.112 ms
-- Execution Time: 0.038 ms
--
-- Explicación: PostgreSQL ahora usa el índice B-Tree 'idx_prestamos_socio_id' para
-- saltar directamente a la posición física de las 15 filas correspondientes. 
-- El escaneo pasa de ser O(N) a O(log N), mejorando drásticamente el tiempo.


-- ============================================================================
-- Análisis 2: Join complejo e indexación
-- ============================================================================
-- EXPLAIN ANALYZE
SELECT s.full_name, p.loan_date, e.stock_code
FROM socios AS s
INNER JOIN prestamos AS p ON s.socio_id = p.socio_id
INNER JOIN ejemplares AS e ON e.ejemplar_id = p.ejemplar_id
WHERE s.full_name = 'Juan Pérez';

-- En este plan de ejecución, PostgreSQL combinará:
-- 1. Un Index Scan (o Seq Scan si la tabla es muy chica) en 'socios' usando el índice único del nombre.
-- 2. Un Index Scan en 'prestamos' a través de 'idx_prestamos_socio_id'.
-- 3. Un Index Scan en 'ejemplares' a través de su llave primaria.
-- Usando algoritmos de Join como Nested Loop o Hash Join de manera altamente optimizada.
