import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib import pyplot as plt


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

levels = ['D', 'W', 'M', '4H']
for level in levels:
    plt.figure()
    for i in indices:
        try:
            group = g.get_group(i)
            group = group.set_index('timestampLocal')

            grouped_b

            resampled = group.resample(level)

            mean_per_day = resampled.value.mean().to_frame()
            mean_per_day = mean_per_day.reset_index()

            plt.subplot(n, n, i)
            plt.title(str(i))
            mean_per_day['value'].plot()
        except KeyError:
            print('error')
            continue
    plt.suptitle(level)


