import pandas as pd
from src.transform.entity import transform_entity_data
import database


def make_test_df(**overrides):
    """Create a base DataFrame with one valid row.
    You can override any column with overrides."""
    base = {
        'departamento': ['Quindio'],
        'ciudad': ['Armenia'],
        'codigo_entidad': [1234],
        'nombre_entidad': ['Entidad de prueba'],
        'nit_entidad': ['900000000'],
        'orden': ['Territorial'],
        'sector': ['servicio publico'],
        'rama': ['ejecutivo'],
        'entidad_centralizada': ['Centralizada'],
    }
    base.update(overrides)
    return pd.DataFrame(base)

# ---- 1. columns renamed correctly ----
def test_columns_renamed():

    engine = database.get_connection()
    schema = "secop2ce"

    result = transform_entity_data(make_test_df(), conn=engine, schema=schema)
    assert 'id_entity' in result.columns
    assert 'name_entity' in result.columns
    assert 'nit_entity' in result.columns
    assert 'order_entity' in result.columns
    assert 'sector_entity' in result.columns
    assert 'branch_entity' in result.columns
    assert 'centralized_entity' in result.columns
    # verify that the Spanish column names were removed
    assert 'codigo_entidad' not in result.columns
    assert 'nombre_entidad' not in result.columns

# ---- 2. text cleaning ----
def test_text_cleaning():

    engine = database.get_connection()
    schema = "secop2ce"

    result = transform_entity_data(make_test_df(), conn=engine, schema=schema)
    assert result['name_entity'].iloc[0] == 'ENTIDAD DE PRUEBA'
    assert result['sector_entity'].iloc[0] == 'SERVICIO PUBLICO'
    assert result['branch_entity'].iloc[0] == 'EJECUTIVO'

# ---- 4. boolean mapping ----
def test_boolean_mapping():

    engine = database.get_connection()
    schema = "secop2ce"

    result = transform_entity_data(make_test_df(), conn=engine, schema=schema)
    assert result['centralized_entity'].iloc[0] == True

    result = transform_entity_data(make_test_df(entidad_centralizada='Descentralizada'), conn=engine, schema=schema)
    assert result['centralized_entity'].iloc[0] == False

# ---- location id ----
def test_location_id_mapping():

    engine = database.get_connection()
    schema = "secop2ce"

    result = transform_entity_data(make_test_df(), conn=engine, schema=schema)
    assert 'id_location' in result.columns
    assert result['id_location'].iloc[0] == 1  # Assuming the location exists in the database

# ---- 5. duplicate removal ----
def test_duplicate_removal():

    engine = database.get_connection()
    schema = "secop2ce"

    df = make_test_df()
    data = pd.concat([df, df], ignore_index=True)  # duplicate the row
    result = transform_entity_data(data, conn=engine, schema=schema)
    assert len(result) == 1  # Only one unique entity should remain