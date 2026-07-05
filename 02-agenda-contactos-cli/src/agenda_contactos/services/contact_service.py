import sqlite3
from typing import Dict

from agenda_contactos.repositories.contact_repository import ContactRepository
from agenda_contactos.services.validators import Validators
from agenda_contactos.decorators.timing import measure_time

ContactDict = Dict[str, str | None]


class ContactService:
    def __init__(self, repository: ContactRepository):
        self.repository = repository

    def normalize_contact(
        self,
        nombre: str,
        telefono: str,
        email: str | None = None,
        categoria: str = "personal",
        descripcion: str | None = None,
    ) -> ContactDict:
        nombre_n = str(nombre).strip().lower()
        telefono_n = str(telefono).strip()
        email_n = str(email).strip().lower() if email else None
        categoria_n = str(categoria).strip().lower() if categoria else "personal"
        descripcion_n = str(descripcion).strip() if descripcion else None

        return {
            "nombre": nombre_n,
            "telefono": telefono_n,
            "email": email_n,
            "categoria": categoria_n,
            "descripcion": descripcion_n,
        }

    def _prepare_contact(self, raw: ContactDict) -> ContactDict:
        nombre_v = Validators._validate_name(raw.get("nombre", ""))
        telefono_v = Validators._validate_telephone(raw.get("telefono", ""))
        email_v = Validators._validate_email(raw.get("email"))

        categoria_raw = raw.get("categoria")
        descripcion_raw = raw.get("descripcion")

        return self.normalize_contact(
            nombre=nombre_v,
            telefono=telefono_v,
            email=email_v,
            categoria=categoria_raw if categoria_raw else "personal",
            descripcion=descripcion_raw,
        )

    @measure_time
    def create_contact(self, raw_params: ContactDict) -> int:
        contact_data = self._prepare_contact(raw_params)
        try:
            return self.repository.add_contact(**contact_data)
        except sqlite3.IntegrityError as e:
            raise ValueError("contacto_duplicado") from e

    @measure_time
    def list_contacts(self) -> list[tuple]:
        return self.repository.list_contacts()

    def list_by_category(self, category: str) -> list[tuple]:
        category_n = str(category).strip().lower()
        if not category_n:
            raise ValueError("categoria_requerida")
        return self.repository.list_by_category(category_n)

    def search_contacts(self, termino: str) -> list[tuple]:
        termino_n = str(termino).strip()
        if not termino_n:
            raise ValueError("termino_requerido")
        return self.repository.search_contacts(termino_n)

    def get_by_id(self, contact_id: int) -> tuple | None:
        if not isinstance(contact_id, int) or contact_id <= 0:
            raise ValueError("id_invalido")
        return self.repository.get_by_id(contact_id)

    def delete_contact(self, contact_id: int) -> bool:
        if not isinstance(contact_id, int) or contact_id <= 0:
            raise ValueError("id_invalido")
        return self.repository.delete_contact(contact_id)

    @measure_time
    def update_contact(self, contact_id: int, raw_params: ContactDict) -> bool:
        if not isinstance(contact_id, int) or contact_id <= 0:
            raise ValueError("id_invalido")

        current = self.repository.get_by_id(contact_id)
        if current is None:
            return False

        _, nombre_a, telefono_a, email_a, categoria_a, descripcion_a, _ = current

        nombre_new = raw_params.get("nombre")
        telefono_new = raw_params.get("telefono")
        email_new = raw_params.get("email")
        categoria_new = raw_params.get("categoria")
        descripcion_new = raw_params.get("descripcion")

        merged: ContactDict = {
            "nombre": nombre_a if nombre_new in (None, "") else nombre_new,
            "telefono": telefono_a if telefono_new in (None, "") else telefono_new,
            "email": email_a if email_new in (None, "") else email_new,
            "categoria": categoria_a if categoria_new in (None, "") else categoria_new,
            "descripcion": (
                descripcion_a if descripcion_new in (None, "") else descripcion_new
            ),
        }

        data = self._prepare_contact(merged)

        return self.repository.update_contact(
            contacto_id=contact_id,
            nombre=str(data["nombre"]),
            telefono=str(data["telefono"]),
            email=data["email"],
            categoria=str(data["categoria"]),
        )
