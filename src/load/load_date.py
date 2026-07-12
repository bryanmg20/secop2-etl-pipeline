from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_date(date, conn: Connection, schema: str) -> None:
    """Load date dimension records into the database.

    Args:
        date: DataFrame containing the date dimension data.
        conn: SQLAlchemy connection (expected to be within a transaction,
            e.g. obtained via `engine.begin()`).
        schema: Target database schema.

    Returns:
        None
    """

    query = text(f"""
    INSERT INTO {schema}.dim_date (
        id_date,
        date,
        year,
        month,
        month_name,
        quarter,
        day_of_week,
        week,
        is_weekend,
        day,
        day_name
    )
    VALUES (
        :id_date,
        :date,
        :year,
        :month,
        :month_name,
        :quarter,
        :day_of_week,
        :week,
        :is_weekend,
        :day,
        :day_name
    )
    ON CONFLICT (id_date)
    DO NOTHING;
    """)

    columns = [
        "id_date",
        "date",
        "year",
        "month",
        "month_name",
        "quarter",
        "day_of_week",
        "week",
        "is_weekend",
        "day",
        "day_name",
    ]

    values = date[columns].to_dict(orient="records")

    conn.execute(query, values)