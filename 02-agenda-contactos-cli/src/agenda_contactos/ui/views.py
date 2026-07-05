def show_message(message: str) -> None:
    print(message)


def show_contacts(contactos: list[tuple]) -> None:
    if not contactos:
        print("No hay contactos.")
        return

    print("\nID | Nombre | Telefono | Email | Categoria | Descripcion")
    print("-" * 80)

    for contacto in contactos:
        id_, nombre, telefono, email, categoria, descripcion, _ = contacto
        email = email if email is not None else "N/A"
        descripcion = descripcion if descripcion is not None else "N/A"

        print(f"{id_} | {nombre} | {telefono} | {email} | {categoria} | {descripcion}")
    print("-" * 80)
