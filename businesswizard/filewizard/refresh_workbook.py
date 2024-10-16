import win32

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
