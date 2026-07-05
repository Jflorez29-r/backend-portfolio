-- ============================================================================
-- Proyecto: Base de Datos de Biblioteca Pública / Escolar
-- Archivo: 01_esquema.sql
-- Motor: PostgreSQL
-- Descripción: Creación del esquema relacional, constraints e inserción
--              de datos semilla para demostraciones.
-- ============================================================================

-- 1. Limpieza previa de tablas si existen (para facilitar despliegue)
DROP TABLE IF EXISTS prestamos CASCADE;
DROP TABLE IF EXISTS ejemplares CASCADE;
DROP TABLE IF EXISTS libros_autores CASCADE;
DROP TABLE IF EXISTS libros CASCADE;
DROP TABLE IF EXISTS autores CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS socios CASCADE;

-- 2. Creación de Tabla: Socios
CREATE TABLE socios (
    socio_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Creación de Tabla: Categorías
CREATE TABLE categorias (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- 4. Creación de Tabla: Autores
CREATE TABLE autores (
    autor_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL
);

-- 5. Creación de Tabla: Libros
CREATE TABLE libros (
    libro_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    year_of_publication INTEGER CHECK (year_of_publication > 0 AND year_of_publication <= EXTRACT(YEAR FROM CURRENT_DATE)),
    category_id INTEGER REFERENCES categorias(category_id) ON DELETE SET NULL
);

-- 6. Creación de Tabla Intermedia: Libros_Autores (Relación N:M)
CREATE TABLE libros_autores (
    libro_id INTEGER REFERENCES libros(libro_id) ON DELETE CASCADE,
    autor_id INTEGER REFERENCES autores(autor_id) ON DELETE CASCADE,
    PRIMARY KEY (libro_id, autor_id)
);

-- 7. Creación de Tabla: Ejemplares
CREATE TABLE ejemplares (
    ejemplar_id SERIAL PRIMARY KEY,
    stock_code VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'available' CHECK (status IN ('available', 'borrowed', 'maintenance')),
    libro_id INTEGER REFERENCES libros(libro_id) ON DELETE CASCADE
);

-- 8. Creación de Tabla: Préstamos
CREATE TABLE prestamos (
    prestamo_id SERIAL PRIMARY KEY,
    socio_id INTEGER REFERENCES socios(socio_id) ON DELETE RESTRICT,
    ejemplar_id INTEGER REFERENCES ejemplares(ejemplar_id) ON DELETE RESTRICT,
    loan_date DATE DEFAULT CURRENT_DATE NOT NULL,
    return_date DATE CHECK (return_date IS NULL OR return_date >= loan_date)
);

-- ============================================================================
-- inserción de datos mock / semilla
-- ============================================================================

-- Socios
INSERT INTO socios (full_name, email) VALUES
('Juan Pérez', 'juan.perez@example.com'),
('Ana Gómez', 'ana.gomez@example.com'),
('Luis López', 'luis.lopez@example.com'),
('María Rodríguez', 'maria.rodriguez@example.com'),
('Carlos Sánchez', 'carlos.sanchez@test.com');

-- Categorías
INSERT INTO categorias (name) VALUES
('food'),
('books'),
('electronics'),
('home'),
('sports'),
('clothing');

-- Autores
INSERT INTO autores (full_name) VALUES
('Gabriel García Márquez'),
('J.K. Rowling'),
('George Orwell'),
('Stephen King'),
('Douglas Adams');

-- Libros
INSERT INTO libros (title, isbn, year_of_publication, category_id) VALUES
('Cien años de soledad', '978-0307474728', 1967, 2),
('Harry Potter and the Philosopher''s Stone', '978-0747532699', 1997, 2),
('1984', '978-0451524935', 1949, 2),
('The Shining', '978-0307743657', 1977, 2),
('The Hitchhiker''s Guide to the Galaxy', '978-0345391803', 1979, 2);

-- Libros_Autores
INSERT INTO libros_autores (libro_id, autor_id) VALUES
(1, 1), -- Cien años de soledad -> G.G.M
(2, 2), -- Harry Potter -> J.K.R
(3, 3), -- 1984 -> G. Orwell
(4, 4), -- The Shining -> S. King
(5, 5); -- Hitchhiker -> D. Adams

-- Ejemplares
INSERT INTO ejemplares (stock_code, status, libro_id) VALUES
('EJ-100-A', 'available', 1),
('EJ-100-B', 'borrowed', 1),
('EJ-200-A', 'available', 2),
('EJ-200-B', 'borrowed', 2),
('EJ-300-A', 'available', 3),
('EJ-400-A', 'maintenance', 4),
('EJ-500-A', 'available', 5);

-- Préstamos
INSERT INTO prestamos (socio_id, ejemplar_id, loan_date, return_date) VALUES
(1, 2, '2026-06-01', NULL),
(2, 4, '2026-06-10', '2026-06-15'),
(3, 4, '2026-06-20', NULL),
(1, 4, '2026-06-25', '2026-06-28');
