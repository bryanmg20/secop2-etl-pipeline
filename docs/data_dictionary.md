# Data Dictionary

## Tabla de la ubicacion
### `location`

##Tabla de Ubicacion

#location 

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_location | INTEGER PRIMARY KEY | Es el identificador unico de la ubicacion departamento/ciudad|
| department | VARCHAR | Departamento de colombia |
| city | VARCHAR | Municipio de un departamento |

## Tabla de Entidad
### `entity`

Contiene la información de las entidades públicas contratantes.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_entity | BIGINT PRIMARY KEY | Identificador único de la entidad contratante. |
| nit_entity | BIGINT | Número de Identificación Tributaria (NIT) de la entidad. |
| id_location | INTEGER (FK) | Referencia a la ubicación (departamento y municipio) de la entidad. |
| name_entity | VARCHAR(200) | Nombre de la entidad contratante. |
| order_entity | VARCHAR(100) | Orden administrativo de la entidad (Nacional, Territorial, etc.). |
| sector_entity | VARCHAR(100) | Sector al que pertenece la entidad. |
| branch_entity | VARCHAR(100) | Rama del poder público a la que pertenece la entidad. |

---

## Tabla de Fechas

### `dim_date`

Dimensión de fechas utilizada para el análisis temporal de los contratos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_date | INTEGER PRIMARY KEY | Identificador único de la fecha. |
| date | DATE | Fecha completa. |
| year | INTEGER | Año correspondiente a la fecha. |
| month | INTEGER | Número del mes (1–12). |
| month_name | VARCHAR(20) | Nombre del mes. |
| quarter | INTEGER | Trimestre del año (1–4). |
| day_of_week | INTEGER | Número del día de la semana. |
| week | INTEGER | Número de la semana del año. |
| is_weekend | BOOLEAN | Indica si la fecha corresponde a un fin de semana. |
| day | INTEGER | Día del mes. |
| day_name | VARCHAR(20) | Nombre del día de la semana. |

---

## Tabla de Proveedores

### `provider`

Contiene la información de los proveedores asociados a los contratos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_provider | INTEGER PRIMARY KEY | Identificador único del proveedor. |
| type_of_provider | VARCHAR(100) | Tipo de proveedor registrado en SECOP II. |
| provider_document | VARCHAR(100) | Número del documento de identificación del proveedor. |
| name_provider | VARCHAR(200) | Nombre o razón social del proveedor. |
| is_pyme | BOOLEAN | Indica si el proveedor está clasificado como PYME. |

---

## Tabla de Contratos

### `contract`

Tabla de hechos que almacena la información principal de cada contrato.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_contract | VARCHAR(100) PRIMARY KEY | Identificador único del contrato. |
| id_entity | INTEGER (FK) | Referencia a la entidad contratante. |
| id_provider | INTEGER (FK) | Referencia al proveedor contratado. |
| id_contract_start_date | INTEGER (FK) | Referencia a la fecha de inicio del contrato. |
| id_contract_end_date | INTEGER (FK) | Referencia a la fecha de finalización del contrato. |
| id_liquidation_start_date | INTEGER (FK) | Referencia a la fecha de inicio de la liquidación del contrato. |
| id_liquidation_end_date | INTEGER (FK) | Referencia a la fecha de finalización de la liquidación del contrato. |
| id_signing_date | INTEGER (FK) | Referencia a la fecha de firma del contrato. |
| contract_state | VARCHAR(100) | Estado actual del contrato. |
| contract_type | VARCHAR(100) | Tipo de contrato. |
| liquidation | BOOLEAN | Indica si el contrato fue liquidado. |
| environmental_obligation | BOOLEAN | Indica si el contrato contempla obligaciones ambientales. |
| is_post_conflict | BOOLEAN | Indica si el contrato está relacionado con programas de posconflicto. |
| contract_value | DECIMAL(20,2) | Valor total del contrato. |
| pending_payment_amount | DECIMAL(20,2) | Valor pendiente de pago. |
| paid_amount | DECIMAL(20,2) | Valor pagado del contrato. |
