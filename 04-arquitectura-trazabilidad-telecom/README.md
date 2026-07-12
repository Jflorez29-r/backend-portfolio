# Caso de Estudio: Sistema de Trazabilidad Operativa y Financiera (SITOC)

Este proyecto describe la arquitectura y diseño técnico de **SITOC**, un sistema de grado empresarial desarrollado para la industria de las telecomunicaciones. Su propósito es conectar el progreso físico de obras en campo con el ciclo de facturación y cobro, previniendo pérdidas de ingresos (lucro cesante) y automatizando flujos de trabajo complejos de facturación.

*Nota: Por motivos de confidencialidad (NDA), el código fuente comercial de las reglas de negocio y los datos del cliente son privados. Este repositorio expone el caso de estudio técnico y el boilerplate arquitectónico utilizado para el desarrollo.*

---

## 🏗️ 1. Desafío de Negocio e Ingeniería

En la gestión de proyectos de telecomunicaciones (como la instalación de infraestructura de red), los coordinadores de campo registran el avance físico en planillas manuales (generalmente Excel), mientras que el equipo de facturación opera de forma aislada. Esto causa:
1. **Retrasos en cobros:** Hitos finalizados en campo que tardan semanas en ser reportados al área financiera.
2. **Complejidad de facturación:** Reglas de negocio complejas de cobros parciales (ej. cobros divididos 80% / 20% al completar la instalación y la aprobación técnica o ATP).
3. **Falta de visibilidad:** Imposibilidad de calcular márgenes reales por sitio de forma consolidada en tiempo real.

---

## 🎨 2. Arquitectura de Sistema Desacoplada y Modular

Para resolver este desafío de manera mantenible, se propuso una arquitectura **Full-Stack desacoplada** organizada en **módulos autocontenidos (Domain-Driven Design)**.

```text
📁 C:\JUNIOR\Antigravity\
├── backend\                 <-- API REST construida con Laravel 13 (PHP 8.5)
│   ├── app\
│   │   ├── Modules\         <-- Estructura modular por dominio de negocio
│   │   │   ├── Auth\        <-- Registro, Login, RBAC Middleware y Tokens (Sanctum)
│   │   │   ├── Projects\    <-- Proyectos, Sitios y Regiones
│   │   │   ├── Operations\  <-- Actividades (Survey, Instalación, ATP)
│   │   │   └── Finance\     <-- Precios, Items de Cobro y Cierres Mensuales (PDF)
│   │   └── Providers\
│   │       └── ModuleServiceProvider.php  <-- Autocargador dinámico de rutas de módulos
│   └── database\migrations\
└── frontend\                <-- Single Page Application (React 19 + Vite + Tailwind CSS v4)
    ├── src\
    │   ├── components\      <-- Componentes UI reutilizables (Estilo Acero Industrial)
    │   ├── services\        <-- API Client (Axios)
    │   └── views\           <-- Vistas (Dashboard, Sitios, Facturación, Alertas)
```

En lugar de esparcir la lógica en directorios globales horizontales, cada módulo en `app/Modules` encapsula sus propios **Models**, **Controllers**, **Resources**, **Routes** y **Observers**, manteniendo una alta cohesión y bajo acoplamiento.

---

## ⚙️ 3. Reglas de Negocio Implementadas

El sistema implementa de forma automática las siguientes reglas financieras según el estado físico de la obra:

1. **Autogeneración de Actividades:** Al registrar un nuevo sitio físico de entrega, el sistema instancia exactamente 4 actividades base: *Site Survey*, *Installation Complete*, *Dismantle* y *ATP*.
2. **Esquema de Cobro 80/20:**
   - Al marcar **Installation Complete** como completada (`closed`), el sistema genera automáticamente un ítem de cobro por el **80%** del valor contratado.
   - El **20%** restante queda bloqueado hasta que la actividad de **ATP** se marque en estado `closed`.
3. **Notificación de Alerta de Lucro Cesante (Mora):**
   - Si un concepto facturable pasa a estar en estado `"Listo para Cobro"` y transcurren **más de 15 días corridos** sin que se registre un número de factura legal, el sistema activa automáticamente una alarma visual roja en el panel financiero de la coordinadora de facturación.
4. **Segregación de Funciones (RBAC):**
   - **Coordinador de Campo:** Solo gestiona fechas, comentarios y progreso físico de las actividades. No tiene acceso a tarifas ni estados de cobro.
   - **Coordinadora de Facturación:** Gestiona tarifas de venta, porcentajes de costos de contratistas y facturación.
   - **Gerencia:** Acceso exclusivo a dashboards analíticos de márgenes financieros reales (`Ingreso Huawei - Costo Contratista`).

---

## 🛠️ 4. Estructura de Archivos del Boilerplate Adjuntos

Para demostrar las capacidades de implementación de este stack técnico, se incluyen los siguientes archivos de configuración del proyecto real:

1. **[`ModuleServiceProvider.php`](./src/ModuleServiceProvider.php):** Proveedor de Laravel personalizado que escanea dinámicamente la carpeta `app/Modules` y registra las rutas de API con prefijo de versión de forma autónoma.
2. **[`Dockerfile`](./src/Dockerfile):** Archivo de configuración Docker multilenguaje que instala extensiones críticas de PHP para bases de datos PostgreSQL (`pdo_pgsql`) y optimización de memoria.
3. **[`docker-entrypoint.sh`](./src/docker-entrypoint.sh):** Script de punto de entrada para producción que automatiza la ejecución de migraciones, enlaces de storage y el cacheado de rutas/configuraciones de Laravel para optimizar el rendimiento del servidor Apache.

---

## 🧪 5. Pruebas y Aseguramiento de Calidad (Testing)

Se diseñó una cobertura completa con **PHPUnit** en el backend para validar:
- La correcta autogeneración de actividades tras crear un sitio.
- La división exacta 80/20 de los importes facturables.
- La activación en base de datos del flag de alarma por mora de 15 días.
