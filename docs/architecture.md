# Arquitectura

## Flujo general

(API → ETL → PostgreSQL)

## Componentes

### Extract
Obtiene los contratos desde la API pública del SECOP II.

### Transform
Limpia los datos, normaliza la información y construye el modelo estrella.

### Load
Carga las tablas en PostgreSQL.

## Decisiones de diseño

- ¿Por qué PostgreSQL?

Por su facilida de implementacion, basta con .yml para iniciar a correr la base de datos.

- ¿Por qué un modelo estrella?

Porque permite consultas rapidas, ademas lo util de dividir la tabla de 84 columnas del secop en varias subtablas haciendo mas facil de entender las dimenciones

- ¿Por qué Docker?

Por el momento solo esta en un contenedor la base de datos para garantizar un entorno limpio.