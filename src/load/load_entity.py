from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_entity(entity, conn: Connection, schema: str) -> None:
    """Load entity records into the database using an upsert.

    Args:
        entity: DataFrame containing the entity data.
        conn: SQLAlchemy connection (expected to be within a transaction,
            e.g. obtained via `engine.begin()`).
        schema: Target database schema.

    Returns:
        None
    """

    query = text(f"""
    INSERT INTO {schema}.entity (
        id_entity,
        nit_entity,
        id_location,
        name_entity,
        order_entity,
        sector_entity,
        branch_entity,
        centralized_entity
    )
    VALUES (
        :id_entity,
        :nit_entity,
        :id_location,
        :name_entity,
        :order_entity,
        :sector_entity,
        :branch_entity,
        :centralized_entity
    )
    ON CONFLICT (id_entity)
    DO UPDATE SET
        nit_entity = EXCLUDED.nit_entity,
        id_location = EXCLUDED.id_location,
        name_entity = EXCLUDED.name_entity,
        order_entity = EXCLUDED.order_entity,
        sector_entity = EXCLUDED.sector_entity,
        branch_entity = EXCLUDED.branch_entity,
        centralized_entity = EXCLUDED.centralized_entity;
    """)

    columns = [
        "id_entity",
        "nit_entity",
        "id_location",
        "name_entity",
        "order_entity",
        "sector_entity",
        "branch_entity",
        "centralized_entity",
    ]

    values = entity[columns].to_dict(orient="records")

    conn.execute(query, values)