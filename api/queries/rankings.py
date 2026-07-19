TOP_PROVIDERS_QUERY = """
SELECT p.id_provider, p.provider_document, p.name_provider, COUNT(c.id_contract) AS contract_count
FROM secop2ce.provider p
INNER JOIN secop2ce.contract c ON p.id_provider = c.id_provider
GROUP BY p.id_provider, p.name_provider
ORDER BY contract_count DESC
LIMIT 100
"""

TOP_ENTITIES_QUERY = """
SELECT e.id_entity, e.nit_entity, e.name_entity, COUNT(c.id_contract) AS contract_count
FROM secop2ce.entity e
INNER JOIN secop2ce.contract c ON e.id_entity = c.id_entity
GROUP BY e.id_entity
ORDER BY contract_count DESC
LIMIT 100
"""

CONTRACTS_BY_DEPARTMENT_QUERY = """
SELECT d.department, COUNT(c.id_contract) AS contract_count, SUM(c.contract_value) AS total_contract_value,
       ROUND(AVG(c.contract_value), 2) AS avg_value, MAX(c.contract_value) AS biggest_contract_value
FROM secop2ce.location d
INNER JOIN secop2ce.entity e ON d.id_location = e.id_location
INNER JOIN secop2ce.contract c ON e.id_entity = c.id_entity
WHERE d.department != 'NO DEFINIDO'
GROUP BY d.department
ORDER BY contract_count DESC
"""

CONTRACTS_BY_YEAR_QUERY = """
SELECT d.year, COUNT(c.id_contract) AS contract_count, SUM(c.contract_value) AS total_contract_value,
       AVG(c.contract_value) AS avg_value, MAX(c.contract_value) AS biggest_contract_value
FROM secop2ce.dim_date d
INNER JOIN secop2ce.contract c ON d.id_date = c.id_signing_date
GROUP BY d.year
ORDER BY d.year DESC
"""