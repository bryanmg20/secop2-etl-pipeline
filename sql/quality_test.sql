
#Pruebas de calidad
-- Contratos con id_entity que no existe en entity
SELECT COUNT(*) FROM secop2ce.contract c
LEFT JOIN secop2ce.entity e ON c.id_entity = e.id_entity
WHERE c.id_entity IS NOT NULL AND e.id_entity IS NULL;

-- Contratos con id_provider que no existe en provider
SELECT COUNT(*) FROM secop2ce.contract c
LEFT JOIN secop2ce.provider p ON c.id_provider = p.id_provider
WHERE c.id_provider IS NOT NULL AND p.id_provider IS NULL;

-- Contratos con fechas que no existen en dim_date
SELECT COUNT(*) FROM secop2ce.contract c
LEFT JOIN secop2ce.dim_date d ON c.id_signing_date = d.id_date
WHERE c.id_signing_date IS NOT NULL AND d.id_date IS NULL;

-- duplicados
SELECT id_contract, COUNT(*) FROM secop2ce.contract
GROUP BY id_contract HAVING COUNT(*) > 1;

SELECT id_entity, COUNT(*) FROM secop2ce.entity
GROUP BY id_entity HAVING COUNT(*) > 1;


SELECT
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE id_entity IS NULL) as null_entity,
    COUNT(*) FILTER (WHERE id_provider IS NULL) as null_provider,
    COUNT(*) FILTER (WHERE id_signing_date IS NULL) as null_signing_date,
    COUNT(*) FILTER (WHERE contract_value IS NULL) as null_value
FROM secop2ce.contract;


-- Valores negativos en campos monetarios
SELECT COUNT(*) FROM secop2ce.contract
WHERE contract_value < 0 
OR paid_value < 0 
OR pending_payment_value < 0;

-- Fechas fuera del rango esperado
SELECT COUNT(*) FROM secop2ce.dim_date
WHERE year < 2000 OR year > 2050;


-- Valor pagado mayor que valor del contrato
SELECT COUNT(*) FROM secop2ce.contract
WHERE paid_value > contract_value;

-- Contratos liquidados sin fecha de liquidación
SELECT COUNT(*) FROM secop2ce.contract
WHERE liquidation = TRUE 
AND id_liquidation_start_date IS NULL;

-- Contratos con fechas de fin antes de la fecha de inicio
SELECT COUNT(*) FROM secop2ce.contract
WHERE id_contract_start_date > id_contract_end_date

-- Contratos con fecha de inicio antes de la fecha de firma
SELECT COUNT(*) FROM secop2ce.contract
WHERE id_contract_start_date < id_signing_date;

-- Porcentaje denulos de fechas
with total_null_dates as (
    SELECT 
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE id_signing_date IS NULL) as null_signing_date,
        COUNT(*) FILTER (WHERE id_contract_start_date IS NULL) as null_contract_start_date,
        COUNT(*) FILTER (WHERE id_contract_end_date IS NULL) as null_contract_end_date,
        COUNT(*) FILTER (WHERE id_liquidation_start_date IS NULL) as null_liquidation_start_date,
        COUNT(*) FILTER (WHERE id_liquidation_end_date IS NULL) as null_liquidation_end_date
    FROM secop2ce.contract
)
SELECT 
    total,
    null_signing_date,
    null_contract_start_date,
    null_contract_end_date,
    null_liquidation_start_date,
    null_liquidation_end_date,
    (null_signing_date::float / total) * 100 as pct_null_signing_date,
    (null_contract_start_date::float / total) * 100 as pct_null_contract_start_date,
    (null_contract_end_date::float / total) * 100 as pct_null_contract_end_date,
    (null_liquidation_start_date::float / total) * 100 as pct_null_liquidation_start_date,
    (null_liquidation_end_date::float / total) * 100 as pct_null_liquidation_end_date
    FROM total_null_dates;

