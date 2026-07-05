import pytest
import sys
import os
import sqlite3
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from agenda_contactos.db.schema import init_db
from agenda_contactos.repositories.contact_repository import ContactRepository
from agenda_contactos.services.contact_service import ContactService
from agenda_contactos.services.validators import Validators


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_contactos.db"
    init_db(db_file)
    return db_file


@pytest.fixture
def service(temp_db):
    repo = ContactRepository(temp_db)
    return ContactService(repo)


# Tests de validadores individuales
def test_validators():
    # Nombre
    assert Validators._validate_name("Juan Perez") == "juan perez"
    with pytest.raises(ValueError, match="nombre_requerido"):
        Validators._validate_name("")
    with pytest.raises(ValueError, match="nombre_requerido"):
        Validators._validate_name("na")

    # Teléfono
    assert Validators._validate_telephone("1234567") == "1234567"
    assert Validators._validate_telephone("3001234567") == "3001234567"
    with pytest.raises(ValueError, match="telefono_requerido"):
        Validators._validate_telephone("")
    with pytest.raises(ValueError, match="telefono_invalido"):
        Validators._validate_telephone("12345")  # muy corto
    with pytest.raises(ValueError, match="telefono_invalido"):
        Validators._validate_telephone("12345678901")  # muy largo
    with pytest.raises(ValueError, match="telefono_invalido"):
        Validators._validate_telephone("123456a")  # caracteres no numéricos

    # Email
    assert Validators._validate_email("test@domain.com") == "test@domain.com"
    assert Validators._validate_email(None) is None
    assert Validators._validate_email("") is None
    with pytest.raises(ValueError, match="email_invalido"):
        Validators._validate_email("invalid_email")
    with pytest.raises(ValueError, match="email_invalido"):
        Validators._validate_email("invalid@domain")


# Tests del Servicio (CRUD)
def test_create_and_get_contact(service):
    raw_contact = {
        "nombre": "Carlos Perez",
        "telefono": "3007654321",
        "email": "carlos@perez.com",
        "categoria": "Trabajo",
        "descripcion": "Colega de desarrollo"
    }
    
    contact_id = service.create_contact(raw_contact)
    assert contact_id == 1

    contact = service.get_by_id(contact_id)
    assert contact is not None
    # Estructura del registro: (id, nombre, telefono, email, categoria, descripcion, fecha_registro)
    assert contact[0] == 1
    assert contact[1] == "carlos perez"  # Normalizado a minúsculas
    assert contact[2] == "3007654321"
    assert contact[3] == "carlos@perez.com"
    assert contact[4] == "trabajo"
    assert contact[5] == "Colega de desarrollo"


def test_create_duplicate_contact(service):
    contact1 = {
        "nombre": "Ana Gomez",
        "telefono": "3111234567",
        "email": "ana@gomez.com"
    }
    service.create_contact(contact1)

    # Duplicado por teléfono
    contact2 = {
        "nombre": "Ana Maria",
        "telefono": "3111234567",
        "email": "anamaria@gomez.com"
    }
    with pytest.raises(ValueError, match="contacto_duplicado"):
        service.create_contact(contact2)


def test_list_contacts(service):
    c1 = {"nombre": "Ana Gomez", "telefono": "3111234567"}
    c2 = {"nombre": "Luis Lopez", "telefono": "3229876543"}
    service.create_contact(c1)
    service.create_contact(c2)

    contacts = service.list_contacts()
    assert len(contacts) == 2
    assert contacts[0][1] == "ana gomez"
    assert contacts[1][1] == "luis lopez"


def test_list_by_category(service):
    c1 = {"nombre": "Ana Gomez", "telefono": "3111234567", "categoria": "Personal"}
    c2 = {"nombre": "Luis Lopez", "telefono": "3229876543", "categoria": "Trabajo"}
    service.create_contact(c1)
    service.create_contact(c2)

    trabajo_contacts = service.list_by_category("Trabajo")
    assert len(trabajo_contacts) == 1
    assert trabajo_contacts[0][1] == "luis lopez"


def test_search_contacts(service):
    c1 = {"nombre": "Ana Gomez", "telefono": "3111234567", "email": "ana@gmail.com"}
    c2 = {"nombre": "Luis Lopez", "telefono": "3229876543"}
    service.create_contact(c1)
    service.create_contact(c2)

    results = service.search_contacts("gomez")
    assert len(results) == 1
    assert results[0][1] == "ana gomez"

    results_by_phone = service.search_contacts("9876")
    assert len(results_by_phone) == 1
    assert results_by_phone[0][1] == "luis lopez"


def test_update_contact(service):
    c1 = {"nombre": "Ana Gomez", "telefono": "3111234567"}
    contact_id = service.create_contact(c1)

    update_params = {
        "nombre": "Ana Gomez Smith",
        "telefono": "3117777777",
        "categoria": "Familia"
    }
    
    updated = service.update_contact(contact_id, update_params)
    assert updated is True

    contact = service.get_by_id(contact_id)
    assert contact[1] == "ana gomez smith"
    assert contact[2] == "3117777777"
    assert contact[4] == "familia"


def test_delete_contact(service):
    c1 = {"nombre": "Ana Gomez", "telefono": "3111234567"}
    contact_id = service.create_contact(c1)

    deleted = service.delete_contact(contact_id)
    assert deleted is True

    contact = service.get_by_id(contact_id)
    assert contact is None
