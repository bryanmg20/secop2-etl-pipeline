from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_provider(provider, conn: Connection, schema: str) -> None:
    """Load provider records into the database using an upsert.

    Args:
        provider: DataFrame containing the provider data.
        conn: SQLAlchemy connection (expected to be within a transaction,
            e.g. obtained via `engine.begin()`).
        schema: Target database schema.

    Returns:
        None
    """

    query = text(f"""
    INSERT INTO {schema}.provider (
        id_provider,
        type_of_provider,
        provider_document,
        name_provider,
        is_pyme,
        is_group
    )
    VALUES (
        :id_provider,
        :type_of_provider,
        :provider_document,
        :name_provider,
        :is_pyme,
        :is_group
    )
    ON CONFLICT (id_provider)
    DO UPDATE SET
        type_of_provider = EXCLUDED.type_of_provider,
        provider_document = EXCLUDED.provider_document,
        name_provider = EXCLUDED.name_provider,
        is_pyme = EXCLUDED.is_pyme,
        is_group = EXCLUDED.is_group;
    """)

    columns = [
        "id_provider",
        "type_of_provider",
        "provider_document",
        "name_provider",
        "is_pyme",
        "is_group",
    ]

    values = provider[columns].to_dict(orient="records")

    conn.execute(query, values)