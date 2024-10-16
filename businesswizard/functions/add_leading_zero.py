import pandas as pd
import pandas_flavor as pf
from typing import List


@pf.register_dataframe_method
def add_leading_zero(
    df: pd.DataFrame,
    column_name: str | List[str],
    character_length: int = 10
) -> pd.DataFrame:
    '''
    Add leading zeroes to column(s) based on a required character length.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    column_name: str | list
        Name of column(s) to add leading zeroes to.
    character_length: int, optional
        Number of characters to pad for - determines how many zeroes need to be added. Default is 10.
    Returns
    -------
    df: pd.DataFrame
        Dataframe with leading zeroes added to the desired columns
    '''
    for c in column_name:
        df[c] = df[c].astype(str).str.zfill(character_length)
    return df
