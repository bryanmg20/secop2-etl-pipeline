
# Calidad de datos

Porcentaje de valores nulos por columna:

Total de filas traidas de la api: 1898936

**Columnas con nulos relevantes:**
- `fecha_inicio_liquidacion`: 87.5% — mayoría de contratos no liquidados
- `fecha_fin_liquidacion`: 87.5% — misma razón
- `fecha_de_inicio_del_contrato`: 0.75% — casos aislados


Hallazgos de calidad de datos: 

Se encontraron contratos duplicados en la fuente (mismo id_contract con 
valores idénticos). Se eliminó el duplicado conservando una sola instancia.

Se encontró fecha de fin del contrato en el año 5025, se dejaron tan cual, aunque con fechas incompatibles con pandas se pasaron a NaT. Correspondientes a que se equivocaron escribiendo o es un contrato indefinido. Es de esperarse encontrarse mas fechas de este estilo.

Hallazgos de fechas de los contratos:
Fecha de inicio del contrato antes que fecha de firma del contrato: 385
Fecha de fin del contrato antes que fecha de inicio del contrato: 533

Es necesario tener en cuenta estas inconsistencias a la hora de hacer calculos con fechas.