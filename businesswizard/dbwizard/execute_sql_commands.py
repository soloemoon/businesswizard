import pandas as pd
import pyodbc
import sqlparse

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