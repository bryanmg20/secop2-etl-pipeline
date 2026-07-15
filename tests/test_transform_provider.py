import pandas as pd
from src.transform.provider import transform_provider_data

def make_test_df(**overrides):
    """Create a base DataFrame with one valid row.
    You can override any column with overrides."""
    base = {
        'codigo_proveedor': [1234],
        'proveedor_adjudicado': ['Bryan Montoya'],
        'documento_proveedor': ['10000000'],
        'es_pyme': ['No'],
        'es_grupo': ['No'],
        'tipodocproveedor': ['Cedula de ciudadania']
    }
    base.update(overrides)
    return pd.DataFrame(base)

# ---- 1. columns renamed correctly ----

def test_columns_renamed():
    result = transform_provider_data(make_test_df())
    assert 'id_provider' in result.columns
    assert 'name_provider' in result.columns
    assert 'provider_document' in result.columns
    assert 'is_pyme' in result.columns
    assert 'is_group' in result.columns
    assert 'type_of_provider' in result.columns


# ---- 2. text cleaning ----
def test_text_cleaning():
    result = transform_provider_data(make_test_df())
    assert result['name_provider'].iloc[0] == 'BRYAN MONTOYA'
    assert result['type_of_provider'].iloc[0] == 'CEDULA DE CIUDADANIA'

# ---- 4. boolean mapping ----
def test_boolean_mapping():
    result = transform_provider_data(make_test_df(es_pyme='Si', es_grupo='No'))
    assert result['is_pyme'].iloc[0] == True
    assert result['is_group'].iloc[0] == False

    result = transform_provider_data(make_test_df(es_pyme='No', es_grupo='Si'))
    assert result['is_pyme'].iloc[0] == False
    assert result['is_group'].iloc[0] == True

# ---- 5. duplicate removal ----
def test_duplicate_removal():
    df = make_test_df()
    data = pd.concat([df, df], ignore_index=True)  # duplicate the row
    result = transform_provider_data(data)
    assert len(result) == 1  # Only one unique provider should remain