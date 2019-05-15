import datetime

import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from matplotlib import pyplot as plt

from utils.io import read_enbw_dataset


def str2float(x):
    return float(x.replace(',', '.'))


def group_by_hour_of_day(d):
    return d.hour


def transform(x):
    return (x - x.mean()) / x.std()


data_filepath = 'data/hackathon_EnBW_smart_meter_data_30_hh.csv'
data = read_enbw_dataset(data_filepath)

groups = data.groupby('id')
group = groups.get_group(2)
group.set_index(group.timestampLocal, inplace=True)

grouped_by_day = group.groupby(lambda x: x.dayofyear)

days = [1, 3, 31, 40, 100, 150, 200, 230, 300, 360]
k = 0
year = 2104
for day in days:
    day_group = grouped_by_day.get_group(day)
    plt.figure()
    day_group['value'].plot()
    print(day)

    current_date = datetime.datetime(year, 1, 1) + datetime.timedelta(day - 1)
    date_string = current_date.strftime('%d.%m., %A')

    k += 1
    plt.title(date_string)
    plt.show()


