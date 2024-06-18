import pandas as pd
import pandas_flavor as pf


@pf.register_dataframe_method
def create_flag(
    df: pd.DataFrame,
    lookup_column: str,
    lookup_list: list,
    flag_column_name: str = 'created_flag_column',
    value_in_flag_mapping: str = 'Y',
    value_not_in_flag_mapping: str = 'N'
)-> pd.DataFrame:
    '''
    Create a flag column in a dataframe based on list values

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    lookup_column: str
        Column containing the values to map for
    lookup_list: list
        List of values to be used as flag mappings
    flag_name: str
        Name of the column that contains the flag mappings
    value_in_flag_mapping: str, optional
        The value to be returned if the column value is in the lookup list
    value_not_in_flag_mapping: str, optional
        The value to be returned if the column value is not in the lookup list

    Returns
    -------
    df: pd.DataFrame
        Dataframe with the mapped values
    '''

    if flag_column_name is None:
        flag_column_name = 'created_flag_column'

    bool_values = [True, False]
    bool_mappings = [value_in_flag_mapping, value_not_in_flag_mapping]
    mapping_dict = dict(zip(bool_values, bool_mappings))

    df[flag_column_name] = df[lookup_column].isin(lookup_list).map(mapping_dict)

    return df