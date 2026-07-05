# Gestor de Contactos CLI (Clean Architecture)

Este proyecto es una aplicación interactiva de consola para gestionar una agenda de contactos, diseñada bajo principios de arquitectura limpia y desacoplamiento de responsabilidades en Python. Utiliza SQLite como base de datos local y demuestra el uso de patrones de diseño, decoradores de telemetría y pruebas automatizadas.

## Diseño de Arquitectura

El proyecto está estructurado para separar estrictamente la lógica de entrada/salida (UI), las reglas de negocio (Services) y el almacenamiento físico de datos (Repositories).

```text
    ┌────────────────────────────────────────────────────────┐
    │                       Capa de UI                       │
    │  - menu.py: Orquestador del flujo CLI                  │
    │  - views.py: Renderizado y salida de consola           │
    │  - prompts.py: Captura de entrada del usuario          │
    └───────────────────────────┬────────────────────────────┘
                                │
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │                   Capa de Servicios                    │
    │  - contact_service.py: Validaciones complejas,         │
    │    normalización de datos y lógica de negocio          │
    │  - validators.py: Reglas de validación estáticas       │
    └───────────────────────────┬────────────────────────────┘
                                │
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │                  Capa de Repositorio                   │
    │  - contact_repository.py: Abstracción de acceso a SQL  │
    └───────────────────────────┬────────────────────────────┘
                                │
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │                      Base de Datos                     │
    │  - session.py: Context Manager para SQLite             │
    │  - schema.py: Inicialización de tablas y DDL           │
    └────────────────────────────────────────────────────────┘
```

## Características Técnicas

- **Repository Pattern**: Desacopla la lógica de base de datos de la lógica de negocio, facilitando el intercambio de motores de almacenamiento (ej. migrar de SQLite a PostgreSQL) en el futuro.
- **Context Management**: Implementa el protocolo `__enter__` y `__exit__` de Python en `SQLiteSession` para garantizar el cierre seguro de conexiones y control transaccional automático (`commit`/`rollback`).
- **Decoradores (AOP - Aspect Oriented Programming)**: Utiliza un decorador personalizado `@measure_time` en `decorators/timing.py` para medir el tiempo de respuesta de los métodos críticos del servicio y reportarlo en tiempo de ejecución.
- **Validaciones Rigurosas**: Validación de formato de teléfono (7-10 dígitos), estructura de correo electrónico y normalización de textos.

## Estructura del Código

- `run.py`: Script de conveniencia para ejecutar la aplicación CLI sin alterar el PYTHONPATH.
- `src/agenda_contactos/config.py`: Parámetros de configuración física (rutas de bases de datos).
- `src/agenda_contactos/main.py`: Punto de entrada de la aplicación.
- `src/agenda_contactos/db/`: Manejo de conexiones y tablas SQLite.
- `src/agenda_contactos/decorators/`: Decoradores transversales de performance.
- `src/agenda_contactos/repositories/`: Consultas SQL encapsuladas por entidad.
- `src/agenda_contactos/services/`: Lógica de validación, normalización e integración.
- `src/agenda_contactos/ui/`: Captura e impresión de datos por consola.
- `tests/`: Suite de pruebas unitarias automatizadas con pytest.

## Instrucciones de Uso

### 1. Ejecutar la Aplicación CLI
Inicia el gestor interactivo en tu terminal ejecutando:
```bash
python run.py
```
*La base de datos SQLite se creará y se inicializará automáticamente en una carpeta `data/` en la raíz del proyecto.*

### 2. Ejecutar Pruebas Unitarias
Para correr la suite de pruebas unitarias que cubren los servicios, validadores e integración con la base de datos de prueba:
```bash
pytest tests/
```
