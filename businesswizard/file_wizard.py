import pandas as pd
from fnmatch import fnmatch
from janitor import clean_names, remove_empty
import zipfile
import os
import re
import duckdb
import win32

default_header_format = {
    'bold': True,
    "text_wrap": True,
    "valign": 'top',
    'fg_color': '#4F81BD',
    'font_color': 'white',
    'border': 1
}

def __csv_encodings(path, **kwargs):
    csv_encodings = ['utf-8', 'utf-8-sig', 'iso-8859-1', 'latin1','cp1252']

    for e in csv_encodings:
        try:
            temp = (
                pd.read_csv(path, encoding=e, engine= 'pyarrow', **kwargs)
                .clean_names()
                .remove_empty()
            )
        except Exception as e:
            pass
    return temp

def bulk_import_csv(file_paths, **kwargs) -> pd.DataFrame:
    '''
    Read multiple csv file and concatenate data into a single dataframe

    Parameters
    ----------
    file_paths: list
        List of csv file paths to read in
    
    Returns
    ----------
    df: pd.DataFrame
        Dataframe of concatenated csv files
    '''

    csv_files = [file for file in file_paths if fnmatch(file, '*.csv')]

    df = pd.DataFrame()
    for i in range(0, len(csv_files)):
        temp = __csv_encodings(path=r''+csv_files[i], **kwargs)
        df = pd.concat([temp, df])
        
    return df

def bulk_import_excel(file_paths, **kwargs) -> pd.DataFrame:
    '''
    Read multiple excel files and concatenate data into a single dataframe.

    Parameters
    ----------
    file_paths: list
        List of excel filepaths to ingest.
    **kwargs: TYPE
        Additional pd.read_excel options
    
    Returns
    --------
    df: pd.DataFrame
        Dataframe of concatenated excel files
    '''

    xlsx_files = [file for file in file_paths if fnmatch(file, '*.xls?')]

    df = pd.DataFrame()
    for i in range(0, len(xlsx_files)):
        temp = (
            pd.read_excel(r''+xlsx_files[i], dtype_backend='pyarrow', **kwargs)
            .clean_names()
            .remove_empty()
        )
    
        df = pd.concat([temp, df])
        del temp
    return df

def compress_file(file_list, zip_file_name) -> str:
    '''
    Compress file(s) into a zip

    Parameters
    ----------
    file_list: list
        List of filepaths to use
    zip_file_name: str
        File path of the output zip
    '''

    if isinstance(file_list, str) == True:
        file_list = [file_list]
    
    with zipfile.zipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
        for f in file_list:
            myzip.write(f)
    
    return zip_file_name

def create_excel_report(
    df: pd.DataFrame,
    file_name: str,
    sheet_name: str = 'Report',
    header_format: dict = default_header_format,
    excel_engine = 'xlsxwriter'
) -> None:

    """
    Exports dataframe to a pre-formatted excel file

    Parameters
    ----------
    df: pd.DataFrame
        Dateframe to export
    file_name: str
        Name of file to export
    sheet_name: str, otpional
        Name of the sheet in Excel
    header_format: dict, optional
        Format of the report header
    excel_engine: str, optional
        Excel Writer enginge to use
    
    Returns
    -------
    None
    """

    writer = pd.ExcelWriter(file_name, engine=excel_engine)

    df.to_excel(writer, index=False, sheet_name=sheet_name, startrow=1, header=False)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    for i, col in enumerate(df.columns):
        width = max(df[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet.set_column(i, i, width)
    
    header = workbook.add_format(header_format)

    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num + 1, value, header)
    
    writer.save()
    
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

def refresh_excel_workbook(workbook_name) -> None:
    '''
    Refresh an Excel Workbook

    Parameters
    ----------
    book_name: str
        Name of excel workbook_name
    
    Returns
    -------
    None
    '''

    xl = win32.Dispatch('Excel.Application')
    xl.DisplayAlerts = False
    wb = xl.Workbooks.Open(workbook_name)
    xl.Visible = False
    wb.RefreshAll()
    wb.Save()
    wb.Close(True)
    print(f'{workbook_name} has been refreshed')