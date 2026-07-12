# Data Quality Report — SECOP II Data Warehouse

Schema: `secop2ce`  
Source: [datos.gov.co — SECOP II Contratos Electrónicos](https://www.datos.gov.co/resource/jbjy-vk9h)  
Last updated: 2026-07-11

---

## Referential Integrity

Verifies that all foreign keys in `contract` point to existing records in their respective dimension tables.

| Test | Result | Status |
|---|---|---|
| Contracts with `id_entity` not found in `entity` | 0 | OK |
| Contracts with `id_provider` not found in `provider` | 0 | OK |
| Contracts with date IDs not found in `dim_date` | 0 | OK |

All foreign keys are valid. No orphan records found.

---

## Uniqueness

Verifies that primary keys contain no duplicate values.

| Test | Result | Status |
|---|---|---|
| Duplicate `id_contract` in `contract` | 0 | OK |
| Duplicate `id_entity` in `entity` | 0 | OK |

---

## Completeness

Percentage of null values in critical columns of the `contract` table.

| Column | Null % | Notes |
|---|---|---|
| `id_signing_date` | 0% | Most reliable date field |
| `id_contract_end_date` | 0.0007% | Negligible |
| `id_contract_start_date` | 1.2% | Acceptable |
| `id_liquidation_start_date` | 88.51% | Expected — most contracts not yet liquidated |
| `id_liquidation_end_date` | 88.51% | Expected — most contracts not yet liquidated |

No nulls were found in `id_entity`, `id_provider`, `id_signing_date` or `contract_value`.

---

## Value Ranges

### Monetary values

| Test | Result | Notes |
|---|---|---|
| Contracts with negative monetary values | 3,290 | Possible credit notes or adjustments in source |
| Contracts where `paid_value` exceeds `contract_value` | 3,388 | Possible contract modifications not reflected in original value |

Negative monetary values and overpayments were not corrected. They are kept as-is from the source and flagged here for awareness. Users should filter these out when performing financial analysis if needed.

### Date ranges

| Test | Result | Notes |
|---|---|---|
| Dates outside year range 2000–2050 in `dim_date` | 116 | Kept as-is from source |

---

## Date Consistency

Verifies logical ordering between contract date fields.

| Test | Result | Notes |
|---|---|---|
| Contracts with end date before start date | 724 | Likely inverted fields during data entry |
| Contracts with start date before signing date | 210,075 | See note below |
| Contracts liquidated with no liquidation start date | 502 | Incomplete records in source |

**Note on start date before signing date (210,075 cases):**  
This is a significant finding. In Colombia it is legally possible for a contract to begin execution before the formal signing date in certain contracting modalities. However the volume of cases (approximately 11% of all contracts) suggests this may also include data entry errors. Users should validate this field against their specific use case before using it in temporal analysis.

**Recommendation:** Exclude contracts with date inconsistencies when calculating contract duration or performing time-based analysis.

---

## Summary

| Category | Status |
|---|---|
| Referential integrity | No issues |
| Uniqueness | No issues |
| Completeness | No critical nulls |
| Monetary ranges | 3,290 negative values, 3,388 overpayments |
| Date ranges | 116 dates outside expected range, kept as-is from source |
| Date consistency | Multiple inconsistencies documented above |

---

## Notes

- All quality tests are available in `sql/quality_tests.sql`
- Data is sourced directly from SECOP II without modification beyond type conversion, deduplication and normalization
- Inconsistencies reflect the state of the source system and are documented here for transparency