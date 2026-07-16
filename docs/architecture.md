# Architecture

This document describes the architectural decisions behind the SECOP II ETL Pipeline and explains how data flows through the system.

---

# General Flow

The pipeline follows a modular ETL architecture where every stage has a single responsibility.

```
SECOP II API
      │
      ▼
  Extract
      │
      ▼
 Transform
      │
      ▼
 Load
      │
      ▼
 PostgreSQL
```

The pipeline extracts public procurement contracts from the SECOP II Electronic Contracts API, transforms the raw data into a dimensional model, and loads it into a PostgreSQL database.

The extraction process is performed in chunks of **5,000 rows**. Each chunk goes through the complete ETL cycle before the next one is requested from the API. This approach keeps memory consumption low while allowing the pipeline to process datasets containing millions of records.

The project is organized using a layered architecture:

- **Extract** is responsible only for retrieving data from the SECOP II API.
- **Transform** cleans, validates and converts the raw data into a Star Schema.
- **Load** inserts the transformed data into PostgreSQL.
- **Database** handles persistence and conflict resolution.

This separation makes every module independent, easier to maintain and easier to test.

---

# Incremental Loading

The pipeline supports two execution modes.

## Initial Load

The initial mode is intended to populate an empty database.

Records are requested sequentially from the API using Socrata's special `:id` column until no more data is available.

## Incremental Load

Once the database already contains data, the incremental mode downloads only contracts that were recently created or updated.

The pipeline retrieves the most recent values of:

- `id_last_update_date`
- `id_signing_date`

from the database and uses them to build the API query.

Before querying the API, a **3-day lookback window** is applied to both dates. This allows the pipeline to capture late updates and prevents records from being missed due to delayed publication.

Pagination is performed using Socrata's internal `:id` field instead of `OFFSET`.

This strategy, commonly known as **keyset pagination**, is recommended by Socrata for large datasets because it provides more stable performance when millions of records are involved.

---

# Database Design

The data warehouse follows a **Star Schema** composed of one fact table and multiple dimension tables.

Dimension tables are loaded before the fact table to guarantee referential integrity.

During loading, conflict resolution depends on the table.

Some dimensions, such as `dim_date`, use:

```sql
ON CONFLICT DO NOTHING
```

because the information never changes once created.

Other tables, such as `entity`, use:

```sql
ON CONFLICT DO UPDATE
```

allowing the pipeline to keep entity information synchronized with SECOP II whenever changes occur.

This strategy prevents duplicated records while ensuring frequently updated entities remain current.

---

# Reliability

The pipeline includes several mechanisms to improve reliability.

## Retry Strategy

Requests that fail due to temporary API errors (429, 500, 503 and 504) are automatically retried using **exponential backoff**.

This reduces the likelihood of failures caused by rate limits or temporary service interruptions.

## Database Transactions

Every loading operation is executed inside a database transaction.

If an unexpected error occurs while loading a chunk, the transaction is rolled back, preventing partial writes and preserving database consistency.

---

# Trade-offs

Like every engineering solution, the current architecture involves trade-offs.

| Decision | Benefit | Limitation |
|----------|---------|------------|
| `ON CONFLICT DO UPDATE` | Keeps entity information synchronized | Corrupted source data could overwrite valid records. |
| Chunk processing | Low memory consumption | Requires additional API requests. |
| Incremental loading | Fast daily updates | Depends on checkpoint logic and update timestamps. |
| GitHub Actions | Free and simple automation | Limited execution time and computing resources. |

At the moment, the pipeline assumes that SECOP II provides trustworthy and consistent data. Future versions may incorporate additional validation rules before updating existing records.