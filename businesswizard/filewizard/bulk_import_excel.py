import pandas as pd
from fnmatch import fnmatch
from janitor import clean_names, remove_empty

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