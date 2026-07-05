# Backend & Database Development Portfolio

Este repositorio reúne una colección de proyectos prácticos enfocados en el desarrollo backend en Python y el diseño/optimización de bases de datos relacionales (PostgreSQL y SQLite). Está diseñado para demostrar competencias en lógica de programación avanzada, arquitectura de software limpia, control transaccional robusto y automatización de pruebas (CI/CD).

---

## 🛠️ Stack Tecnológico Global
- **Lenguaje**: Python 3.12+ (con fuerte tipado estático `typing`)
- **Bases de Datos**: PostgreSQL, SQLite (SQL nativo DDL/DML)
- **Framework de Pruebas**: Pytest
- **Herramientas de Integración**: psycopg2, GitHub Actions (CI/CD)

---

## 📂 Índice de Proyectos

### [1. Pipeline ETL de Limpieza y Validación de Transacciones (Python)](./01-etl-pipeline/)
Un script de procesamiento de datos optimizado para la eficiencia de memoria a través de generadores (`yield`).
*   **Habilidades Demostradas**: Procesamiento lazy de streams de datos, validación robusta de formatos de datos, tipado estático y normalización.
*   **Valor Freelance**: Ideal para clientes que necesitan migrar o limpiar datos de hojas de cálculo o CSVs a bases de datos relacionales asegurando la calidad de la información.
*   **[Ir al Proyecto ➔](./01-etl-pipeline/)**

### [2. Gestor de Contactos CLI con Arquitectura Limpia (Python & SQLite)](./02-agenda-contactos-cli/)
Una aplicación de consola modular estructurada bajo el patrón de diseño **Repository & Service**, logrando un desacoplamiento del 100% entre la base de datos y la interfaz de usuario.
*   **Habilidades Demostradas**: Repository Pattern, Context Managers en SQLite, Programación Orientada a Aspectos (decoradores de telemetría de rendimiento y logging).
*   **Valor Freelance**: Demuestra capacidad para construir lógica de negocio escalable, estructurada y mantenible, fácil de migrar a interfaces web o APIs en el futuro.
*   **[Ir al Proyecto ➔](./02-agenda-contactos-cli/)**

### [3. Base de Datos de Biblioteca en PostgreSQL (SQL & Python Integration)](./03-biblioteca-db-postgres/)
Diseño lógico y físico de una base de datos relacional orientada al rendimiento, incluyendo indexación estratégica, transacciones seguras (ACID) e integración segura mediante Python.
*   **Habilidades Demostradas**: Modelado relacional, agregaciones y uniones complejas en SQL, tuning de base de datos (`EXPLAIN ANALYZE`), transacciones y manejo seguro de variables de entorno.
*   **Valor Freelance**: Muestra dominio avanzado en bases de datos empresariales, optimización de queries lentas para reducir costos de infraestructura y consistencia de datos críticos.
*   **[Ir al Proyecto ➔](./03-biblioteca-db-postgres/)**

---

## 🚀 Cómo Empezar Localmente

### 1. Clonar el repositorio y crear el entorno virtual
```bash
# Clonar tu repositorio
git clone <tu-repositorio-publico-url>
cd portfolio-entregables

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Linux/macOS:
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🧪 Automatización y Suite de Pruebas (CI/CD)

El portafolio incluye una suite de pruebas unitarias y de integración completa que garantiza el correcto funcionamiento del software en todo momento.

Las pruebas se ejecutan de forma automática en cada `push` o `pull request` a la rama `main` mediante **GitHub Actions** (configurado en `.github/workflows/ci.yml`).

Para correr las pruebas de forma local en tu máquina virtual activa:
```bash
# Ejecuta todos los tests de todos los proyectos de forma simultánea
pytest
```

---

## 📬 Contacto y Redes
Si estás interesado en colaborar conmigo en algún proyecto freelance, desarrollo backend o administración de base de datos, puedes contactarme en:

-   **LinkedIn**: [Tu Nombre](https://www.linkedin.com/in/tu-usuario/)
-   **GitHub**: [@tu-usuario](https://github.com/tu-usuario)
-   **Email**: tu.email@example.com
