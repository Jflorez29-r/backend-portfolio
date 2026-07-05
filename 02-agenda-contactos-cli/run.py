import sys
import os

# Agregar el directorio src al PYTHONPATH
base_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(base_dir, "src")))

from agenda_contactos.ui.menu import run_cli

if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario. Saliendo...")
