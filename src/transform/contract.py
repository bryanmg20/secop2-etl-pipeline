import pandas as pd
from . import utils
import logging

logger = logging.getLogger(__name__)

def transform_contract_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the contract data into a structured format suitable for loading into the database.
    Args:
        df (pd.DataFrame): The extracted data."""
    
     #transform contract data
    contract = df[['id_contrato','codigo_entidad','codigo_proveedor',
               
               'fecha_de_inicio_del_contrato',
               'fecha_de_fin_del_contrato','fecha_de_firma','fecha_inicio_liquidacion','fecha_fin_liquidacion', 'ultima_actualizacion',

               'estado_contrato', 'modalidad_de_contratacion', 'origen_de_los_recursos', 'destino_gasto','habilita_pago_adelantado',
               
               'valor_del_contrato','valor_pagado','valor_de_pago_adelantado','valor_pendiente_de_pago','valor_facturado','valor_amortizado',
               'valor_pendiente_de', 'valor_pendiente_de_ejecucion', 
               
               'dias_adicionados','el_contrato_puede_ser_prorrogado',

               'tipo_de_contrato','liquidaci_n','obligaci_n_ambiental','espostconflicto','obligaciones_postconsumo','reversion']].copy()


    columns_to_clean = ['estado_contrato', 'modalidad_de_contratacion', 'origen_de_los_recursos', 'destino_gasto', 'tipo_de_contrato']
    for column in columns_to_clean:
        contract[column] = utils.clean_text(contract[column])

    contract.rename(columns={
        # IDs
        'id_contrato': 'id_contract',
        'codigo_entidad': 'id_entity',
        'codigo_proveedor': 'id_provider',

        # Dates
        'fecha_de_inicio_del_contrato': 'id_contract_start_date',
        'fecha_de_fin_del_contrato': 'id_contract_end_date',
        'fecha_de_firma': 'id_signing_date',
        'fecha_inicio_liquidacion': 'id_liquidation_start_date',
        'fecha_fin_liquidacion': 'id_liquidation_end_date',
        'ultima_actualizacion': 'id_last_update_date',

        # Contract information
        'estado_contrato': 'contract_state',
        'modalidad_de_contratacion': 'method_of_contracting',
        'origen_de_los_recursos': 'source_of_resources',
        'destino_gasto': 'destination_of_expense',
        'tipo_de_contrato': 'contract_type',

        # Monetary values
        'valor_del_contrato': 'contract_value',
        'valor_pagado': 'paid_value',
        'valor_de_pago_adelantado': 'advance_payment_value',
        'valor_pendiente_de_pago': 'pending_payment_value',
        'valor_facturado': 'invoiced_value',
        'valor_amortizado': 'amortized_value',
        'valor_pendiente_de': 'pending_amortization_value',
        'valor_pendiente_de_ejecucion': 'pending_execution_value',

        # Duration
        'dias_adicionados': 'additional_days',
        'el_contrato_puede_ser_prorrogado': 'contract_can_be_extended',

        # Booleans
        'liquidaci_n': 'liquidation',
        'obligaci_n_ambiental': 'environmental_obligation',
        'espostconflicto': 'is_post_conflict',
        'habilita_pago_adelantado': 'allows_advance_payment',
        'obligaciones_postconsumo': 'post_consumer_obligations',
        'reversion': 'reversion'
    }, inplace=True)

    contract.drop_duplicates(inplace=True)

    #transform contract dates to datetime format and then to integer format
    contract['id_contract_start_date'] = pd.to_datetime(contract['id_contract_start_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')
    contract['id_contract_end_date'] = pd.to_datetime(contract['id_contract_end_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')
    contract['id_signing_date'] = pd.to_datetime(contract['id_signing_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')
    contract['id_liquidation_start_date'] = pd.to_datetime(contract['id_liquidation_start_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')
    contract['id_liquidation_end_date'] = pd.to_datetime(contract['id_liquidation_end_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')
    contract['id_last_update_date'] = pd.to_datetime(contract['id_last_update_date'], format='ISO8601', errors='coerce').dt.strftime('%Y%m%d').astype('Int64')


    contract['liquidation'] = contract['liquidation'].map({'Si': True, 'No': False})
    contract['environmental_obligation'] = contract['environmental_obligation'].map({'Si': True, 'No': False})
    contract['is_post_conflict'] = contract['is_post_conflict'].map({'Si': True, 'No': False})
    contract['allows_advance_payment'] = contract['allows_advance_payment'].map({'Si': True, 'No': False, 'No Definido': None})
    contract['post_consumer_obligations'] = contract['post_consumer_obligations'].map({'Si': True, 'No': False})
    contract['reversion'] = contract['reversion'].map({'Si': True, 'No': False})
    contract['contract_can_be_extended'] = contract['contract_can_be_extended'].map({'Si': True, 'No': False})

    logger.info(f"Contract data transformed: {len(contract)} unique records created.")

    return contract