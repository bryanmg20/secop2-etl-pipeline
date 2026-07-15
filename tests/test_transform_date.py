import pandas as pd

from src.transform.dim_date import transform_date_data

def make_test_df(**overrides):
    base = {
        'fecha_de_inicio_del_contrato': ['2023-01-01', '2023-02-01', None, 'invalid-date'],
        'fecha_de_fin_del_contrato': ['2023-12-31', None, '2023-11-30', '2023-10-15'],
        'fecha_de_firma': ['2022-12-15', '2022-11-20', None, '2022-10-05'],
        'fecha_inicio_liquidacion': [None, '2023-03-01', '2023-04-01', None],
        'fecha_fin_liquidacion': ['2023-05-31', None, None, '2023-06-30'],
        'ultima_actualizacion': ['2023-07-01', '2023-08-01', None, 'invalid-date'],
    }
    base.update(overrides)
    return pd.DataFrame(base)

# ---- 1. columns renamed correctly ----
def test_columns_renamed():
    result = transform_date_data(make_test_df())
    assert 'date' in result.columns
    assert 'id_date' in result.columns
    assert 'year' in result.columns
    assert 'month' in result.columns
    assert 'day' in result.columns
    assert 'quarter' in result.columns
    assert 'week' in result.columns
    assert 'day_of_week' in result.columns
    assert 'day_name' in result.columns
    assert 'month_name' in result.columns
    assert 'is_weekend' in result.columns


# ---- 2. text cleaning ----

def test_text_cleaning():
    data = make_test_df(
        fecha_de_inicio_del_contrato=['2023-01-01', None, None, None]
    )
    result = transform_date_data(data)
    assert result['date'].iloc[0] == pd.Timestamp('2023-01-01 00:00:00')
    assert result['year'].iloc[0] == 2023
    assert result['month'].iloc[0] == 1
    assert result['day'].iloc[0] == 1
    assert result['quarter'].iloc[0] == 1
    assert result['week'].iloc[0] == 52
    assert result['day_of_week'].iloc[0] == 6
    assert result['day_name'].iloc[0] == 'Sunday'
    assert result['month_name'].iloc[0] == 'January'
    assert result['is_weekend'].iloc[0] == True
    assert result['id_date'].iloc[0] == 20230101

# ---- 5. duplicate removal ----

def test_duplicate_removal():
    data = pd.DataFrame({
        'fecha_de_inicio_del_contrato': ['2023-01-01', '2023-01-01'],
        'fecha_de_fin_del_contrato':    ['2023-01-01', '2023-01-01'],
        'fecha_de_firma':               ['2023-01-01', '2023-01-01'],
        'fecha_inicio_liquidacion':     ['2023-01-01', '2023-01-01'],
        'fecha_fin_liquidacion':        ['2023-01-01', '2023-01-01'],
        'ultima_actualizacion':         ['2023-01-01', '2023-01-01'],
    })
    result = transform_date_data(data)
    assert len(result) == 1  # una sola fecha única entre todas las columnas