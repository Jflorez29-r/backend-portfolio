from agenda_contactos.db.session import SQLiteSession


CREATE_CONTACTOS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS contactos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    categoria TEXT DEFAULT 'personal',
    descripcion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


def init_db(db_path) -> None:
    with SQLiteSession(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_CONTACTOS_TABLE_SQL)
