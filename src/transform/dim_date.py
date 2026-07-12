import pandas as pd
import logging
from . import utils

logger = logging.getLogger(__name__)

def transform_date_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the date data into a structured format suitable for loading into the database.
    Args:
        df (pd.DataFrame): The extracted data."""
    
    #transform dates data
    pre_date = pd.concat([df['fecha_de_inicio_del_contrato'], df['fecha_de_fin_del_contrato'], 
                          df['fecha_de_firma'], df['fecha_inicio_liquidacion'], 
                          df['fecha_fin_liquidacion'],df['ultima_actualizacion']])
    
    date = pd.DataFrame(pre_date.drop_duplicates().dropna().reset_index(drop=True), columns=['date'])

    #tranform date to datetime format
    date['date'] = pd.to_datetime(date['date'], format='ISO8601', errors='coerce')
    date.dropna(inplace=True)

    #create new columns for year, month, day, quarter, week, day_of_week, day_name, month_name, is_weekend
    date['year'] = date['date'].dt.year.astype('Int64')
    date['month'] = date['date'].dt.month.astype('Int64')
    date['day'] = date['date'].dt.day.astype('Int64')
    date['quarter'] = date['date'].dt.quarter.astype('Int64')
    date['week'] = date['date'].dt.isocalendar().week.astype('Int64')
    date['day_of_week'] = date['date'].dt.dayofweek.astype('Int64')
    date['day_name'] = date['date'].dt.day_name()
    date['month_name'] = date['date'].dt.month_name()
    date['is_weekend'] = date['day_of_week'].isin([5, 6])

    #id_date
    date['id_date'] = date['date'].dt.strftime('%Y%m%d').astype('Int64')

    logger.info(f"Date data transformed: {len(date)} unique records created.")

    return date