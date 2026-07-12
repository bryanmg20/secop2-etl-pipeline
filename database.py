import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import SQLAlchemyError

from src.logger import get_logger

logger = get_logger(__name__)

load_dotenv()


def get_connection() -> Engine:
    """Create a SQLAlchemy engine for the PostgreSQL database.

    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy engine instance.
    """
    try:
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        engine = create_engine(url)

        # Verifica que la conexión realmente funcione
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        logger.info("Database connection established successfully.")
        return engine

    except SQLAlchemyError as e:
        logger.critical(f"Failed to connect to the database: {e}")
        raise


def create_schema(conn: Connection) -> None:
    """Create the database schema if it doesn't exist.

    Args:
        conn: SQLAlchemy connection (expected to be within an active
            transaction, e.g. obtained via `engine.begin()` from the caller).

    Returns:
        None
    """
    try:
        with open("sql/schema.sql", "r", encoding="utf-8") as f:
            schema = f.read()

        conn.execute(text(schema))

        logger.info("Schema created successfully.")

    except SQLAlchemyError as e:
        logger.critical(f"Failed to create schema: {e}")
        raise