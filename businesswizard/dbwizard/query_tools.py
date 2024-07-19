import pyodbc
import pandas as pd
from typing import Optional, Iterator

class Query:
    '''
    Class to represent query objects. Contains raw SQL text and optional collection of parameters.

    Attributes
    ----------
    text: str
        Raw SQL query text
    params: Iterator (default=None)
        Collection of parameter values (required for queries with bound parameters i.e. '?')
    '''

    def __init__(self, text: str, params: Optional[Iterator]=None):
        '''
        Parameters
        ----------
        text: str
            Raw SQL Query text
        params: Iterator (default=None)
            Collection of parameter values (required for queries with bound parameters i.e. '?')
        '''
        self.text = text
        self.params = params

class QueryManager:
    '''
    Class for fetching records from database

    Attributes
    ----------
    dsn: str
        System DSN of target database
    
    Methods
    -------
    fetch_records: pd.DataFrame
        Fetches query object result set
    connection_string: str
        Formats connection string for communication with database
    '''

    def __init__(self, dsn: str):
        '''
        Parameters
        ----------
        dsn: str
            System DSN of target database
        '''
        self.dsn = dsn
    
    _dsn_prefix = 'DSN='

    @property
    def connection_string(self) -> str:
        '''
        Formats connection string for communication with database

        Returns
        -------
        str
        '''
        return self._dsn_prefix + self.dsn
    
    @connection_string.setter
    def connection_string(self, value: str) -> None:
        '''
        Setter for connection_string

        Strips connection string formatting and updates dsn attribute

        Parameters
        ----------
        value: str
            Formatted connection string update
        
        Returns
        -------
        None
        '''
        value = value.replace(self._dsn_prefix, '')
        self.dsn = value

    def fetch_records(self, query: Query) -> pd.DataFrame:
        '''
        Fetches Query object results set

        Parameters
        ----------
        query: Query
            Query object for which to fetch results set
        
        Returns
        -------
        pd.DataFrame
        '''
        with pyodbc.connect(self.connection_string, autocommit=True) as conn:
            records = pd.read_sql(query.text, conn, params=query.params)

        return records