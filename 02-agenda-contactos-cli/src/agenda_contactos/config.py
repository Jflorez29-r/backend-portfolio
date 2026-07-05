from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# El directorio data se creará un nivel arriba del código fuente para higiene del repositorio
DATA_DIR = BASE_DIR.parent.parent / "data"
DB_PATH = DATA_DIR / "contactos.db"
