"""Collection of utility functions
"""

import pandas as pd

def _invert_dict_nonunique(d):
    """ Inverting nonunique dictionary 'd'

    Reference:
    [1] http://www.saltycrane.com/blog/2008/01/how-to-invert-dict-in-python/
    """
    newdict = {}
    for k, v in d.iteritems():
        newdict.setdefault(v, []).append(k)
    return newdict

def encoding_col_values_to_num(df, encode_col, lower=True, strip=True):
    """Values of df[encode_col] encoded as numerical pandas.Series + dict

    Result is:
    category_col[category_dict] == df[encode_col]           *

    *: Modulo str.lower() and str.strip(), if applied

    Keyword arguments:
        df -- pandas.Dataframe
        encode_col -- Column (string) encoding is applied to,
               the column should contain strings.
        lower -- Ignore case? Default: True
        strip -- Strip strings? Default: True

    Returns:
        category_col -- pandas.Series
        category_dict -- dict

    Warning: Does not change 'column' in the passed dataframe.

    Todo:
        - Finalize 'presed_dict' functionality: Enabling customized dictionaries.
          currently inversion of dictionary will cause error.
        - Alternatively remove code related to 'prest_dict' (including function '_invert_dict_nonunique')
    """
    column = df[encode_col].copy()
    if lower:
        column = column.apply(str.lower)
    if strip:
        column = column.apply(str.strip)

    categories = column.unique()
    mapping_dict = {category : i for i, category in enumerate(categories)}
    # Inverting mapping_dict:
    category_dict = dict([(v, k) for k, v in mapping_dict.items()])

    category_col = pd.Series(column.map(mapping_dict), dtype=int)

    # Verifies that all rows were successfully coded:
    assert(category_col.isnull().any()==False)

    return category_col, category_dict


def apply_one_hot_encoding(df_in, encode_col, lower=True, strip=True,
                           col_prefix='category_col'):
    """Calls encoding_col_values_to_num and applies pd.get_dummies()

    Returns df with dummy columns and dictionary mapping category to col. value
    """
    df = df_in.copy()
    category_col, category_dict = encoding_col_values_to_num(df, encode_col)
    df[col_prefix] = category_col

    df = pd.get_dummies(df, columns=[col_prefix], drop_first=True)

    return df, category_dict
