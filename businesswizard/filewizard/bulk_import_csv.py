import pandas as pd
from fnmatch import fnmatch
from janitor import clean_names, remove_empty

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

