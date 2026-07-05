-- ============================================================================
-- Proyecto: Base de Datos de Biblioteca Pública / Escolar
-- Archivo: 02_queries.sql
-- Motor: PostgreSQL
-- Descripción: Consultas de demostración que cubren filtros, joins,
--              agregaciones y subconsultas complejas.
-- ============================================================================

-- ============================================================================
-- 1. SELECT y filtros básicos
-- ============================================================================

-- Q1: Listar título, isbn y año de publicación de todos los libros ordenados
-- de los más recientes a los más antiguos.
SELECT title, isbn, year_of_publication
FROM libros 
ORDER BY year_of_publication DESC;

-- Q2: Mostrar nombre completo y email de los socios cuyo correo contenga 'example'.
SELECT full_name, email
FROM socios
WHERE email LIKE '%example%';

-- Q3: Mostrar los ejemplares que no estén disponibles ('available').
SELECT * 
FROM ejemplares
WHERE status <> 'available';


-- ============================================================================
-- 2. INNER JOINS (Relaciones fuertes)
-- ============================================================================

-- Q4: Mostrar el nombre del socio, la fecha del préstamo y el código de stock
-- del ejemplar prestado.
SELECT s.full_name, p.loan_date, e.stock_code
FROM socios AS s
INNER JOIN prestamos AS p ON s.socio_id = p.socio_id
INNER JOIN ejemplares AS e ON e.ejemplar_id = p.ejemplar_id;

-- Q5: Mostrar el título de cada libro con el nombre completo de su respectivo autor.
SELECT l.title, a.full_name
FROM libros AS l
INNER JOIN libros_autores AS la ON l.libro_id = la.libro_id
INNER JOIN autores AS a ON a.autor_id = la.autor_id;

-- Q6: Mostrar el título del libro y el nombre de su categoría asociada.
SELECT l.title, c.name
FROM libros AS l
INNER JOIN categorias AS c ON l.category_id = c.category_id;


-- ============================================================================
-- 3. LEFT JOINS (Relaciones opcionales)
-- ============================================================================

-- Q7: Mostrar todos los socios y, si existen, sus préstamos (incluso si no tienen).
SELECT s.full_name, p.loan_date
FROM socios AS s
LEFT JOIN prestamos AS p ON s.socio_id = p.socio_id;

-- Q8: Mostrar todos los libros y sus ejemplares correspondientes (si existen).
SELECT l.title, e.stock_code
FROM libros AS l
LEFT JOIN ejemplares AS e ON l.libro_id = e.libro_id;

-- Q9: Mostrar todos los autores y la lista de libros que han escrito.
SELECT a.full_name, l.title
FROM autores AS a
LEFT JOIN libros_autores AS la ON a.autor_id = la.autor_id
LEFT JOIN libros AS l ON l.libro_id = la.libro_id;


-- ============================================================================
-- 4. Agregaciones y agrupamiento (GROUP BY y HAVING)
-- ============================================================================

-- Q10: Contar cuántos ejemplares existen agrupados por estado.
SELECT status, COUNT(*) AS total_ejemplares
FROM ejemplares
GROUP BY status;

-- Q11: Mostrar cada categoría y la cantidad de libros que pertenecen a ella.
SELECT c.name, COUNT(l.libro_id) AS total_libros
FROM categorias AS c
LEFT JOIN libros AS l ON c.category_id = l.category_id
GROUP BY c.category_id, c.name;

-- Q12: Mostrar cada socio y cuántos préstamos ha tenido, de mayor a menor.
SELECT s.full_name, COUNT(p.prestamo_id) AS total_prestamos
FROM socios AS s
LEFT JOIN prestamos AS p ON s.socio_id = p.socio_id
GROUP BY s.socio_id, s.full_name
ORDER BY total_prestamos DESC;

-- Q13: Filtrar únicamente a los socios que hayan tenido estrictamente más de 1 préstamo.
SELECT s.full_name, COUNT(p.prestamo_id) AS total_prestamos
FROM socios AS s
LEFT JOIN prestamos AS p ON s.socio_id = p.socio_id
GROUP BY s.socio_id, s.full_name
HAVING COUNT(p.prestamo_id) > 1;


-- ============================================================================
-- 5. LEFT JOIN + GROUP BY avanzado
-- ============================================================================

-- Q14: Mostrar todos los libros y su cantidad de ejemplares, incluyendo los que no tienen.
SELECT l.title, COUNT(e.ejemplar_id) AS total_ejemplares
FROM libros AS l
LEFT JOIN ejemplares AS e ON l.libro_id = e.libro_id
GROUP BY l.libro_id, l.title;


-- ============================================================================
-- 6. Subconsultas (Subqueries)
-- ============================================================================

-- Q15: Mostrar los libros cuya fecha de publicación sea posterior al año promedio general.
SELECT title, year_of_publication
FROM libros
WHERE year_of_publication > (SELECT AVG(year_of_publication) FROM libros);
