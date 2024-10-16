import zipfile
import os

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