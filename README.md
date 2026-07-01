# secop2-etl-pipeline

Pipeline ETL que extrae contratos públicos de SECOP II (datos.gov.co),
los transforma y carga en PostgreSQL siguiendo un esquema estrella,
con visualización en Power BI.

**Tecnologías:** Python · Pandas · PostgreSQL · SQLAlchemy · Power BI

---

Descubrimientos en exploration.ipynb con contratos con fecha de inicio de contrato entre 2024-2025:

Se comprobó que id_contract es un valor unico y no existen nulos, por lo que es una fuente confiable para identificar cada contrato

Existen fechas absurdas como 2924 en fecha_inicio_del_contrato  y fecha_fin_contrato, estos datos se convirtieron a null en la tabla de contrato.

No existen nulos en las columnas originales de fecha_inicio_del_contrato y fecha_fin_contrato por lo que son confiables para calcular la duracion de los contratos.

Las fechas de liquidacion de inicio a fin son igual o mas del 89% nulas, indicando que la mayoria de contratos no estan liquidados.

Para evitar inconsistencias se cargaran los datos filtrados porque representan la fecha en que el contrato ha sido formalizado legalmente.

Existen contratos con valor_del_contrato igual a 0, posiblemente correspondientes a convenios o contratos sin costo directo. Se conservan en el análisis.