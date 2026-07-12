from . import utils
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform_entity_data(df: pd.DataFrame, conn, schema) -> pd.DataFrame:
    """Transform the entity data into a structured format suitable for loading into the database.
    Args:
        df (pd.DataFrame): The extracted data."""
    
    #transform entity data
    entity = df[['departamento','ciudad','codigo_entidad','nombre_entidad','nit_entidad','orden','sector','rama','entidad_centralizada']].copy()

    columns_to_clean = ['nombre_entidad', 'sector', 'rama','orden','departamento','ciudad']

    for col in columns_to_clean:
        entity[col] = utils.clean_text(entity[col])

    entity.rename(columns={ 'departamento': 'department', 'ciudad': 'city', 'codigo_entidad': 'id_entity',
                           'nombre_entidad': 'name_entity', 'nit_entidad': 'nit_entity', 'orden': 'order_entity',
                           'rama': 'branch_entity', 'sector': 'sector_entity', 'entidad_centralizada': 'centralized_entity' }, inplace=True)


    entity.drop_duplicates(inplace=True)

    query = """
    SELECT id_location, department, city FROM {schema}.location
    """.format(schema=schema)

    location_df = pd.read_sql_query(query, conn)

    entity = entity.merge(location_df, on=['department', 'city'], how='left')

    entity.drop(columns=['city','department'], inplace=True)

    entity['centralized_entity'] = entity['centralized_entity'].map({'Centralizada': True, 'Descentralizada': False})

    logger.info(f"Entity data transformed: {len(entity)} unique records created.")

    return entity