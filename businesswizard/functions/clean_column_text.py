import pandas as pd
import pandas_flavor as pf
import re


def __lower_text(df, c):
    return [str(x).lower() for x in df[c]]


def __upper_text(df, c):
    return [str(x).upper() for x in df[c]]


def __proper_text(df, c):
    return [str(x).title() for x in df[c]]


@pf.register_dataframe_method
def clean_column_text(
        df: pd.DataFrame,
        columns_to_transform: str | list,
        transformations_dictionary: dict = None,
        remove_special_characters: bool = False,
        use_regex: bool = False,
        change_case: str = None
) -> pd.DataFrame:
    '''
    Clean column text in a variety of ways from changing the case of words, to replacing words, or moving special characters.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe
    columns_to_transform: str | list
        Name of columns to be transformed. Can be either a string or list.
    transformations_dictionary: dict, optional
        Dictionary of word replacements to be made.
    remove_special_characters: bool, optional
        When True, special characters are removed from the column
    use_regex: bool, optional
        Set to true when regex should be used in word replacement
    change_case: str, optional
        Determines if the case of words should be changed. E.g. 'lower' for lowercase.
    Returns
    -------
    df: pd.Dataframe
        Dataframe containing the transformed result
    '''

    case_map = {
        'upper': __upper_text,
        'lower': __lower_text,
        'capitalize': __proper_text,
     }

    # Remove special & weird characters from columns
    for c in columns_to_transform:
        if remove_special_characters is True:
            df[c] = [re.sub('[^A-Za-z]+', '', str(x)) for x in df[c]]
        
        if change_case is not None:
            df[c] = case_map[change_case.lower()](df, c)
        
        if transformations_dictionary is not None:
            df[c].replace(transformations_dictionary, regex=use_regex, inplace=True)
        # Remove numbers
        df[c] = df[c].str.strip()

    return df