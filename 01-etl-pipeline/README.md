# Pipeline ETL de Limpieza y Validación de Transacciones

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) robusto en Python diseñado para procesar archivos de transacciones comerciales de gran volumen. El pipeline extrae registros, aplica un motor de reglas de validación en 5 campos críticos, normaliza los datos válidos a un formato estándar y segrega los registros incorrectos identificando el motivo exacto del rechazo.

## Arquitectura y Flujo de Datos

El flujo del pipeline se describe a continuación:

```text
    [ datos.csv ]  <-- Archivo de entrada (Muestra o Generado)
          │
          ▼
   [ pipeline.py ]  --> Lee fila por fila usando generadores (Lazy Evaluation)
          │
          ├───► [ validadores.py ] (Motor de reglas)
          │            │
          │            ├── ¿Tiene todos los campos requeridos?
          │            ├── ¿País reconocido?
          │            ├── ¿Categoría soportada?
          │            ├── ¿Formato de monto válido? (Moneda, decimales, etc.)
          │            ├── ¿Cantidad válida?
          │            └── ¿Fecha en formato reconocible?
          │
          │     SI: Pasar a normalización
          │     NO: Escribir en rejects.csv con motivo de error
          │
          ├───► [ transformaciones.py ] (Normalización de datos)
          │            │
          │            ├── Country -> ISO Alpha-2 (ej. Colombia -> CO)
          │            ├── Category -> Estándar minúscula
          │            ├── Amount -> Float limpio (sin símbolos ni letras)
          │            ├── Quantity -> Entero (ej. "dos" -> 2)
          │            └── Transaction Date -> ISO "YYYY-MM-DD"
          │
          ├───► [ clean.csv ] (Resultados limpios)
          └───► [ rejects.csv ] (Registros rechazados con campo 'motivo')
```

## Características Técnicas
- **Eficiencia de Memoria**: Utiliza generadores de Python (`yield`) a través del módulo `explorador.py` para procesar archivos de datos grandes de forma perezosa (streaming de datos), evitando cargar millones de filas en memoria.
- **Tipado Estático**: Implementa Type Hints de Python para mejorar la legibilidad y mantenibilidad del código.
- **Muestreo Inteligente**: Incluye una muestra representativa de 100 registros en `data/datos.csv` para clonado rápido y pruebas inmediatas.
- **Generador de Datos**: Un script complementario para simular millones de transacciones con datos realistas para pruebas de carga.

## Estructura del Código

- `src/pipeline.py`: Orquestador principal del pipeline.
- `src/validadores.py`: Reglas lógicas y verificación de ausencia o malformación de campos.
- `src/transformaciones.py`: Normalizadores de datos para garantizar consistencia.
- `src/explorador.py`: Funciones auxiliares para iterar el CSV de forma eficiente y generar reportes de calidad.
- `data/datos.csv`: Archivo de datos de entrada (muestra inicial).
- `scripts/generate_mock_data.py`: Script para generar datos ficticios masivos.
- `tests/test_pipeline.py`: Cobertura de pruebas unitarias.

## Instrucciones de Uso

### 1. Ejecutar el Pipeline
Para procesar la muestra predeterminada y generar los archivos `clean.csv` y `rejects.csv` en la carpeta `data/`:
```bash
python src/pipeline.py
```

### 2. Generar Datos Masivos (Prueba de Rendimiento)
Puedes generar un dataset de transacciones aleatorias del tamaño que prefieras (por ejemplo, 50,000 registros):
```bash
# Sintaxis: python scripts/generate_mock_data.py [numero_de_filas]
python scripts/generate_mock_data.py 50000
```
Luego ejecuta `python src/pipeline.py` para procesar el nuevo archivo.

### 3. Ejecutar Pruebas Unitarias
Para correr los tests correspondientes a las transformaciones y validaciones con `pytest`:
```bash
pytest tests/
```
