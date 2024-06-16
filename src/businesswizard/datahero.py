import pandas as pd
import numpy as np
import pandas_flavor as pf
from datetime import datetime, timedelta

def __column_to_list(x, dtype='str'):
    '''
    Checks the 
    '''
    if isinstance(x, dtype) == True:
        x = list(x)
    else:
        x


def __business_day_calc(
        start_date: str, 
        end_date: str
        ):
    weekday_friday = 4
    if start_date.weekday() > weekday_friday:
        start_date = start_date + timedelta(days=7 - start_date.weekday())

    if end_date.weekday() > weekday_friday:
        end_date = end_date - timedelta( days = end_date.weekday() - weekday_friday )

    if start_date > end_date:
        return 0

    diff_days = (end_date - start_date).days + 1
    weeks = int(diff_days/7)
    remainder = end_date.weekday() - start_date.weekday() + 1

    if remainder != 0 and end_date.weekday() < start_date.weekday():
        remainder = 5 + remainder
    
    return weeks * 5 + remainder


@pf.register_dataframe_method
def group_concat(
    df: pd.DataFrame,
    group_column: str | list,
    concat_column: str | list,
    delimiter: str = '|'
) -> pd.DataFrame:
    '''
    Collapse multiple values across groups into a single row per group

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    group_column: str | list
        Name of column(s) to group by. Multiple names must be in a list.
    concat_column: str | list
        Name of column(s) to collapse. Multiple names must be in a list
    delimiter: str
        Type of delimiter to use for separation of concat column values   
    Return
    ------
    result: pd.DataFrame
        Summarised dataframe with one row (grouping) and multiple values
    '''

    result = df.groupby(group_column)[concat_column].agg(lambda x: f'{delimiter} '.join(x))
    return result


@pf.register_dataframe_method
def create_list_in_column(
        df: pd.DataFrame,
        column: str | list,
        delimiter: str = '|'
) -> pd.DataFrame:
    '''
    Create lists of values in the rows of a column

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    column: str | list
        Column(s) whose rows should have lists created in.
    delimiter: str, optional
        Delimiter to use to separate the lists
    '''
    # result = df[column].apply(lambda x: [i for i in str(x).split(delimiter)])
    result = df[column].apply(lambda x: list(str(x).split(delimiter)) )
    return result


@pf.register_dataframe_method
def fill_leading_zero(
    df: pd.DataFrame,
    column_name: str | list,
    character_length: int = 10
) -> pd.DataFrame:
    '''
    Add leading zeroes to column(s) based on a required character length.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    column_name: str | list
        Name of column(s) to add leading zeroes to.
    character_length: int, optional
        Number of characters to pad for - determines how many zeroes need to be added. Default is 10.
    Returns
    -------
    df: pd.DataFrame
        Dataframe with leading zeroes added to the desired columns
    '''
    for c in column_name:
        df[c] = df[c].astype(str).str.zfill(character_length)
    
    return df


@pf.register_dataframe_method
def subset_by_group(
    df: pd.DataFrame,
    category_column: str | list
) -> dict | pd.DataFrame:
    '''
    Breaks a dataframe into smaller dataframes based on the column category.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    category_column: str | list
        Name of column containing the category used to subset
    
    Returns
    -------
    result: dict | pd.DataFrame
        Dictionary of dataframes based on category
    '''

    result = dict(iter(df.groupby(category_column)))
    return result


@pf.register_dataframe_method
def dataframe_compare(
    df: pd.DataFrame,
    df2: pd.DataFrame
) -> pd.DataFrame:
    '''
    Compare to dataframes and return a summary of what changed

    Parameters
    ----------
    df: pd.DataFrame
        First dataframe to use in comparison
    df2: pd.DataFrame
        Second dataframe to use in comparison
    
    Returns
    -------
    result: pd.DataFrame
        Summarised dataframe showing changes
    '''
    ne_stacked = (df != df2).stack()
    changed = ne_stacked[ne_stacked]
    changed.index_names = {'id', 'col'}

    difference_locations = np.where(df != df2)

    changed_from = df.values[difference_locations]
    changed_to = df2.values[difference_locations]

    result = pd.DataFrame({'from': changed_from, 'to': changed_to}, index = changed.index)
    return result


@pf.register_dataframe_method
def date_diff(
    df: pd.DataFrame,
    start_date_column: str,
    end_date_column: str,
    calculation: str = 'days'
) -> pd.DataFrame:
    '''
    Computes difference between two date columns in business days (calendar and business), months, or years

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
        calendar_diff_list = [(x-y).days for x,y in zip(end_list, start_list)]
        business_day_diff_list = [__business_day_calc(x, y) for x,y in zip(start_list, end_list)]

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


@pf.register_dataframe_method
def create_flag(
    df: pd.DataFrame,
    lookup_column: str,
    flag_name: str,
    lookup_list: list,
    overwrite_values: bool = True,
    default_value: str = 'N',
    flag_value: str = 'Y',
    map_if_in_list: bool = True
)-> pd.DataFrame:
    '''
    Create a flag column in a dataframe based on list values

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    lookup_column: str
        Column containing the values to map for
    flag_name: str
        Name of the column that contains the flag mappings
    lookup_list: list
        List of values to be used as flag mappings
    overwrite_values: bool, optional
        Determines if missing mappings will be populated with a default of N
    flag_value: str, optional
        What to use to denote if value(s) are found in the lookup list
    map_if_in_list: bool, optional
        Determines if the flag_value should be mapped if values are in the list or not in the list. Default is True (map if values in the list). 

    Returns
    -------
    df: pd.DataFrame
        Dataframe with the mapped values
    '''

    if overwrite_values is True:
        df[flag_name] = default_value
    
    if map_if_in_list is True:
        df.loc[(df[lookup_column].isin(lookup_list)), flag_name] = flag_value
    
    elif map_if_in_list is False:
        df.loc[~(df[lookup_column].isin(lookup_list)), flag_name] = flag_value
    
    return df


def transform_column_strings(
        df: pd.DataFrame,
        column_to_transform: str,
        transformations_dictionary: dict
) -> pd.DataFrame:
    '''
    Transforms a string column within a dataframe based on an input dictionary.
    Ex: Remove the word 'Private', change 'LTD' to 'LTD.', and remove spaces at end within an entity name column.
    transformations_dict ={
        'PRIVATE':'',
        'LTD':'LTD.',
        ' +$':'' # Alternative way to remove whitespace at the end of a string

        names_to_be_screend = names_to_be_screened.transform_column_strings(column_to_transform='company_name, transformations_dictionary = transform_dict)
        }
    
    
    '''
    for word_to_remove, word_to_replace_with in transformations_dictionary.items():
        df[column_to_transform].replace(word_to_remove, word_to_replace_with, inplace=True, regex=True)
    
    df[column_to_transform] = df[column_to_transform].str.strip()

    return df