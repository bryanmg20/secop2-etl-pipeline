from datetime import timedelta
import json
import pandas as pd
import database
import argparse

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

    # Set up argument parser for mode selection
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["initial", "incremental"],
        required=True
    )
    args = parser.parse_args()
    
    # Establish database connection and create schema if it doesn't exist
    engine = database.get_connection()
    schema = "secop2ce"

    with engine.begin() as conn:
        database.create_schema(conn)


    # Load the last processed row ID from the cursor file
    last_row_id = load_cursor() if args.mode == "initial" else None
        

    try:
        while True:

            if args.mode == "initial":
                where_clause = "fecha_de_firma IS NOT NULL" 
                if last_row_id is not None:
                    where_clause += f" AND :id > '{last_row_id}'"

            elif args.mode == "incremental":

                query = """
                        SELECT MAX(id_last_update_date), MAX(id_signing_date) FROM {schema}.contract
                        """.format(schema=schema)

                with engine.begin() as conn:
                    df = pd.read_sql_query(query, conn)

                last_update = pd.to_datetime(str(df.iloc[0,0]), format="%Y%m%d")
                last_signing = pd.to_datetime(str(df.iloc[0,1]), format="%Y%m%d")

                LOOKBACK_DAYS = 3

                last_update = last_update - timedelta(days=LOOKBACK_DAYS)
                last_signing = last_signing - timedelta(days=LOOKBACK_DAYS)

                last_update = last_update.strftime("%Y-%m-%d")
                last_signing = last_signing.strftime("%Y-%m-%d")


                where_clause = f"(ultima_actualizacion >= '{last_update}' OR fecha_de_firma >= '{last_signing}')"
                if last_row_id is not None:
                    where_clause += f" AND :id > '{last_row_id}'"

            data = extract_data(where_clause)

            if data is None or data.empty:  # No more data to fetch
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

            last_row_id = data.iloc[-1][":id"]

            if args.mode == "initial":
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