import pandas as pd
import pandas_flavor as pf

from typing import List
import pydoc

@pf.register_dataframe_method
def subset_by_group(
    df: pd.DataFrame,
    column_name: List[str] | str
) -> dict:

    """
    Subsets dataframe based on categories in separate dictionary of dataframes

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    column_name: List[str] | str
        List or string of name to subset by
    
    Returns
    -------
    result: dict
        Dictionary of dataframes subset by specified category
    """

    return dict(iter(df.groupby(column_name)))

pydoc.writedoc('subset_by_group')

