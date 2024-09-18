import pandas as pd
from hashkey_generator import generate_md5


def dataframe_full_refresh_timestamp(dataframe, identifier):

    # Convert timestamp column to datetime.
    dataframe['TIME_STAMP'] = pd.to_datetime(dataframe['TIME_STAMP'])

    # Sort by identifier and timestamp, then drop duplicated to keep the latest
    latest_records_df = dataframe.sort_values(by = [identifier, 'TIME_STAMP'], ascending = [True, False]).drop_duplicates(subset = [identifier], keep = 'first')

    latest_records_df['MD5_HASH'] = latest_records_df.apply(generate_md5, axis = 1)

    return latest_records_df