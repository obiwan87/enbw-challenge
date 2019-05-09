import pandas as pd
import numpy as np

from utils.io import read_enbw_dataset

TIMESTAMP_LOCAL = 'timestampLocal'

fifteen_minutes_in_ns = 900000000000
data_filepath = 'data/hackathon_EnBW_smart_meter_data_30_hh.csv'
data = read_enbw_dataset(data_filepath)
cols = data.columns
date_range_year = pd.date_range(start='2014-01-01 00:00', end='2014-12-31 23:45', freq="15T")

groups = data.groupby(by=data.id)

for key, group in groups:
    group.set_index(group.timestampLocal, inplace=True)

    value_counts = group.index.value_counts()
    print('Group: ', key)
    print('Nans: ', group.isna().sum()['timestampLocal'])
    print(value_counts[value_counts > 1])
    print('Missing: ', date_range_year.difference(group.index))
    #
    # group.set_index(TIMESTAMP_LOCAL, inplace=True)
    # group.drop_duplicates(keep='first')
    #
    # group.dropna(inplace=True)
    #
    # new_group = pd.DataFrame(index=date_range_year, columns=data.columns)
    # del new_group[TIMESTAMP_LOCAL]
    # new_group.index.name = TIMESTAMP_LOCAL
    #
    # to_list = group.index.dropna().to_list()
    # new_group.loc[to_list, 'id'] = group.loc[to_list, 'id'].values
    # stop = 1
