import json
import database

from src.extract import extract_data
from src.logger import get_logger

from src.load.load_location import load_location
from src.load.load_entity import load_entity
from src.load.load_provider import load_provider
from src.load.load_date import load_date
from src.load.load_contract import load_contract

from src.transform.location import transform_location_data
from src.transform.entity import transform_entity_data
from src.transform.provider import transform_provider_data
from src.transform.dim_date import transform_date_data
from src.transform.contract import transform_contract_data

logger = get_logger(__name__)


def load_cursor():
    try:
        with open("offset.txt", "r") as f:
            cursor = json.load(f)
            return cursor.get("last_row_id")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def main() -> None:
    """Main function to orchestrate the ETL pipeline."""

    engine = database.get_connection()
    schema = "secop2ce"

    with engine.begin() as conn:
        database.create_schema(conn)

    last_row_id = load_cursor()

    try:
        while True:
            data = extract_data(last_row_id)

            if data is False:  # No more data to fetch
                break

            with engine.begin() as conn:
                transformed_location = transform_location_data(data)
                load_location(transformed_location, conn, schema)

                transformed_entity = transform_entity_data(data, conn=conn, schema=schema)
                load_entity(transformed_entity, conn, schema)

                transformed_provider = transform_provider_data(data)
                load_provider(transformed_provider, conn, schema)

                transformed_date = transform_date_data(data)
                load_date(transformed_date, conn, schema)

                transformed_contract = transform_contract_data(data)
                load_contract(transformed_contract, conn, schema)

            last_row_id = data.iloc[-1][":id"]  # ajusta la clave si es distinta

            with open("offset.txt", "w") as f:
                json.dump({"last_row_id": last_row_id}, f)

    except Exception as e:
        logger.critical(f"Pipeline failed: {e}")
        raise

    finally:
        engine.dispose()
        logger.info("Database connection closed.")


if __name__ == "__main__":
    main()