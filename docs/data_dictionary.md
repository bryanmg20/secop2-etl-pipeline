# Data Dictionary — SECOP II Data Warehouse

Schema: `secop2ce`  
Source: [datos.gov.co — SECOP II Contratos Electrónicos](https://www.datos.gov.co/resource/jbjy-vk9h)  
Last updated: 2026-07-11

---

## Table: `location`

Geographic reference table. Contains unique combinations of department and city found across all contracts.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id_location` | SERIAL | NOT NULL | Surrogate primary key, auto-generated |
| `department` | VARCHAR(100) | NOT NULL | Colombian department name (uppercase, no accents) |
| `city` | VARCHAR(100) | NOT NULL | Municipality or city name (uppercase, no accents) |

**Notes:**
- Combination of `department` + `city` is unique (UNIQUE constraint)
- Values normalized to uppercase and stripped of accents during transformation

---

## Table: `entity`

Public entities that issue contracts through SECOP II.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id_entity` | BIGINT | NOT NULL | Surrogate primary key, generated from `codigo_entidad` in source |
| `nit_entity` | BIGINT | NOT NULL | Legal tax identification number (NIT) of the entity |
| `id_location` | INTEGER | NULL | Foreign key to `location` |
| `name_entity` | VARCHAR(200) | NOT NULL | Official name of the entity (uppercase, no accents) |
| `order_entity` | VARCHAR(100) | NULL | Administrative order (e.g. NACIONAL, TERRITORIAL) |
| `sector_entity` | VARCHAR(100) | NULL | Sector the entity belongs to (e.g. SALUD, EDUCACION) |
| `branch_entity` | VARCHAR(100) | NULL | Branch of government (e.g. EJECUTIVO, JUDICIAL) |
| `centralized_entity` | BOOLEAN | NULL | Whether the entity is centralized |

**Notes:**
- The same NIT can correspond to multiple entities (e.g. national institutions with regional offices like SENA)
- `id_entity` is derived from `codigo_entidad` in SECOP II
- `codigo_entidad` was found to be shared across different entities in some cases, likely due to data capture errors in SECOP II

---

## Table: `provider`

Natural persons or legal entities that receive public contracts.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id_provider` | BIGINT | NOT NULL | Surrogate primary key, generated from `codigo_proveedor` in source |
| `type_of_provider` | VARCHAR(100) | NULL | Document type (e.g. NIT, Cédula de Ciudadanía) |
| `provider_document` | VARCHAR(100) | NULL | Document number of the provider |
| `name_provider` | VARCHAR(200) | NULL | Full name of the provider |
| `is_pyme` | BOOLEAN | NULL | Whether the provider is classified as a SME (PYME) |
| `is_group` | BOOLEAN | NULL | Whether the provider is a consortium or temporary union |

**Notes:**
- `is_pyme` and `is_group` were converted from "Si"/"No" text values to boolean

---

## Table: `dim_date`

Date dimension. Contains one row per unique date referenced across all contract date fields.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id_date` | INTEGER | NOT NULL | Primary key in YYYYMMDD format (e.g. 20240115) |
| `date` | DATE | NOT NULL | Full date value |
| `year` | INTEGER | NOT NULL | Calendar year |
| `month` | INTEGER | NOT NULL | Month number (1–12) |
| `month_name` | VARCHAR(20) | NOT NULL | Month name in English (e.g. January) |
| `quarter` | INTEGER | NOT NULL | Quarter (1–4) |
| `week` | INTEGER | NOT NULL | ISO week number (1–53) |
| `day` | INTEGER | NOT NULL | Day of month (1–31) |
| `day_of_week` | INTEGER | NOT NULL | Day of week (0=Monday, 6=Sunday) |
| `day_name` | VARCHAR(20) | NOT NULL | Day name in English (e.g. Monday) |
| `is_weekend` | BOOLEAN | NOT NULL | True if Saturday or Sunday |

**Notes:**

- `id_date` uses YYYYMMDD integer format for readability and efficient joining

---

## Table: `contract`

Fact table. Central table of the star schema. Contains one row per unique electronic contract registered in SECOP II.

### Identifiers

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id_contract` | VARCHAR(100) | NOT NULL | Primary key. Original contract ID from SECOP II (e.g. CO1.PCCNTR.5717120) |
| `id_entity` | BIGINT | NULL | Foreign key to `entity` |
| `id_provider` | BIGINT | NULL | Foreign key to `provider` |

### Date Foreign Keys

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id_contract_start_date` | INTEGER | NULL | FK to `dim_date`. Date the contract execution began |
| `id_contract_end_date` | INTEGER | NULL | FK to `dim_date`. Date the contract execution was expected to end |
| `id_signing_date` | INTEGER | NULL | FK to `dim_date`. Date the contract was formally signed |
| `id_liquidation_start_date` | INTEGER | NULL | FK to `dim_date`. Date the liquidation process started |
| `id_liquidation_end_date` | INTEGER | NULL | FK to `dim_date`. Date the liquidation process ended |
| `id_last_update_date` | INTEGER | NULL | FK to `dim_date`. Date the record was last updated in SECOP II |


### Contract Information

| Column | Type | Nullable | Description |
|---|---|---|---|
| `contract_state` | VARCHAR(100) | NULL | Current state (e.g. En ejecución, Liquidado, Terminado) |
| `contract_type` | VARCHAR(100) | NULL | Type of contract (e.g. Prestación de servicios, Obra) |
| `method_of_contracting` | VARCHAR(100) | NULL | Contracting modality (e.g. Contratación directa, Licitación pública) |
| `source_of_resources` | VARCHAR(200) | NULL | Origin of funding |
| `destination_of_expense` | VARCHAR(200) | NULL | Budget destination category |

### Monetary Values

| Column | Type | Nullable | Description |
|---|---|---|---|
| `contract_value` | NUMERIC(30,2) | NULL | Total value of the contract in Colombian pesos (COP) |
| `paid_value` | NUMERIC(30,2) | NULL | Amount paid to date |
| `advance_payment_value` | NUMERIC(30,2) | NULL | Advance payment amount |
| `pending_payment_value` | NUMERIC(30,2) | NULL | Amount pending payment |
| `invoiced_value` | NUMERIC(30,2) | NULL | Amount invoiced by the provider |
| `amortized_value` | NUMERIC(30,2) | NULL | Amortized advance payment amount |
| `pending_amortization_value` | NUMERIC(30,2) | NULL | Advance payment pending amortization |
| `pending_execution_value` | NUMERIC(30,2) | NULL | Contract value pending execution |

**Monetary notes:**
- All values are in Colombian pesos (COP)
- Some contracts have `contract_value = 0`, possibly corresponding to cooperation agreements or non-monetary contracts
- No negative values were found

### Duration

| Column | Type | Nullable | Description |
|---|---|---|---|
| `additional_days` | INTEGER | NULL | Days added to the original contract duration through modifications |
| `contract_can_be_extended` | BOOLEAN | NULL | Whether the contract allows extension |

**Duration notes:**
- Total contract duration should not be calculated solely from `id_contract_start_date` and `id_contract_end_date` without accounting for `additional_days`, as modifications may have extended the original term

### Boolean Flags

| Column | Type | Nullable | Description |
|---|---|---|---|
| `liquidation` | BOOLEAN | NULL | Whether the contract has been liquidated |
| `environmental_obligation` | BOOLEAN | NULL | Whether the contract has environmental obligations |
| `is_post_conflict` | BOOLEAN | NULL | Whether the contract is associated with Colombia's peace agreement |
| `allows_advance_payment` | BOOLEAN | NULL | Whether advance payment is enabled |
| `post_consumer_obligations` | BOOLEAN | NULL | Whether post-consumer obligations apply |
| `reversion` | BOOLEAN | NULL | Whether a reversion clause exists |

**Boolean notes:**
- All boolean fields were converted from "Si"/"No" text values in the source

---
