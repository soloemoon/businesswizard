import pandas as pd
import numpy as np
import pandas_flavor as pf
from datetime import datetime, timedelta


def __business_day_calc(
    start_date: str,
    end_date: str
):
    '''
    Function to compute the number of business days
    '''
    weekday_friday = 4
    if start_date.weekday() > weekday_friday:
        start_date = start_date + timedelta(days=7 - start_date.weekday())

    if end_date.weekday() > weekday_friday:
        end_date = end_date - timedelta(days=end_date.weekday()-weekday_friday)

    if start_date > end_date:
        return 0

    diff_days = (end_date - start_date).days + 1
    weeks = int(diff_days/7)
    remainder = end_date.weekday() - start_date.weekday() + 1

    if remainder != 0 and end_date.weekday() < start_date.weekday():
        remainder = 5 + remainder   
    return weeks * 5 + remainder


@pf.register_dataframe_method
def date_diff(
    df: pd.DataFrame,
    start_date_column: str,
    end_date_column: str,
    calculation: str = 'days'
) -> pd.DataFrame:
    '''
    Computes difference between two date columns in business days (calendar and business), months, or years

    Examples
    --------
    df.date_diff(start_date_column = 'starting_dates', end_date_column = 'ending_dates')

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe containing the start and ending date columns
    start_date_column: str
        Name of the column containing the start dates
    end_date_column: str
        Name of the column containing ending dates
    calculation: str, optional
       Determines the date differencing calculation to apply. Default is days. Months and years are also options.
    Returns
    -------
    result: pd.Dataframe
        Dataframe appended with date calculation column(s) added
    '''

    start_list = [pd.to_datetime(x) for x in df[start_date_column].tolist()]
    end_list = [pd.to_datetime(x) for x in df[end_date_column].tolist()]

    # Make calculation parameter lowercase 
    calculation = calculation.lower()

    # Day Calculation and Assignment
    if calculation in ['day', 'd', 'days']:
        calendar_diff_list = [(x - y).days for x, y in zip(end_list, start_list)]
        business_day_diff_list = [__business_day_calc(x, y) for x, y in zip(start_list, end_list)]

        # Assign day calcylation output to columns
        df['date_diff_calendar_days'] = calendar_diff_list
        df['date_diff_business_days'] = business_day_diff_list

    # Month calculation and assignment
    elif calculation in ['month', 'm', 'months']:
        month_diff_list = [(x.year - y.year) * 12 + x.month - y.month for x, y in zip(end_list, start_list)]
        df['date_diff_months'] = month_diff_list
    # Year calcuation and assignment
    elif calculation in ['year', 'y', 'years']:
        year_diff_list = [(x.year - y.year) for x, y in zip(end_list, start_list)]
        df['date_diff_years'] = year_diff_list
    return df
