from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_location(location, conn: Connection, schema: str) -> None:
    """Load location records into the database.

    Args:
        location: DataFrame containing the location data (columns:
            department, city).
        conn: SQLAlchemy connection (expected to be within a transaction,
            e.g. obtained via `engine.begin()`).
        schema: Target database schema.

    Returns:
        None
    """

    query = text(f"""
    INSERT INTO {schema}.location (department, city)
    VALUES (:department, :city)
    ON CONFLICT (department, city)
    DO NOTHING;
    """)

    columns = ["department", "city"]

    values = location[columns].to_dict(orient="records")

    conn.execute(query, values)