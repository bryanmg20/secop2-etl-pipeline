CREATE SCHEMA IF NOT EXISTS secop2ce;


CREATE TABLE IF NOT EXISTS secop2ce.location(
    id_location SERIAL PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    
    UNIQUE(department, city)
);

CREATE TABLE IF NOT EXISTS secop2ce.entity(
    id_entity BIGINT PRIMARY KEY,
    nit_entity BIGINT NOT NULL,
    id_location INTEGER REFERENCES secop2ce.location(id_location),
    name_entity VARCHAR(200) NOT NULL,
    order_entity VARCHAR(100),
    sector_entity VARCHAR(100),
    branch_entity VARCHAR(100),
    centralized_entity BOOLEAN
);

CREATE TABLE IF NOT EXISTS secop2ce.dim_date(
    id_date INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    week INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    day INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS secop2ce.provider(
    id_provider BIGINT PRIMARY KEY,
    type_of_provider VARCHAR(100),
    provider_document VARCHAR(100),
    name_provider VARCHAR(200),
    is_pyme BOOLEAN,
    is_group BOOLEAN
);

CREATE TABLE IF NOT EXISTS secop2ce.contract(
    -- IDs
    id_contract VARCHAR(100) PRIMARY KEY,
    id_entity BIGINT REFERENCES secop2ce.entity(id_entity),
    id_provider BIGINT REFERENCES secop2ce.provider(id_provider),

    -- Dates
    id_contract_start_date INTEGER REFERENCES secop2ce.dim_date(id_date),
    id_contract_end_date INTEGER REFERENCES secop2ce.dim_date(id_date),
    id_signing_date INTEGER REFERENCES secop2ce.dim_date(id_date),
    id_liquidation_start_date INTEGER REFERENCES secop2ce.dim_date(id_date),
    id_liquidation_end_date INTEGER REFERENCES secop2ce.dim_date(id_date),
    id_last_update_date INTEGER REFERENCES secop2ce.dim_date(id_date),

    -- Contract information
    contract_state VARCHAR(100),
    method_of_contracting VARCHAR(100),
    source_of_resources VARCHAR(200),
    destination_of_expense VARCHAR(200),
    contract_type VARCHAR(100),

    -- Monetary values
    contract_value NUMERIC(30, 2),
    paid_value NUMERIC(30, 2),
    advance_payment_value NUMERIC(30, 2),
    pending_payment_value NUMERIC(30, 2),
    invoiced_value NUMERIC(30, 2),
    amortized_value NUMERIC(30, 2),
    pending_amortization_value NUMERIC(30, 2),
    pending_execution_value NUMERIC(30, 2),

    -- Duration
    additional_days INTEGER,
    contract_can_be_extended BOOLEAN,

    -- Booleans
    liquidation BOOLEAN,
    environmental_obligation BOOLEAN,
    is_post_conflict BOOLEAN,
    allows_advance_payment BOOLEAN,
    post_consumer_obligations BOOLEAN,
    reversion BOOLEAN
);