import pandas as pd
from . import utils
import logging

logger = logging.getLogger(__name__)


def transform_location_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the location data into a structured format suitable for loading into the database.
    Args:
        df (pd.DataFrame): The extracted data."""
    
    #transform location data
    location = df[['departamento','ciudad']].copy()

    location['ciudad'] = utils.clean_text(location['ciudad'])
    location['departamento'] = utils.clean_text(location['departamento'])

    location.rename(columns={'ciudad': 'city', 'departamento': 'department'}, inplace=True)

    location.drop_duplicates(inplace=True)
    logger.info(f"Location data transformed: {len(location)} unique records created.")

    return location
