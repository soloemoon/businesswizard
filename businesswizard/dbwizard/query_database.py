import pandas as pd
import pyodbc

def query_database(query, connection, dsn_name) -> pd.DataFrame:
    """
    Parameters
    ----------
    query: str
        File path of .SQL file or query to run
    connection: string
        Connection String
    dsn_name: str
        Name of dsn to use
    
    Returns
    -------
    df: pd.DataFrame
        Dataframe of results
    """

    if query.endswith('.sql')==True:
        query = open(query, 'r').read().strip()
    
    try:
        df = pd.read_sql(query, connection, dtype_backend = 'pyarrow')
        return df
    except:
        return print('Please connect to ODBC and re-run')


        