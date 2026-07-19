STATS_QUERY = """
SELECT
    (SELECT COUNT(c.id_contract) FROM secop2ce.contract c) AS total_contracts,
    (SELECT MAX(d.date) FROM secop2ce.contract c INNER JOIN secop2ce.dim_date d ON c.id_signing_date = d.id_date) AS latest_signing_date,
    (SELECT COUNT(e.id_entity) FROM secop2ce.entity e) AS total_entities,
    (SELECT COUNT(p.id_provider) FROM secop2ce.provider p) AS total_providers,
    (SELECT COUNT(DISTINCT d.department) FROM secop2ce.location d WHERE department != 'NO DEFINIDO') AS total_departments,
    (SELECT COUNT(d.city) FROM secop2ce.location d WHERE city != 'NO DEFINIDO') AS total_cities,
    pg_size_pretty(pg_database_size(current_database())) AS db_size
"""