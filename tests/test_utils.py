import pandas as pd
from src.transform.utils import remove_accents, clean_text

def test_normal_cases_remove_accents():
    assert remove_accents("café") == "cafe"
    assert remove_accents("naïve") == "naive"
    assert remove_accents("résumé") == "resume"
    assert remove_accents("São Paulo") == "Sao Paulo"
    assert remove_accents("façade") == "facade"
    assert remove_accents("coöperate") == "cooperate"
    assert remove_accents("crème brûlée") == "creme brulee"
    assert remove_accents("niño") == "nino"
    assert remove_accents("jalapeño") == "jalapeno"
    assert remove_accents("über") == "uber"

def test_edge_cases_remove_accents():
    assert remove_accents("") == ""
    assert remove_accents(" ") == " "
    assert remove_accents("!@#$%^&*()") == "!@#$%^&*()"
    assert remove_accents("São Paulo?") == "Sao Paulo?"
    assert remove_accents("façade,") == "facade,"
    assert remove_accents(123) == 123 # Non-string input should return the same value
    assert remove_accents(None) == None # Non-string input should return the same value


def test_clean_text_mayusculas():
    serie = pd.Series(["bogotá", "medellín"])
    resultado = clean_text(serie)
    assert resultado[0] == "BOGOTA"
    assert resultado[1] == "MEDELLIN"

def test_clean_text_strip_caracteres_especiales():
    # verifica que elimina los caracteres del inicio y final
    serie = pd.Series(["*BOGOTA*", "[MEDELLIN]", "..CALI..","(CA(LI)"])
    resultado = clean_text(serie)
    assert resultado[0] == "BOGOTA"
    assert resultado[1] == "MEDELLIN"
    assert resultado[2] == "CALI"
    assert resultado[3] == "(CA(LI)"  # los paréntesis no se eliminan porque no están en la lista de strip

def test_clean_text_no_toca_el_medio():
    # el strip solo actúa en los extremos, no en el medio
    serie = pd.Series(["BOGO*TA"])
    resultado = clean_text(serie)
    assert resultado[0] == "BOGO*TA"

def test_clean_text_con_none():
    serie = pd.Series([None, "bogotá"])
    resultado = clean_text(serie)
    assert resultado[0] is None or pd.isna(resultado[0])
    assert resultado[1] == "BOGOTA"