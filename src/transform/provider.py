from . import utils
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform_provider_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the provider data into a structured format suitable for loading into the database.
    Args:
        df (pd.DataFrame): The extracted data."""
    
    #transform provider data
    provider = df[['codigo_proveedor','proveedor_adjudicado','documento_proveedor', 'es_pyme','tipodocproveedor','es_grupo']].copy()

    provider['proveedor_adjudicado'] = utils.clean_text(provider['proveedor_adjudicado'])
    provider['tipodocproveedor'] = utils.clean_text(provider['tipodocproveedor'])

    provider.rename(columns={'codigo_proveedor':'id_provider','proveedor_adjudicado':'name_provider',
                             'documento_proveedor':'provider_document','es_pyme':'is_pyme',
                             'tipodocproveedor':'type_of_provider','es_grupo':'is_group'}, inplace=True)
    
    provider.drop_duplicates(inplace=True)

    provider['is_pyme'] = provider['is_pyme'].map({'Si': True, 'No': False})
    provider['is_group'] = provider['is_group'].map({'Si': True, 'No': False})

    logger.info(f"Provider data transformed: {len(provider)} unique records created.")

    return provider