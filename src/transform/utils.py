import pandas as pd
import unicodedata

def remove_accents(text) -> str:
    """Remove accents from a given string.
    Args:
        text (str): The input string.
    Returns:
        str: The string without accents.
    """
    if isinstance(text, str):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text

def clean_text(series) -> pd.Series:
    """Clean a pandas Series by removing accents, converting to uppercase, and stripping unwanted characters.
    Args:
        series (pd.Series): The input pandas Series.
    Returns:
        pd.Series: The cleaned pandas Series.
    """
    return series.apply(remove_accents).str.upper().str.strip('*/+-.,;:[] ')


