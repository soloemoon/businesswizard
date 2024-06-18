import pandas as pd
import numpy as np
import pandas_flavor as pf


@pf.register_dataframe_method
def group_concat(
    df: pd.DataFrame,
    group_column: str | list,
    concat_column: str | list,
    delimiter: str = '|'
) -> pd.DataFrame:
    '''
    Collapse multiple values across groups into a single row per group

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    group_column: str | list
        Name of column(s) to group by. Multiple names must be in a list.
    concat_column: str | list
        Name of column(s) to collapse. Multiple names must be in a list
    delimiter: str
        Type of delimiter to use for separation of concat column values   
    Return
    ------
    result: pd.DataFrame
        Summarised dataframe with one row (grouping) and multiple values
    '''
    
    result = df.groupby(group_column)[concat_column].agg(lambda x: f'{delimiter} '.join(x))
    return result