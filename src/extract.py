import os
from dotenv import load_dotenv
import pandas as pd
import requests
import time

from src.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

api_secopii = os.getenv("API_SECOPII")
csv_file = 'data/raw/secop2-2426.csv'
file_exists = os.path.exists(csv_file)

def extract_data() -> pd.DataFrame:
    """Extract data from the SECOP II API and save it to a CSV file.
    Returns:
        pd.DataFrame: The extracted data.
    """
    global file_exists
    limit=5000
    columns = [
    # location
    'departamento', 'ciudad',
    
    # entity
    'codigo_entidad', 'nit_entidad', 'nombre_entidad', 'orden', 'sector', 'rama',

    # contract
    'id_contrato', 'estado_contrato', 'tipo_de_contrato', 'liquidaci_n', 'obligaci_n_ambiental',
    'espostconflicto', 'valor_del_contrato', 'valor_pendiente_de_pago', 'valor_pagado',
    
    # provider
    'codigo_proveedor', 'tipodocproveedor', 'documento_proveedor', 'proveedor_adjudicado', 'es_pyme',
    
    # dates
    'fecha_de_firma', 'fecha_de_inicio_del_contrato', 'fecha_de_fin_del_contrato',
    'fecha_inicio_liquidacion', 'fecha_fin_liquidacion'
    ]


    try:
        df = pd.read_csv(csv_file) if file_exists else pd.DataFrame()
        if file_exists:
            logger.info(f"Csv file found with {len(df)} records...")
        offset = len(df)

    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        offset = 0
        
    while True:
        try:
            logger.info(f"Starting data extraction from offset {offset}...")
            response = requests.get(api_secopii, 
                                    params={'$select': ','.join(columns),
                                            '$where': "fecha_de_firma >= '2024-01-01' and fecha_de_firma < '2026-01-01'",
                                            '$order': 'fecha_de_firma ASC',
                                            '$limit': limit, 
                                            '$offset': offset,
                                            }, timeout=(60,120))
            if response.status_code == 200:
                data = response.json()
                if not data:
                    logger.info("No more data to fetch.")
                    break
           
                offset += limit

                df_data = pd.DataFrame(data)
                df_data = df_data[columns]  # Ensure the DataFrame has the correct column order

                df_data.to_csv(csv_file, mode='a', header=not file_exists, index=False)

                if not file_exists:
                    file_exists = True

                logger.info(f"Fetched {len(df_data)} records...")

            elif response.status_code == 503:
                logger.warning("Service unavailable. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
                continue

            elif response.status_code == 429:
                logger.warning("Rate limit exceeded. Retrying...")
                time.sleep(10)  # Wait for 10 seconds before retrying
                continue

            else:
                logger.error(f"Error: {response.status_code}")
                break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.error(f"Request failed: {e}")
            break
    
    
    try:
        df = pd.read_csv(csv_file) if file_exists else pd.DataFrame()
    except Exception as e:
        logger.critical(f"Error reading CSV file after extraction: {e}")
        raise

    logger.info(f"Extraction completed: {len(df)} records loaded from {csv_file}")

    return df
    

if __name__ == "__main__":
    df = extract_data()
    print(df.head())
    print(df.info())
    print(df.describe())