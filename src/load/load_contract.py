from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_contract(contract, conn: Connection, schema: str) -> None:
    """Load contract records into the database using an upsert.

    Args:
        contract: DataFrame containing the contract data.
        conn: SQLAlchemy connection (expected to be within a transaction,
            e.g. obtained via `engine.begin()`).
        schema: Target database schema.

    Returns:
        None
    """

    query = text(f"""
    INSERT INTO {schema}.contract (
        -- IDs
        id_contract,
        id_entity,
        id_provider,

        -- Dates
        id_contract_start_date,
        id_contract_end_date,
        id_signing_date,
        id_liquidation_start_date,
        id_liquidation_end_date,
        id_last_update_date,

        -- Contract information
        contract_state,
        method_of_contracting,
        source_of_resources,
        destination_of_expense,
        contract_type,

        -- Monetary values
        contract_value,
        paid_value,
        advance_payment_value,
        pending_payment_value,
        invoiced_value,
        amortized_value,
        pending_amortization_value,
        pending_execution_value,

        -- Duration
        additional_days,
        contract_can_be_extended,

        -- Booleans
        liquidation,
        environmental_obligation,
        is_post_conflict,
        allows_advance_payment,
        post_consumer_obligations,
        reversion
    )
    VALUES (
        :id_contract,
        :id_entity,
        :id_provider,
        :id_contract_start_date,
        :id_contract_end_date,
        :id_signing_date,
        :id_liquidation_start_date,
        :id_liquidation_end_date,
        :id_last_update_date,
        :contract_state,
        :method_of_contracting,
        :source_of_resources,
        :destination_of_expense,
        :contract_type,
        :contract_value,
        :paid_value,
        :advance_payment_value,
        :pending_payment_value,
        :invoiced_value,
        :amortized_value,
        :pending_amortization_value,
        :pending_execution_value,
        :additional_days,
        :contract_can_be_extended,
        :liquidation,
        :environmental_obligation,
        :is_post_conflict,
        :allows_advance_payment,
        :post_consumer_obligations,
        :reversion
    )
    ON CONFLICT (id_contract)
    DO UPDATE SET
        id_entity = EXCLUDED.id_entity,
        id_provider = EXCLUDED.id_provider,
        id_contract_start_date = EXCLUDED.id_contract_start_date,
        id_contract_end_date = EXCLUDED.id_contract_end_date,
        id_signing_date = EXCLUDED.id_signing_date,
        id_liquidation_start_date = EXCLUDED.id_liquidation_start_date,
        id_liquidation_end_date = EXCLUDED.id_liquidation_end_date,
        id_last_update_date = EXCLUDED.id_last_update_date,
        contract_state = EXCLUDED.contract_state,
        method_of_contracting = EXCLUDED.method_of_contracting,
        source_of_resources = EXCLUDED.source_of_resources,
        destination_of_expense = EXCLUDED.destination_of_expense,
        contract_type = EXCLUDED.contract_type,
        contract_value = EXCLUDED.contract_value,
        paid_value = EXCLUDED.paid_value,
        advance_payment_value = EXCLUDED.advance_payment_value,
        pending_payment_value = EXCLUDED.pending_payment_value,
        invoiced_value = EXCLUDED.invoiced_value,
        amortized_value = EXCLUDED.amortized_value,
        pending_amortization_value = EXCLUDED.pending_amortization_value,
        pending_execution_value = EXCLUDED.pending_execution_value,
        additional_days = EXCLUDED.additional_days,
        contract_can_be_extended = EXCLUDED.contract_can_be_extended,
        liquidation = EXCLUDED.liquidation,
        environmental_obligation = EXCLUDED.environmental_obligation,
        is_post_conflict = EXCLUDED.is_post_conflict,
        allows_advance_payment = EXCLUDED.allows_advance_payment,
        post_consumer_obligations = EXCLUDED.post_consumer_obligations,
        reversion = EXCLUDED.reversion;
    """)

    columns = [
        # IDs
        "id_contract",
        "id_entity",
        "id_provider",
        # Dates
        "id_contract_start_date",
        "id_contract_end_date",
        "id_signing_date",
        "id_liquidation_start_date",
        "id_liquidation_end_date",
        "id_last_update_date",
        # Contract information
        "contract_state",
        "method_of_contracting",
        "source_of_resources",
        "destination_of_expense",
        "contract_type",
        # Monetary values
        "contract_value",
        "paid_value",
        "advance_payment_value",
        "pending_payment_value",
        "invoiced_value",
        "amortized_value",
        "pending_amortization_value",
        "pending_execution_value",
        # Duration
        "additional_days",
        "contract_can_be_extended",
        # Booleans
        "liquidation",
        "environmental_obligation",
        "is_post_conflict",
        "allows_advance_payment",
        "post_consumer_obligations",
        "reversion",
    ]

    # SQLAlchemy hace executemany automáticamente al recibir una lista de dicts
    values = contract[columns].to_dict(orient="records")

    conn.execute(query, values)