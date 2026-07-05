-- ============================================================================
-- Proyecto: Base de Datos de Biblioteca Pública / Escolar
-- Archivo: 03_indices.sql
-- Motor: PostgreSQL
-- Descripción: Creación de índices optimizados para llaves foráneas y
--              campos de filtrado frecuente para mejorar planes de ejecución.
-- ============================================================================

-- Nota conceptual de optimización:
-- Las columnas llave primaria (PRIMARY KEY) y con restricción de unicidad (UNIQUE)
-- como 'libros.libro_id', 'libros.isbn' y 'socios.socio_id' ya son indexadas
-- automáticamente mediante índices B-Tree por PostgreSQL. Por lo tanto, no es necesario
-- crear índices explícitos sobre ellas. Nos enfocamos en las llaves foráneas y
-- filtros de negocio de alta cardinalidad.

-- 1. Índice en Préstamos por Socio
-- Justificación: Búsquedas frecuentes de historial por socio (WHERE socio_id = X)
-- y Joins comunes entre las tablas 'socios' y 'prestamos'.
CREATE INDEX IF NOT EXISTS idx_prestamos_socio_id
ON prestamos(socio_id);

-- 2. Índice en Ejemplares por Libro
-- Justificación: Permite buscar rápidamente los ejemplares físicos de un libro
-- específico y acelera los joins entre 'libros' y 'ejemplares' (Q8, Q14).
CREATE INDEX IF NOT EXISTS idx_ejemplares_libro_id
ON ejemplares(libro_id);

-- 3. Índice en Préstamos por Ejemplar
-- Justificación: Acelera las búsquedas del historial de uso de un ejemplar físico
-- y los joins correspondientes (Q4).
CREATE INDEX IF NOT EXISTS idx_prestamos_ejemplar_id
ON prestamos(ejemplar_id);

-- 4. Índice parcial de Ejemplares Disponibles (Opcional - Avanzado)
-- Justificación: Acelera drásticamente la búsqueda de libros listos para préstamo,
-- ignorando los ejemplares en mantenimiento o ya prestados.
CREATE INDEX IF NOT EXISTS idx_ejemplares_disponibles
ON ejemplares(libro_id)
WHERE status = 'available';
