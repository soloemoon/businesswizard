import pandas as pd
import numpy as np
import pandas_flavor as pf
from typing import List


@pf.register_dataframe_method
def group_concat(
    df: pd.DataFrame,
    group_column: str | List[str],
    concat_column: str | List[str],
    delimiter: str = '|'
) -> pd.DataFrame:
    '''
    Collapse multiple values across groups into a single row per group

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    group_column: str | List[str]
        Name of column(s) to group by. Multiple names must be in a list.
    concat_column: str | List[str]
        Name of column(s) to collapse. Multiple names must be in a list
    delimiter: str
        Type of delimiter to use for separation of concat column values   
    Return
    ------
    result: pd.DataFrame
        Summarised dataframe with one row (grouping) and multiple values
    '''

    col_dict = {}
    for col in df:
        if (col in concat_column):
            col_dict[col] = f' {delimiter} '.join
        else:
            col_dict[col] = 'first'
               
    result = df.groupby(group_column, as_index=False).agg(col_dict)
    return result
