import numpy as np
import pandas as pd
from pandas.tseries import converter
from pandas.plotting import register_matplotlib_converters
from matplotlib import pyplot as plt
import seaborn as sns


def str2float(x):
    return float(x.replace(',', '.'))


def group_by_hour_of_day(d):
    return d.hour


def transform(x):
    return (x - x.mean()) / x.std()


data_filepath = 'data/hackathon_EnBW_smart_meter_data_30_hh.csv'
data = pd.read_csv(data_filepath, delimiter=';', converters={'value': str2float})
data['timestampLocal'] = pd.to_datetime(data.timestampLocal)

g = data.groupby('id')

indices = g.indices.keys()
N = len(indices)
n = np.ceil(np.sqrt(N))


# data = data.dropna() \
#     .groupby(group_by_hour_of_day) \
#     .transform(transform)

data.set_index(data.timestampLocal, inplace=True)
data.dropna(inplace=True)
series = pd.Series(data.value.values, data.index)
t = series.groupby(lambda x: x.hour)\
    .transform(lambda x: (x - x.mean())/x.std())\
    .groupby(lambda x: x.hour)

group = g.get_group(1)

# levels = ['D', 'W', 'M']
# for level in levels:
#     plt.figure()
#     for i in indices:
#         try:
#             group = g.get_group(i)
#             group = group.set_index('timestampLocal')
#
#             grouped_by_day = group.resample(level)
#
#             mean_per_day = grouped_by_day.value.mean().to_frame()
#             mean_per_day = mean_per_day.reset_index()
#
#             register_matplotlib_converters()
#             plt.subplot(n, n, i)
#             plt.title(str(i))
#             mean_per_day['value'].plot()
#         except KeyError:
#             continue
#     plt.suptitle(level)
#
#
