import re
import query_tools
import pandas as pd
import numpy as np

from concurrent.futures import ThreadPoolExecutor
from typing import c, List, Dict, Tuple, Iterable

class ColNameCleaner:
    '''
    Class for making Dataframe column names SQL friendly

    Class Methods
    -------------
    clean: str
        Strips non-alphanumeric characters and replaces spaces with underscores
    '''

    @classmethod
    def clean(cls, colnames: str) -> List[str]:
        '''
        Converts column names to SQL-friendly format;

        Strips non-alphanumeric characters and replaces spaces with underscores

        Parameters
        ----------
        colnames: pd.Series
            Pandas series of column names (Dataframe.columns attribute)
        
        Returns
        -------
        List[str]
        '''
        return [cls._clean_colname(colname) for colname in colnames]

    @classmethod
    def _clean_colname(cls, colname: str) -> str:
        '''
        Cleans individual column name by stripping non-alphanumeric characters and replaces spaces with underscores

        Parameters
        ----------
        colname: str
            Column name to clean
        
        Returns
        -------
        str
        '''

        colname = cls._standardize_case(colname)
        colname = cls._replace_spaces(colname)
        colname = cls._remove_nonalphanumeric_characters(colname)
        return colname
    
    @staticmethod
    def _standardize_case(colname: str) -> str:
        '''
        Set column name to lower case

        Parameters
        ----------
        colname: str
            Column name to clean
        
        Returns
        -------
        str
        '''

        return colname.lower()
    
    @staticmethod
    def _replace_spaces(colname: str) -> str:
        '''
        Replace spaces with underscores

        Parameters
        ----------
        colname: str
            Column name to clean
        
        Returns
        -------
        str
        '''
        return colname.replace(' ', '_')
    
    @staticmethod
    def _remove_nonalphanumeric_characters(colname: str) -> str:
        '''
        Strip non-alphanumeric characters

        Parameters
        ----------
        colname: str
            Column name to clean
        
        Returns
        -------
        str
        '''

        return re.sub('[^a-zA-Z0-9_]', '', colname)

   
class ColumnLengthProcessor:
    '''
    Class to calculate and standardize column lengths to make them SQL-compatible

    Class Methods
    -------------
    process: Tuple[pd.DataFrame, Dict[str, int]]
        Calculate maximum column lengths and truncate columns that are too long (65,535 characters)
    '''
    _max_length = 65535

    @classmethod
    def process(cls, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
        '''
        Calculate maximum column lengths and tuncate columns that are too long (65,535 characters)

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe to process for SQL upload
        
        Returns
        -------
        Tuple[pd.DataFrame, Dict[str, int]]
            Tuple of prepared DataFrame and Dictionary of column names and maximum lengths
        '''
        column_lengths = cls._get_column_lengths(df)
        return cls._prepare_columns(df, column_lengths)
    
    @staticmethod
    def _get_column_lengths(df: pd.DataFrame) -> Dict[str, int]:
        '''
        Create dictionary of column names and maximum lengths

        Parameters
        ----------
        df: pd.DataFrame 
            Data to process for SQL upload
        
        Returns
        -------
        Dict[str, int]
        '''

        column_lengths = {}
        for colname in df.columns:
            column_length = df[colname].str.len().max()
            column_lengths[colname] = column_length
        return column_lengths
    
    @classmethod
    def _prepare_columns(
        cls, df: pd.DataFrame, 
        column_lengths: Dict[str, int]
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        
        '''
        Update column lengths

        Columns that exceed maximum allowable length will be truncated and column length will be updated:
        Empty columns will be set to a default length of 10

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame to process for SQL upload
        column_lengths: Dict[str, int]
            Dictionary that maps column names to maximum length
        
        Returns
        -------
        Tuple[pd.DataFrame, Dict[str, int]]
            Tuple of prepared DataFrame and Dictionary of column names and maximum legnths
        '''

        for colname, length in column_lengths.items():
            if length > cls._max_length:
                df[colname] = cls._truncate_column(df[colname])
                column_lengths[colname] = cls._max_length
            elif length == 0 or length is np.nan:
                column_lengths[colname] = 10
            else:
                column_lengths[colname] = round(length)
        return df, column_lengths
    
    @classmethod
    def _truncate_column(cls, column: pd.Series) -> pd.Series:
        '''
        Truncate column to maximum allowable column length

        Parameters
        ----------
        column: pd.Series
            Column to be trucnated
        
        Returns
        -------
        pd.Series
        '''

        return column.str.slice(0, cls._max_length)


class RowCleaner:
    '''
    Class for prepareing DataFrame rows for upload to database

    Class Methods
    -------------
    clean: List[str]
        Replaces missing values with None for upload
    '''

    _replacement_list = [np.nan, 'NULL', 'null']

    @classmethod
    def clean(cls, row: pd.Series) -> List[str]:
        '''
        Clean columns
        '''
        return [None if item in cls._replacement_list else f"'{item}'" for item in row]


class QueryBuilder:
    '''
    Base class for SQL Generating Classes
    '''
# Needs to be user input
    _table_prefix = ''
    _table_suffix = ''
    _schema = ''

    @classmethod
    def _prepare_table_name(cls, table_name: str) -> str:
        '''
        Format table name with prefix, suffix, and schema

        Parameters
        ----------
        table_name: str
            Destination table name
        
        Returns
        -------
        str
        '''
        return f'"{cls._schema}"."{cls._table_prefix}_{table_name}_{cls._table_suffix}"'

   
class CreateTableBuilder(QueryBuilder):
    '''
    A class for creating CREATE TABLE queries

    Class Methods
    -------------
    build: query_tools.Query
        Creates CREATE TABLE query based on maximum column lengths
    '''

    _create_string = 'CREATE TABLE'

    @classmethod
    def build(cls, table_name: str, column_lengths: Dict[str, int]) -> query_tools.Query:
        '''
        Creates CREATE TABLE query based on maximum column legnths

        Parameters
        ----------
        table_name: str
            Name of destination table
        column_lengths: Dict[str, int]
            Dictionary that maps column lengths to column names
        
        Returns
        -------
        query_tools.Query
        '''

        table_name = cls._prepare_table_name(table_name)
        create_string = cls._build_create_string(table_name)
        column_string = cls._build_column_string(column_lengths)
        full_query_string = cls._combine_query_components(create_string, column_string)
        return cls._convert_to_query(full_query_string)

    @classmethod 
    def _build_create_string(cls, table_name: str) -> str:

        '''
        Creates 'CREATE TABLE "{schema}.{table}"' string

        Parameters
        ----------
        table_name: str
            Name of destination table
        
        Returns
        -------
        str
        '''

        return f'{cls._create_string} {table_name}'
    
    @staticmethod
    def _build_column_string(column_lengths: Dict[str, int]) -> str:
        '''
        Builds column definition portion of CREATE TABLE query

        Parameters
        ----------
        column_lengths: Dict[str, int]
            Dictionary that maps column lengths to column names
        
        Returns
        -------
        str
        '''
        
        column_list = []
        for colname, length in column_lengths.items():
            col_string = f'\n\t"{colname}" varchar({length})'
            column_list.append(col_string)
        col_string = ','.join(column_list)
        return f'({col_string}\n);'
    
    @staticmethod
    def _combine_query_components(create_string: str, column_string: str) -> str:
        '''
        Combines CREATE TABLE clause and column definition statement to create full query

        Parameters
        ----------
        create_string: str
            CREATE TABLE clause string
        column_string: str
            Column definition portion of CREATE TABLE query
        
        Returns
        -------
        str
        '''

        return create_string + column_string
   
    @staticmethod
    def _convert_to_query(full_query_string: str) -> query_tools.Query:
        '''
        Converts full query string to executable Query object

        Parameters
        ----------
        full_query_string: str
            Full CREATE TABLE query string
        
        Returns 
        -------
        query_tools.Query
        '''

        return query_tools.Query(full_query_string)


class InsertIntoBuilder(QueryBuilder):
    '''
    Class to create executable INSERT INTO queries

    Class Methods
    -------------
    build: Iterable[query_tools.Query]
        Yields executable INSERT INTO queries for each row in input DataFrame
    '''
    _insert_string = 'INSERT INTO'

    @classmethod
    def build(cls, table_name: str, df: pd.DataFrame) -> Iterable[query_tools.Query]:
        '''
        Yields executable INSERT INTO queries for each row in input DataFrame

        Parameters
        ----------
        table_name: str
            Name of destination table
        df: pd.DataFrame
            Dataframe to be uploaded

        Returns
        -------
        Iterable[query_tools.Query]
        '''

        table_name = cls._prepare_table_name(table_name)
        insert_string = cls._build_insert_string(table_name)
        placeholder_string = cls._build_placeholder_string(df)
        full_query_string = cls._build_full_query_string(insert_string, placeholder_string)
        for _, row in df.iterrows():
            row = cls._clean_row(row)
            yield cls._build_query(full_query_string, row)

    @staticmethod
    def _build_placeholder_string(df: pd.DataFrame) -> str:
        '''
        Builds VALUES () portion of INSERT query with ? placeholders

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe to be uplaoded to database
        
        Returns
        -------
        str
        '''

        placeholders = ['?' for _ in df.columns]
        placeholders = ','.join(placeholders)
        return f'VALUES ({placeholders});'
    
    @classmethod
    def _build_insert_string(cls, table_name: str) -> str:
        '''
        Build CREATE TABLE {table_name} clause

        Parameters
        ----------
        table_name: str
            Destination table name
        
        Returns
        -------
        str
        '''
        return f'{cls._insert_string} {table_name}'
    
    @staticmethod
    def _build_full_query_string(insert_string: str, placeholder_string: str) -> str:
        '''
        Combines INSERT INTO clause and placeholder string to create full query

        Parameters
        ----------
        insert_string: str
            INSERT INTO clause string
        column_string: str
            Placeholder string
        
        Returns
        -------
        str
        '''

        return f'{insert_string} {placeholder_string}'
    
    @staticmethod
    def _clean_row(row: pd.Series) -> List[str]:
        '''
        Prepare row for upload to database

        Parameters
        ----------
        row: pd.Series
            Row to be uploaded to database
        
        Returns
        -------
        List[str]
        '''
        return RowCleaner.clean(row)
    
    @staticmethod
    def _build_query(full_query_string: str, row: list[str]) -> query_tools.Query:
        '''
        Converts full query string into executable Query object

        Parameters
        ----------
        full_query_string: str
            Full text of INSERT INTO query
        row: List[str]
            Row to be uploaded to database
        
        Returns
        -------
        query_tools.Query
        '''

        return query_tools.Query(full_query_string, params=row)

  
class DataLoader:
    '''
    Class for loading DataFrame into database table

    Attributes
    ----------
    query_manager: query_tools.QueryManager
        QueryManager object connected to database
    
    Methods
    -------
    load: None
        Loads Dataframe into table
    '''

    def __init__(self, query_manager: query_tools.QueryManager):
        '''
        Parameters
        ----------
        query_manager: query_tools.QueryManager
            QueryManager object connected to database
        '''
        self.query_manager = query_manager
    
    def load(self, table_name:str, df: pd.DataFrame) -> None:
        '''
        Loads DataFrame into table

        Parameters
        ----------
        table_name: str
            Name of destinateion table
        df: pd.DataFrame
            Dataframe to be loaded into database
        
        Returns
        --------
        None
        '''
        self._create_table(table_name, df)
        self._load_data(table_name, df)

    def _create_table(self, table_name: str, df: pd.DataFrame) -> None:
        '''
        Creates and executes CREATE TABLE query to build destination table

        Parameters
        ----------
        table_name: str
            Name of destination table
        df: pd.DataFrame
            Dataframe to be loaded into database
        
        Returns
        -------
        None
        '''
        create_query = CreateTableBuilder.build(table_name, df)
        self.query_manager.execute(create_query)

    def _load_data(self, table_name: str, df: pd.DataFrame) -> float:
        '''
        Loads records into target table and returns percentage of records successfully loaded

        Parameters
        ----------
        table_name: str
            Name of destination table
        df: pd.DataFrame
            Dataframe to be loaded into database

        Returns
        -------
        float
        '''

        query_generator = InsertIntoBuilder.build(table_name, df)
        results =[]
        with ThreadPoolExecutor() as executor:
            for result in executor.map(self.query_manager.execute, query_generator):
                results.append(result)
        return sum(results) / len(df.index)
