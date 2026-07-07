import pandas as pd
import unicodedata

from logger import get_logger

logger = get_logger(__name__)

def remove_accents(text) -> str:
    """Remove accents from a given string.
    Args:
        text (str): The input string.
    Returns:
        str: The string without accents.
    """
    if isinstance(text, str):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text

def clean_text(series) -> pd.Series:
    """Clean a pandas Series by removing accents, converting to uppercase, and stripping unwanted characters.
    Args:
        series (pd.Series): The input pandas Series.
    Returns:
        pd.Series: The cleaned pandas Series.
    """
    return series.apply(remove_accents).str.upper().str.strip('*/+-.,;:()[] ')


def transform_data(df: pd.DataFrame) -> dict:
    """Transform the extracted data into a structured format suitable for loading into the database.
    Args:
        df (pd.DataFrame): The extracted data.
    Returns:
        dict: A dictionary containing the transformed data for each dimension.
    """
    # Clean text columns
    columns_to_clean = ['ciudad', 'departamento', 'nombre_entidad', 'sector', 'rama', 'orden',
                        'estado_contrato', 'tipo_de_contrato', 'tipodocproveedor', 'proveedor_adjudicado']

    for col in columns_to_clean:
        df[col] = clean_text(df[col])


    #transform location data
    location = df[['ciudad','departamento']]

    location.rename(columns={'ciudad': 'city', 'departamento': 'department'}, inplace=True)

    location.drop_duplicates(inplace=True)
    location.reset_index(drop=True, inplace=True) 

    location['id_location'] = range(1,len(location)+1)

    logger.info(f"Location data transformed: {len(location)} unique records created.")

    #transform entity data
    entity = df[['codigo_entidad','nombre_entidad','nit_entidad','orden','sector','rama', 'ciudad','departamento']]

    entity.rename(columns={'ciudad': 'city', 'departamento': 'department','codigo_entidad':'id_entity',
                           'nombre_entidad':'name_entity','nit_entidad':'nit_entity','orden':'order_entity',
                           'rama':'branch_entity','sector':'sector_entity'}, inplace=True)
    
    
    entity.drop_duplicates(inplace=True)
    entity = entity.merge(location, on=['city','department'], how='left')

    entity.drop(columns=['city','department'], inplace=True)

    logger.info(f"Entity data transformed: {len(entity)} unique records created.")

    #transform provider data
    provider = df[['codigo_proveedor','proveedor_adjudicado','documento_proveedor', 'es_pyme','tipodocproveedor']]

    provider.rename(columns={'codigo_proveedor':'id_provider','proveedor_adjudicado':'name_provider',
                             'documento_proveedor':'provider_document','es_pyme':'is_pyme',
                             'tipodocproveedor':'type_of_provider'}, inplace=True)
    
    provider.drop_duplicates(inplace=True)

    provider['is_pyme'] = provider['is_pyme'].map({'Si': True, 'No': False})

    logger.info(f"Provider data transformed: {len(provider)} unique records created.")

    #transform dates data
    pre_date = pd.concat([df['fecha_de_inicio_del_contrato'], df['fecha_de_fin_del_contrato'], df['fecha_de_firma'], df['fecha_inicio_liquidacion'], df['fecha_fin_liquidacion']])
    
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

    #transform contract data
    contract = df[['id_contrato','codigo_entidad','codigo_proveedor','fecha_de_inicio_del_contrato',
               'fecha_de_fin_del_contrato','fecha_de_firma','fecha_inicio_liquidacion','fecha_fin_liquidacion',
               'estado_contrato','valor_del_contrato','valor_pendiente_de_pago','valor_pagado','tipo_de_contrato',
               'liquidaci_n','obligaci_n_ambiental','espostconflicto']]
    
    contract.rename(columns={'id_contrato':'id_contract','codigo_entidad':'id_entity','codigo_proveedor':'id_provider',
                             'fecha_de_inicio_del_contrato':'id_contract_start_date',
                         'fecha_de_fin_del_contrato':'id_contract_end_date','fecha_de_firma':'id_signing_date',
                         'fecha_inicio_liquidacion':'id_liquidation_start_date','fecha_fin_liquidacion':'id_liquidation_end_date',
                         'estado_contrato':'contract_state','valor_del_contrato':'contract_value',
                         'valor_pendiente_de_pago':'pending_payment_amount','valor_pagado':'paid_amount',
                         'tipo_de_contrato':'contract_type','liquidaci_n':'liquidation','obligaci_n_ambiental':'environmental_obligation',
                         'espostconflicto':'is_post_conflict'}, inplace=True)
    
    contract.drop_duplicates(subset=['id_contract'], inplace=True)

     #transform contract dates to datetime format and then to integer format
    contract['id_contract_start_date'] = pd.to_datetime(contract['id_contract_start_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')
    contract['id_contract_end_date'] = pd.to_datetime(contract['id_contract_end_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')
    contract['id_signing_date'] = pd.to_datetime(contract['id_signing_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')
    contract['id_liquidation_start_date'] = pd.to_datetime(contract['id_liquidation_start_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')
    contract['id_liquidation_end_date'] = pd.to_datetime(contract['id_liquidation_end_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')


    contract['liquidation'] = contract['liquidation'].map({'Si': True, 'No': False})
    contract['environmental_obligation'] = contract['environmental_obligation'].map({'Si': True, 'No': False})
    contract['is_post_conflict'] = contract['is_post_conflict'].map({'Si': True, 'No': False})

    logger.info(f"Contract data transformed: {len(contract)} unique records created.")

    return {
        'location': location,
        'entity': entity,
        'provider': provider,
        'date': date,
        'contract': contract
    }