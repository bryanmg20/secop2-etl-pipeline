# tests/test_transform_contract.py
import pandas as pd
from src.transform.contract import transform_contract_data

# ---- fixture: minimal valid DataFrame to reuse across several tests ----

def make_test_df(**overrides):
    """Create a base DataFrame with one valid row.
    You can override any column with overrides."""
    base = {
        'id_contrato': ['ABC-123'],
        'codigo_entidad': ['ENT-001'],
        'codigo_proveedor': ['PROV-001'],
        'fecha_de_inicio_del_contrato': ['2023-04-15T00:00:00.000'],
        'fecha_de_fin_del_contrato': ['2024-04-15T00:00:00.000'],
        'fecha_de_firma': ['2023-04-01T00:00:00.000'],
        'fecha_inicio_liquidacion': [None],
        'fecha_fin_liquidacion': [None],
        'ultima_actualizacion': ['2023-05-01T00:00:00.000'],
        'estado_contrato': ['en ejecución'],
        'modalidad_de_contratacion': ['licitación pública'],
        'origen_de_los_recursos': ['nación'],
        'destino_gasto': ['inversión'],
        'habilita_pago_adelantado': ['No'],
        'valor_del_contrato': [1000000],
        'valor_pagado': [500000],
        'valor_de_pago_adelantado': [0],
        'valor_pendiente_de_pago': [500000],
        'valor_facturado': [500000],
        'valor_amortizado': [0],
        'valor_pendiente_de': [0],
        'valor_pendiente_de_ejecucion': [500000],
        'dias_adicionados': [0],
        'el_contrato_puede_ser_prorrogado': ['No'],
        'tipo_de_contrato': ['prestación de servicios'],
        'liquidaci_n': ['No'],
        'obligaci_n_ambiental': ['No'],
        'espostconflicto': ['No'],
        'obligaciones_postconsumo': ['No'],
        'reversion': ['No'],
    }
    base.update(overrides)
    return pd.DataFrame(base)


# ---- 1. columns renamed correctly ----

def test_columns_renamed():
    result = transform_contract_data(make_test_df())
    assert 'id_contract' in result.columns
    assert 'id_entity' in result.columns
    assert 'contract_state' in result.columns
    assert 'contract_value' in result.columns
    # verify that the Spanish column names were removed
    assert 'id_contrato' not in result.columns
    assert 'estado_contrato' not in result.columns


# ---- 2. text cleaning ----

def test_text_cleaning_removes_accents_and_uppercases():
    data = make_test_df(
        estado_contrato=['en ejecución'],
        modalidad_de_contratacion=['licitación pública'],
    )
    result = transform_contract_data(data)
    assert result['contract_state'].iloc[0] == 'EN EJECUCION'
    assert result['method_of_contracting'].iloc[0] == 'LICITACION PUBLICA'


# ---- 3. date conversion to YYYYMMDD integer ----

def test_start_date_converted_to_integer():
    data = make_test_df(fecha_de_inicio_del_contrato=['2023-04-15T00:00:00.000'])
    result = transform_contract_data(data)
    assert result['id_contract_start_date'].iloc[0] == 20230415

def test_null_date_stays_as_na():
    data = make_test_df(fecha_inicio_liquidacion=[None])
    result = transform_contract_data(data)
    assert pd.isna(result['id_liquidation_start_date'].iloc[0])

def test_invalid_date_stays_as_na():
    # errors='coerce' should convert invalid dates to NaT -> NA
    data = make_test_df(fecha_de_inicio_del_contrato=['no-es-una-fecha'])
    result = transform_contract_data(data)
    assert pd.isna(result['id_contract_start_date'].iloc[0])


# ---- 4. boolean mapping ----

def test_yes_no_booleans():
    data = make_test_df(
        liquidaci_n=['Si'],
        obligaci_n_ambiental=['No'],
        reversion=['Si'],
    )
    result = transform_contract_data(data)
    assert result['liquidation'].iloc[0] == True
    assert result['environmental_obligation'].iloc[0] == False
    assert result['reversion'].iloc[0] == True

def test_advance_payment_undefined_maps_to_none():
    # este campo tiene un tercer valor posible: 'No Definido' -> None
    data = make_test_df(habilita_pago_adelantado=['No Definido'])
    result = transform_contract_data(data)
    assert result['allows_advance_payment'].iloc[0] is None or pd.isna(result['allows_advance_payment'].iloc[0])


# ---- 5. duplicate removal ----

def test_removes_duplicates():
    row = make_test_df()
    data = pd.concat([row, row], ignore_index=True)  # two identical rows
    result = transform_contract_data(data)
    assert len(result) == 1