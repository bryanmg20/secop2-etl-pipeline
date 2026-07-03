# secop2-etl-pipeline

Pipeline ETL que extrae contratos públicos de SECOP II (datos.gov.co),
los transforma y carga en PostgreSQL siguiendo un esquema estrella,
con visualización en Power BI.

**Tecnologías:** Python · Pandas · PostgreSQL · SQLAlchemy · Power BI

---

Descubrimientos en exploration.ipynb con contratos con fecha de firma de contrato del 2024:

Para evitar inconsistencias se cargaran los datos filtrados por fecha de firma porque representan la fecha en que el contrato ha sido formalizado legalmente.

Se comprobó que id_contrato es un valor unico y no existen nulos, por lo que es una fuente confiable para identificar cada contrato

Existen fechas absurdas como el año 2924 en fecha_inicio_del_contrato  y fecha_fin_contrato, estos datos se convirtieron a null en la tabla de contrato.

No existen nulos en las columnas originales de fecha_inicio_del_contrato y fecha_fin_contrato, sin embargo al transformar las fechas absurdas con años como 2924 a nulo, ahora no es posible calcular el tiempo de todos los contratos.

Las fechas de liquidacion de inicio a fin son igual o mas del 89% nulas, indicando que la mayoria de contratos no estan liquidados.

Existen contratos con valor_del_contrato igual a 0, posiblemente correspondientes a convenios o contratos sin costo directo. Se conservan en el análisis.

Se encontró un caso en donde dos entidades tienen el mismo nombre, ubicacion, orden sector y rama, aunque difieren del NIT y codigo de la entidad. Se dejaron tal cual porque no hay manera de saber cuál es el real o si ambos pueden logicamente coexistir.

Hallazgos de calidad de datos: 
Se encontraron contratos duplicados en la fuente (mismo id_contract con 
valores idénticos). Se eliminó el duplicado conservando una sola instancia.