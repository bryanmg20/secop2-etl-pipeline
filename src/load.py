import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from src.logger import get_logger


logger = get_logger(__name__)
load_dotenv()


def get_engine() -> create_engine:
    """Create a SQLAlchemy engine for connecting to the PostgreSQL database.
    Returns:
        create_engine: The SQLAlchemy engine.
    """
    try:
        url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(url)
        with engine.connect() as conn:  # this ensures that the connection is established and can be used to execute queries
            conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully.")
        return engine
    except Exception as e:
        logger.critical(f"Failed to connect to the database: {e}")
        raise

def create_schema(engine) -> None:
    """Create the database schema if it doesn't exist.
    Args:
        engine (create_engine): The SQLAlchemy engine.
    Returns:
        None
    """
    try:
        with open("sql/schema.sql", "r") as f:
            schema = f.read()
        with engine.connect() as conn:
            conn.execute(text(schema))
            conn.commit()
        logger.info("Schema created successfully")
    except Exception as e:
        logger.critical(f"Failed to create schema: {e}")
        raise

def load(tables) -> None:
    """Load the transformed data into the PostgreSQL database.
    Args:
        tables (dict): A dictionary containing the transformed data for each dimension.
    Returns:
        None
    """
    engine = get_engine()
    create_schema(engine)
    
    # orden importante: primero las que no tienen FK
    try:
        tables['date'].to_sql('dim_date', engine, if_exists='append', index=False)
        tables['location'].to_sql('location', engine, if_exists='append', index=False)
        tables['provider'].to_sql('provider', engine, if_exists='append', index=False)
        tables['entity'].to_sql('entity', engine, if_exists='append', index=False)
        tables['contract'].to_sql('contract', engine, if_exists='append', index=False)
    except Exception as e:
        logger.critical(f"Failed to load data into the database: {e}")
        raise
    
    logger.info("Data uploaded successfully to PostgreSQL database.")