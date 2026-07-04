# secop2-etl-pipeline

Pipeline ETL que extrae contratos públicos de SECOP II (datos.gov.co),
los transforma y carga en PostgreSQL siguiendo un esquema estrella,
con visualización en Power BI.

**Tecnologías:** Python · Pandas · PostgreSQL · SQLAlchemy · Power BI

---

Descubrimientos en exploration.ipynb con contratos con fecha de firma entre 2024-2025:

Porcentaje de valores nulos por columna:

Total de filas traidas de la api: 1898936

**Columnas con nulos relevantes:**
- `fecha_inicio_liquidacion`: 87.5% — mayoría de contratos no liquidados
- `fecha_fin_liquidacion`: 87.5% — misma razón
- `fecha_de_inicio_del_contrato`: 0.75% — casos aislados

Hallazgos de calidad de datos: 

Se encontraron contratos duplicados en la fuente (mismo id_contract con 
valores idénticos). Se eliminó el duplicado conservando una sola instancia.

Se encontró fecha de fin del contrato en el año 5025, se pasó a null. Supongo que se equivocaron escribiendo o es un contrato indefinido. Es de esperarse encontrarse mas fechas de este estilo.

Hallazgos de fechas de los contratos:
Inicio antes que firma: 385
Fin antes que inicio: 533

Es necesario tener en cuenta estas inconcistencias a la hora de hacer calculos con fechas.