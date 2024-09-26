import pandas as pd
from hashkey_generator import generate_md5


def dataframe_full_refresh(dataframe, indentifier):
    """
    Perform a Rank operation and return the latest entry for unique identifier

    Parameters:
    dataframe (pd.DataFrame): The input DataFrame.
    identifier (str): The column name used as the unique identifier for partitioning,

    Returns:
    pd.DataFrame: A DataFrame with only the latest entry for each identifier.
    """

    # Sort by index to ensure the latest entry is the last one for each identifier
    sorted_df = dataframe.sort_index()

    # Drop duplicated based on the identifier, keeping the last occurence
    latest_df = sorted_df.drop_duplicates(subset=indentifier, keep = 'last')

    latest_df['MD5_HASH'] = latest_df.apply(generate_md5, axis = 1)

    return latest_df