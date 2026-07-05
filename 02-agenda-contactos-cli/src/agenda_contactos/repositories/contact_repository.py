from agenda_contactos.db.session import SQLiteSession
from pathlib import Path


class ContactRepository:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def add_contact(
        self,
        nombre: str,
        telefono: str,
        email: str | None = None,
        categoria: str = "personal",
        descripcion: str | None = None,
    ) -> int:
        with SQLiteSession(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contactos(nombre, telefono, email, categoria, descripcion) VALUES (?,?,?,?,?)",
                (nombre, telefono, email, categoria, descripcion),
            )

        return cursor.lastrowid

    def list_contacts(self) -> list[tuple]:
        with SQLiteSession(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contactos")
            contacts = cursor.fetchall()
            return contacts

    def list_by_category(self, categoria: str) -> list[tuple]:
        with SQLiteSession(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM contactos WHERE categoria = ? ORDER BY id", (categoria,)
            )
            contacts = cursor.fetchall()
            return contacts

    def search_contacts(self, termino: str) -> list[tuple]:
        with SQLiteSession(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM contactos WHERE nombre LIKE ? OR email LIKE ? OR telefono LIKE ?",
                (f"%{termino}%", f"%{termino}%", f"%{termino}%"),
            )
            contacts = cursor.fetchall()
            return contacts

    def get_by_id(self, contacto_id: int) -> tuple | None:
        with SQLiteSession(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contactos WHERE id = ?", (contacto_id,))
            contact = cursor.fetchone()
            return contact

    def update_contact(
        self,
        contacto_id: int,
        nombre: str,
        telefono: str,
        email: str | None,
        categoria: str,
    ) -> bool:
        with SQLiteSession(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE contactos SET nombre = ?, telefono = ?, email = ?, categoria = ? WHERE id = ?",
                (nombre, telefono, email, categoria, contacto_id),
            )
            return cursor.rowcount > 0

    def delete_contact(self, contact_id: int) -> bool:
        with SQLiteSession(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contactos WHERE id = ?", (contact_id,))
            return cursor.rowcount > 0
