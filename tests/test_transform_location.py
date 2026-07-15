import pandas as pd
from src.transform.location import transform_location_data

def make_df(**overrides):
    base = {
        'departamento': ['Quindio'],
        'ciudad': ['Armenia'],
    }
    base.update(overrides)
    return pd.DataFrame(base)

# ---- 1. columns renamed correctly ----

def test_columns_renamed():
    result = transform_location_data(make_df())
    assert 'city' in result.columns
    assert 'department' in result.columns
    # verify that the Spanish column names were removed
    assert 'ciudad' not in result.columns
    assert 'departamento' not in result.columns

# ---- 2. text cleaning ----
def test_text_cleaning_removes_accents_and_uppercases():

    data = make_df(
        departamento=['Quindío'],
        ciudad=['Armenía'],
    )
    result = transform_location_data(data)
    assert result['department'].iloc[0] == 'QUINDIO'
    assert result['city'].iloc[0] == 'ARMENIA'

# ---- 5. duplicate removal ----

def test_duplicate_removal():
    data = make_df(
        departamento=['Quindio', 'Quindio'],
        ciudad=['Armenia', 'Armenia'],
    )
    result = transform_location_data(data)
    assert len(result) == 1

def test_none_values():
    data = make_df(
        departamento=[None],
        ciudad=[None],
    )
    result = transform_location_data(data)
    assert pd.isna(result['department'].iloc[0])
    assert pd.isna(result['city'].iloc[0])
   