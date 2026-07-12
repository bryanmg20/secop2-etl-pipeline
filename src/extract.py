import os
from dotenv import load_dotenv
import pandas as pd
import requests
import time

from src.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

api_secopii = os.getenv("API_SECOPII")
app_token = os.getenv("SOCRATA_APP_TOKEN")  # opcional pero recomendado


def extract_data(last_row_id=None) -> pd.DataFrame:
    """Extract data from the SECOP II API using keyset pagination on :id.

    Args:
        last_row_id: valor de la columna de sistema :id del último registro
            procesado (None en la primera llamada).

    Returns:
        pd.DataFrame: los datos extraídos, o False si no hay más datos.
    """
    limit = 5000

    columns = [
        # location
        'departamento', 'ciudad',

        # entity
        'codigo_entidad', 'nit_entidad', 'nombre_entidad', 'orden', 'sector', 'rama',

        # contract
        'id_contrato', 'estado_contrato', 'tipo_de_contrato', 'liquidaci_n', 'obligaci_n_ambiental',
        'espostconflicto', 'valor_del_contrato', 'valor_pendiente_de_pago', 'valor_pagado', 'entidad_centralizada',
        'modalidad_de_contratacion', 'origen_de_los_recursos', 'destino_gasto', 'habilita_pago_adelantado',
        'obligaciones_postconsumo', 'reversion', 'valor_de_pago_adelantado', 'valor_facturado', 'valor_amortizado',
        'valor_pendiente_de', 'valor_pendiente_de_ejecucion', 'dias_adicionados', 'duraci_n_del_contrato',
        'el_contrato_puede_ser_prorrogado',

        # provider
        'codigo_proveedor', 'tipodocproveedor', 'documento_proveedor', 'proveedor_adjudicado', 'es_pyme', 'es_grupo',

        # dates
        'fecha_de_firma', 'fecha_de_inicio_del_contrato', 'fecha_de_fin_del_contrato',
        'fecha_inicio_liquidacion', 'fecha_fin_liquidacion', 'ultima_actualizacion',
    ]

    select_columns = [':id'] + columns  # pedimos también la columna de sistema

    where_clause = "fecha_de_firma IS NOT NULL"  # ejemplo de filtro, puedes ajustarlo según tus necesidades
    if last_row_id is not None:
        where_clause += f" AND :id > '{last_row_id}'"

    params = {
        '$select': ','.join(select_columns),
        '$where': where_clause,
        '$order': ':id ASC',
        '$limit': limit,
    }

    headers = {'X-App-Token': app_token} if app_token else {}

    try:
        logger.info(f"Starting data extraction after :id = {last_row_id}...")
        response = requests.get(api_secopii, params=params, headers=headers, timeout=(60, 120))
    
        if response.status_code == 200:
            data = response.json()
            if not data:
                logger.info("No more data to fetch.")
                return False

            df_data = pd.DataFrame(data)
            df_data = df_data.reindex(columns=select_columns)  # incluye ':id' + columnas originales

            logger.info(f"Fetched {len(df_data)} records...")
            return df_data

        elif response.status_code == 503:
            logger.warning("Service unavailable. Retrying...")
            time.sleep(5)
            return extract_data(last_row_id)

        elif response.status_code == 429:
            logger.warning("Rate limit exceeded. Retrying...")
            time.sleep(10)
            return extract_data(last_row_id)

        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return False

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        logger.error(f"Request failed: {e}. Retrying...")
        time.sleep(10)
        return extract_data(last_row_id)