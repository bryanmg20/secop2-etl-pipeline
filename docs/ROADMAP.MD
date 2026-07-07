# Roadmap

Este documento presenta la hoja de ruta del proyecto. Para conocer el historial de cambios, consulta el **CHANGELOG.md**.

---

## v1.0 — Initial ETL (done)

Construcción del pipeline ETL inicial para transformar los datos públicos del SECOP II en un modelo dimensional dentro de PostgreSQL.

**Incluye**

* Extracción desde SECOP II
* Transformación de datos
* Modelo estrella
* PostgreSQL
* Docker
* Documentación inicial

---

## v1.1 — (done)

Convertir el pipeline en un proyecto mantenible y preparado para ejecutarse de forma confiable.

**Objetivos**

* Documentación técnica
* Diccionario de datos
* CHANGELOG
* ROADMAP

---

## v2.0 — (developing)

Automatizar completamente la actualización del Data Warehouse.

**Objetivos**

* Apache Airflow
* DAG del pipeline
* Programación automática
* Reintentos automáticos
* Registro de ejecuciones
* Notificación de errores
* Optimización de consultas SQL

---

## v2.1 — Incremental Processing

Actualizar únicamente la información nueva o modificada.

**Objetivos**

* Carga incremental
* Upserts
* Eliminación de duplicados
* Optimización del tiempo de procesamiento

---

## v3.0 — Data Platform

Publicar el Data Warehouse mediante interfaces de consumo estables.

**Objetivos**

### PostgreSQL

* Modelo dimensional documentado
* Índices optimizados
* Consultas eficientes

### REST API

* FastAPI
* Documentación Swagger / OpenAPI
* Endpoints para contratos, entidades, proveedores y estadísticas

---

## v3.1 — Consumer Experience

Facilitar el consumo de los datos desde herramientas de análisis.

**Objetivos**

* Ejemplos para Power BI
* Ejemplos para Python
* Ejemplos para SQL
* Ejemplos para Excel
* Guías de conexión
* Consultas de ejemplo
* Casos de uso

---

## v4.0 — Open Source Readiness

Preparar el proyecto para su crecimiento como iniciativa open source.

**Objetivos**

* LICENSE
* CONTRIBUTING.md
* Plantillas para Issues
* Plantillas para Pull Requests
* GitHub Actions
* Releases
* Versionado

---

## v5.0 — Production Deployment

Desplegar la plataforma para que cualquier persona pueda consumir los datos sin necesidad de ejecutar el ETL localmente.

**Objetivos**

* Base de datos PostgreSQL en la nube
* API desplegada
* Pipeline desplegado
* Airflow en producción
* Variables de entorno
* Backups
* Monitoreo básico
* Documentación de despliegue
