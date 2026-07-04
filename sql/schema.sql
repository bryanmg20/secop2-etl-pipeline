DROP TABLE IF EXISTS contract;
DROP TABLE IF EXISTS entity;
DROP TABLE IF EXISTS provider;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS location;

CREATE TABLE location(
    id_location INTEGER PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL
);

CREATE TABLE entity(
    id_entity BIGINT PRIMARY KEY,
    nit_entity BIGINT NOT NULL,
    id_location INTEGER REFERENCES location(id_location),
    name_entity VARCHAR(200) NOT NULL,
    order_entity VARCHAR(100),
    sector_entity VARCHAR(100),
    branch_entity VARCHAR(100)
);

CREATE TABLE dim_date(
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

CREATE TABLE provider(
    id_provider INTEGER PRIMARY KEY,
    type_of_provider VARCHAR(100),
    provider_document VARCHAR(100),
    name_provider VARCHAR(200),
    is_pyme BOOLEAN
);

CREATE TABLE contract(
    id_contract VARCHAR(100) PRIMARY KEY,
    id_entity INTEGER REFERENCES entity(id_entity),
    id_provider INTEGER REFERENCES provider(id_provider),
    id_contract_start_date INTEGER REFERENCES dim_date(id_date),
    id_contract_end_date INTEGER REFERENCES dim_date(id_date),
    id_liquidation_start_date INTEGER REFERENCES dim_date(id_date),
    id_liquidation_end_date INTEGER REFERENCES dim_date(id_date),
    id_signing_date INTEGER REFERENCES dim_date(id_date),
    contract_state VARCHAR(100),
    contract_type VARCHAR(100),
    liquidation BOOLEAN,
    environmental_obligation BOOLEAN,
    is_post_conflict BOOLEAN,
    contract_value DECIMAL(20, 2),
    pending_payment_amount DECIMAL(20, 2),
    paid_amount DECIMAL(20, 2)
);