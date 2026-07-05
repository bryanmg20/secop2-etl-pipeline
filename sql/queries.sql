
#Que departamentos tienen mas contratos firmados?
WITH 
department_per_entity AS (
SELECT e.id_entity, l.department FROM entity AS e
INNER JOIN location AS l ON l.id_location = e.id_location
)
SELECT l.department, COUNT(1) AS total_contracts FROM department_per_entity AS l
INNER JOIN contract AS c ON l.id_entity = c.id_entity
GROUP BY l.department 
ORDER BY total_contracts DESC


#¿Qué tipo de contrato mueve más dinero?
SELECT contract_type, SUM(contract_value) AS total_value_contracts FROM contract 
GROUP BY contract_type 
ORDER BY total_value_contracts DESC

#¿Qué entidades contratan más?
SELECT e.id_entity, e.name_entity, COUNT(1) AS total_contracts FROM entity AS e
INNER JOIN contract AS c ON e.id_entity = c.id_entity
GROUP BY e.id_entity, e.name_entity
ORDER BY total_contracts DESC

#Cuanto es el periodo de tiempo que acuerdan liquidar los contratos en promedio?
WITH period_liquidation AS (
    SELECT d1.date AS start_liquidation, d2.date AS end_liquidation FROM contract AS c
    INNER JOIN dim_date AS d1 ON c.id_liquidation_start_date = d1.id_date
    INNER JOIN dim_date AS d2 ON c.id_liquidation_end_date = d2.id_date
)
SELECT AVG(end_liquidation - start_liquidation) AS average_liquidation_period FROM period_liquidation

#evolucion entre los dos años:
SELECT 
    d.year,
    COUNT(1) AS total_contracts,
    SUM(c.contract_value) AS total_value
FROM contract c
JOIN dim_date d ON c.id_signing_date = d.id_date
GROUP BY d.year
ORDER BY d.year ASC