ENTITY_SEARCH_QUERY = """
SELECT
    e.id_entity,
    e.nit_entity,
    e.name_entity,
    e.order_entity,
    e.sector_entity,
    e.branch_entity,
    e.centralized_entity
FROM secop2ce.entity AS e
WHERE
    e.name_entity ILIKE :search_query OR
    CAST(e.nit_entity AS TEXT) ILIKE :search_query
ORDER BY e.name_entity
LIMIT 10
"""

PROVIDER_SEARCH_QUERY = """
SELECT
    p.id_provider,
    p.type_of_provider,
    p.provider_document,
    p.name_provider,
    p.is_pyme,
    p.is_group
FROM secop2ce.provider AS p
WHERE
    p.name_provider ILIKE :search_query OR
    CAST(p.provider_document AS TEXT) ILIKE :search_query
ORDER BY p.name_provider
LIMIT 10
"""

ENTITY_DETAIL_QUERY = """
SELECT
    e.id_entity,
    e.nit_entity,
    e.name_entity,
    e.order_entity,
    e.sector_entity,
    e.branch_entity,
    e.centralized_entity,
    COUNT(c.id_contract) AS total_contracts,
    SUM(c.paid_value) AS total_value_paid,
    SUM(c.contract_value) AS total_value_contracted,
    (SELECT c2.id_contract FROM secop2ce.contract AS c2 WHERE c2.id_entity = e.id_entity ORDER BY c2.contract_value DESC LIMIT 1) AS id_contract_most_value,
    (SELECT p.provider_document FROM secop2ce.provider AS p INNER JOIN secop2ce.contract AS c3 ON p.id_provider = c3.id_provider WHERE c3.id_entity = e.id_entity GROUP BY p.provider_document ORDER BY COUNT(c3.id_contract) DESC LIMIT 1) AS document_provider_most_contracts,
    (SELECT EXTRACT(YEAR FROM d.date) FROM secop2ce.contract AS c4 INNER JOIN secop2ce.dim_date d ON c4.id_signing_date = d.id_date WHERE c4.id_entity = e.id_entity GROUP BY EXTRACT(YEAR FROM d.date) ORDER BY COUNT(c4.id_contract) DESC LIMIT 1) AS year_most_contracts
FROM secop2ce.entity AS e
LEFT JOIN secop2ce.contract c ON e.id_entity = c.id_entity
WHERE e.id_entity = :id_entity
GROUP BY e.id_entity
"""

ENTITY_CONTRACT_TYPE_DISTRIBUTION_QUERY = """
SELECT
    c.contract_type,
    COUNT(c.id_contract) AS total_contracts,
    SUM(c.contract_value) AS total_value_contracted
FROM secop2ce.contract c
WHERE c.id_entity = :id_entity
GROUP BY c.contract_type
"""

PROVIDER_DETAIL_QUERY = """
SELECT
    p.id_provider,
    p.type_of_provider,
    p.provider_document,
    p.name_provider,
    p.is_pyme,
    p.is_group,
    COUNT(c.id_contract) AS total_contracts,
    SUM(c.paid_value) AS total_value_paid,
    SUM(c.contract_value) AS total_value_contracted,
    (SELECT c2.id_contract FROM secop2ce.contract AS c2 WHERE c2.id_provider = p.id_provider ORDER BY c2.contract_value DESC LIMIT 1) AS id_contract_most_value,
    (SELECT e.nit_entity FROM secop2ce.entity AS e INNER JOIN secop2ce.contract AS c3 ON e.id_entity = c3.id_entity WHERE c3.id_provider = p.id_provider GROUP BY e.nit_entity ORDER BY COUNT(c3.id_contract) DESC LIMIT 1) AS nit_entity_most_contracts,
    (SELECT EXTRACT(YEAR FROM d.date) FROM secop2ce.contract AS c4 INNER JOIN secop2ce.dim_date d ON c4.id_signing_date = d.id_date WHERE c4.id_provider = p.id_provider GROUP BY EXTRACT(YEAR FROM d.date) ORDER BY COUNT(c4.id_contract) DESC LIMIT 1) AS year_most_contracts
FROM secop2ce.provider AS p
LEFT JOIN secop2ce.contract c ON p.id_provider = c.id_provider
WHERE p.id_provider = :id_provider
GROUP BY p.id_provider
"""

PROVIDER_CONTRACT_TYPE_DISTRIBUTION_QUERY = """
SELECT
    c.contract_type,
    COUNT(c.id_contract) AS total_contracts,
    SUM(c.contract_value) AS total_value_contracted
FROM secop2ce.contract c
WHERE c.id_provider = :id_provider
GROUP BY c.contract_type
"""