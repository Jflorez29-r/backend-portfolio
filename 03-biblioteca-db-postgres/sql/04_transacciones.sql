-- ============================================================================
-- Proyecto: Base de Datos de Biblioteca Pública / Escolar
-- Archivo: 04_transacciones.sql
-- Motor: PostgreSQL
-- Descripción: Casos de uso transaccionales reales que aseguran la consistencia
--              de la base de datos bajo fallos (propiedades ACID).
-- ============================================================================

-- ============================================================================
-- Caso 1: Registrar Préstamo de un Libro
-- Lógica: Inserta en 'prestamos' y cambia el estado del ejemplar a 'borrowed'.
-- ============================================================================
BEGIN;

-- 1. Insertamos la fila del préstamo (Socio ID 3 toma Ejemplar ID 1)
INSERT INTO prestamos (socio_id, ejemplar_id, loan_date, return_date)
VALUES (3, 1, CURRENT_DATE, NULL);

-- 2. Actualizamos el estado del ejemplar físico a prestado
UPDATE ejemplares
SET status = 'borrowed'
WHERE ejemplar_id = 1;

-- Si ambas operaciones tienen éxito, confirmamos los cambios
COMMIT;


-- ============================================================================
-- Caso 2: Devolución de un Libro
-- Lógica: Registra la fecha de devolución en 'prestamos' y cambia el estado
--         del ejemplar de vuelta a 'available'.
-- ============================================================================
BEGIN;

-- 1. Establecemos la fecha de retorno del préstamo activo (Socio ID 3, Ejemplar 1)
UPDATE prestamos
SET return_date = CURRENT_DATE
WHERE socio_id = 3 
  AND ejemplar_id = 1 
  AND return_date IS NULL;

-- 2. Devolvemos el estado del ejemplar físico a disponible
UPDATE ejemplares
SET status = 'available'
WHERE ejemplar_id = 1;

COMMIT;


-- ============================================================================
-- Caso 3: Simulación de Transacción Fallida (Rollback Automático)
-- Lógica: Si intentamos prestar un libro y algo falla o el libro está en
--         mantenimiento, cancelamos toda la operación para evitar registros huérfanos.
-- ============================================================================
BEGIN;

-- 1. Intentamos registrar el préstamo de un ejemplar en mantenimiento (Ejemplar ID 6 es 'maintenance')
-- El sistema del negocio debería comprobar previamente si está 'available', pero si falla:
INSERT INTO prestamos (socio_id, ejemplar_id, loan_date, return_date)
VALUES (2, 6, CURRENT_DATE, NULL);

-- 2. Supongamos que aquí ocurre un error inesperado de integridad de datos 
-- o forzamos un ROLLBACK porque la validación lógica de la aplicación falló.
ROLLBACK;
-- Nota: La base de datos queda exactamente como estaba antes de ejecutar BEGIN.
