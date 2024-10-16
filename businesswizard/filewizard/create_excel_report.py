import pandas as pd

default_header_format = {
    'bold': True,
    "text_wrap": True,
    "valign": 'top',
    'fg_color': '#4F81BD',
    'font_color': 'white',
    'border': 1
}

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
    
