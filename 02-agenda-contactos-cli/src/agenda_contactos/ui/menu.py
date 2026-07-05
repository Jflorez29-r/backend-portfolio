from agenda_contactos.config import DB_PATH
from agenda_contactos.db.schema import init_db
from agenda_contactos.repositories.contact_repository import ContactRepository
from agenda_contactos.services.contact_service import ContactService
from agenda_contactos.ui.prompts import ask_int, ask_text
from agenda_contactos.ui.views import show_contacts, show_message


def _show_menu() -> None:
    show_message("\n=== Agenda de Contactos ===")
    show_message("1. Agregar contacto")
    show_message("2. Listar contactos")
    show_message("3. Listar por categoria")
    show_message("4. Buscar contacto")
    show_message("5. Actualizar contacto")
    show_message("6. Eliminar contacto")
    show_message("7. Salir")


def _translate_error(code: str) -> str:
    messages = {
        "contacto_duplicado": "Teléfono o email ya existen.",
        "nombre_requerido": "El nombre es obligatorio.",
        "telefono_requerido": "El teléfono es obligatorio.",
        "telefono_invalido": "Teléfono inválido (solo dígitos, longitud 7-10).",
        "email_invalido": "Email inválido.",
        "categoria_requerida": "La categoría es obligatoria.",
        "termino_requerido": "Debes ingresar un término de búsqueda.",
        "id_invalido": "El ID debe ser un entero positivo.",
    }
    return messages.get(code, f"Error: {code}")


def run_cli() -> None:
    init_db(DB_PATH)
    repo = ContactRepository(DB_PATH)
    service = ContactService(repo)

    while True:
        _show_menu()
        option = ask_int("Ingrese una opción (1-7): ")

        if option == 1:
            raw = {
                "nombre": ask_text("Nombre: "),
                "telefono": ask_text("Teléfono: "),
                "email": ask_text("Email (opcional): ", allow_empty=True),
                "categoria": ask_text("Categoría (opcional): ", allow_empty=True),
                "descripcion": ask_text("Descripción (opcional): ", allow_empty=True),
            }
            try:
                contact_id = service.create_contact(raw)
                show_message(f"Contacto creado con id {contact_id}")
            except ValueError as e:
                show_message(_translate_error(str(e)))

        elif option == 2:
            contactos = service.list_contacts()
            show_contacts(contactos)

        elif option == 3:
            categoria = ask_text("Categoría: ")
            try:
                contactos = service.list_by_category(categoria)
                show_contacts(contactos)
            except ValueError as e:
                show_message(_translate_error(str(e)))

        elif option == 4:
            termino = ask_text("Buscar (nombre, teléfono, email): ")
            try:
                contactos = service.search_contacts(termino)
                show_contacts(contactos)
            except ValueError as e:
                show_message(_translate_error(str(e)))

        elif option == 5:
            contactos = service.list_contacts()
            show_contacts(contactos)

            contact_id = ask_int("ID del contacto a actualizar: ")
            try:
                current = service.get_by_id(contact_id)
            except ValueError as e:
                show_message(_translate_error(str(e)))
                continue

            if current is None:
                show_message("No existe un contacto con ese ID.")
                continue

            _, nombre_a, telefono_a, email_a, categoria_a, descripcion_a, _ = current
            show_message("Presiona Enter para mantener el valor actual.")

            raw_update = {
                "nombre": ask_text(f"Nombre [{nombre_a}]: ", allow_empty=True),
                "telefono": ask_text(f"Teléfono [{telefono_a}]: ", allow_empty=True),
                "email": ask_text(
                    f"Email [{email_a if email_a else 'N/A'}]: ", allow_empty=True
                ),
                "categoria": ask_text(
                    f"Categoría [{categoria_a}]: ", allow_empty=True
                ),
                "descripcion": ask_text(
                    f"Descripción [{descripcion_a if descripcion_a else 'N/A'}]: ",
                    allow_empty=True,
                ),
            }

            try:
                updated = service.update_contact(contact_id, raw_update)
                if updated:
                    show_message("Contacto actualizado correctamente.")
                else:
                    show_message("No fue posible actualizar el contacto.")
            except ValueError as e:
                show_message(_translate_error(str(e)))

        elif option == 6:
            contactos = service.list_contacts()
            show_contacts(contactos)

            contact_id = ask_int("ID del contacto a eliminar: ")
            confirm = ask_text("Confirmar eliminación (si/no): ").strip().lower()

            if confirm != "si":
                show_message("Eliminación cancelada.")
                continue

            try:
                deleted = service.delete_contact(contact_id)
                if deleted:
                    show_message("Contacto eliminado correctamente.")
                else:
                    show_message("No existe un contacto con ese ID.")
            except ValueError as e:
                show_message(_translate_error(str(e)))

        elif option == 7:
            show_message("Saliendo...")
            break

        else:
            show_message("Opción no válida.")
