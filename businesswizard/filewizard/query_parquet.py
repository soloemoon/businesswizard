import re
import duckdb
import pandas as pd

def query_parquet(
    parquet_path: str,
    query: str
) -> pd.DataFrame:
    '''
    Pre-filter a parquet file based on criteria before ingesting

    Parameters
    ----------
    parquet_path: str
        File path of parquet to read
    query: str
        SQL Query to execute against the parquet file
    
    Returns
    ---------
    df: pd.DataFrame
        Dataframe(s) with filtered parquet data
    '''

    query = query.lower()
    start = re.findall(r'select.+?from', query)
    end = re.findall(r'(where.*)', query)

    query = f'{start} read_parquet({parquet_path}) {end}'
    df = duckdb.query(query).to_df()
    return df