import pandas as pd
import pyodbc
import sqlparse

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
        

def execute_sql_commanges(file_path, connection):
    """
    Import a sql file and execute all embedded SQL commands. 

    Parameters
    ----------
    query_file_path: str
        File path of SQL
    
    Returns
    -------
    None
    """

    sql_commands = open(file_path, 'r').read().split(';')
    sql_commands = [x.strip() for x in sql_commands]

    for command in sql_commands:
        try:
            command = sqlparse.format(command, strip_comments = True).strip()
            pd.io.sql.execute(command, connection)
        except Exception as e:
            print(e)
    
    print('All Queries Successfully Executed')


def check_duplicates(connection, column_id, table_name) ->pd.DataFrame:
    """
    Check a table for duplicate records 

    Parameters
    ----------
    connection: str
        Name of the connection string
    column_id: str
        Name of the column to check for duplicate records
    table_name: str
        Name of the database table
    
    Returns
    -------
    result: pd.DataFrame
        Dataframe of the results
    """
    query = f"Select {column_id}, count(distinct {column_id}) from {table_name} Group By 1 Having count(distinct {column_id}) >1"
    result = pd.read_sql_query(query, connection)
    return result