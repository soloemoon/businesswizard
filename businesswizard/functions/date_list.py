import pandas as pd
from datetime import datetime, timedelta
import pydoc

def __date_range_calc(
    start_date, 
    end_date, 
    number_of_days, 
    date_format = '%Y-%m-%d'
) -> list:
    
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)

    d1 = pd.period_range(start_date, end_date, periods=number_of_days)
    d1 = sorted(d1)
    return d1

def __month_output(dl, date_format):
    date_list = date_list[date_list.day==1]
    date_list = sorted(date_list)
    date_list = [x.strftime(date_format) for x in date_list]
    return date_list

def create_date_list(
    start_date: str,
    end_date: str,
    number_of_days: int = 1,
    date_format: str = "%Y-%m-%d",
    remove_weekends: bool = False,
    output_months: bool= False
) -> list:
    """
    Creates a list of months based on the first day of each month.

    Parameters
    ----------
    start_date: str
        Starting Date
    end_date: str
        Ending Date
    number_of_days: int, optional
        Number of days to increment dates by
    date_format: str, optional
        Optional date format. YYYY-MM-DD is the default
    remove_weekends: bool, optional
        Determines if dates that fall on a weekend should be removed
    output_months: bool, optional
        Determines if dates should reflect the start of the month
    
    Returns
    -----------
    date_list: list
        Sorted list of dates
    """

    date_list = __date_range_calc(start_date, end_date, number_of_days, date_format)
    
    if output_months == True:
       date_list = __month_output(date_list, date_format)
    else:
        date_list = [ x.strftime(date_format) for x in date_list if remove_weekends==True ]
    return date_list

pydoc.writedoc('create_date_list')
