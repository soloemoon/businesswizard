from typing import List, Tuple

import pandas as pd
import matplotlib as plt
import seaborn as sns
import pandas_flavor as pf


@pf.register_dataframe_method
def heatmap(
    df: pd.DataFrame,
    index_column: str,
    columns: str | List[str],
    values_column: str,
    figure_size: Tuple = (9,6)
):
    df_pivot = df.pivot(index_column, columns, values_column)
    f, ax = plt.subplots(figsize=(figure_size))
    hm = sns.heatmap(df_pivot, annot=True, fmt='d', linewidht=.5, ax=ax)
    return hm