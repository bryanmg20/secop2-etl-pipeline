import os
from dotenv import load_dotenv
import pandas as pd
import requests
import time
from typing import Optional

from src.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

secopii_api_url = os.getenv("API_SECOPII")

if not secopii_api_url:
    raise ValueError("API_SECOPII environment variable is required")

app_token = os.getenv("SOCRATA_APP_TOKEN")  # optional but recommended



def extract_data(where_clause=None, max_retries=3) -> Optional[pd.DataFrame]:
    """Extract data from the SECOP II API using keyset pagination on :id.

    Args:
        where_clause: WHERE clause to filter the data.

    Returns:
        pd.DataFrame: the extracted data, or an empty DataFrame if there is no more data.
        None if an error occurs.
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

    select_columns = [':id'] + columns  # include the system column too


    params = {
        '$select': ','.join(select_columns),
        '$where': where_clause,
        '$order': ':id ASC',
        '$limit': limit,
    }

    headers = {'X-App-Token': app_token} if app_token else {}

    delay = 1  # initial delay for exponential backoff
    for attempt in range(max_retries+1):
        try:
            logger.info(f"Starting data extraction with WHERE clause: {where_clause}")
            response = requests.get(secopii_api_url, params=params, headers=headers, timeout=(60, 120))
        
            if response.status_code == 200:
                data = response.json()
                if not data:
                    logger.info("No more data to fetch.")
                    return pd.DataFrame()  # Return an empty DataFrame instead of False

                df_data = pd.DataFrame(data)
                df_data = df_data.reindex(columns=select_columns)  # include ':id' + original columns

                logger.info(f"Fetched {len(df_data)} records...")
                return df_data

            recoverable_errors = [429,500,502,503,504,408]
            if response.status_code in recoverable_errors:
                logger.warning(f"Recoverable error: {response.status_code}. Retrying...")
                delay *= 2  # exponential backoff
                time.sleep(delay)
                continue  # Retry the request

            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                return None

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.error(f"Request failed: {e}. Retrying...")
            delay *= 2  # exponential backoff
            time.sleep(delay)
            continue  # Retry the request
        
    logger.error("Max retries exceeded.")
    return None