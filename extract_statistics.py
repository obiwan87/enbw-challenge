import datetime
from datetime import timedelta

import pandas as pd
import numpy as np

from utils.datetime_utils import day_of_year_to_date
from utils.io import read_enbw_dataset
import seaborn as sns
import matplotlib.pyplot as plt

data = read_enbw_dataset('data/data-sun-holidays.csv')

groups = data.groupby('id')

# get customer
group = groups.get_group(2)
group.set_index(group.timestampLocal, inplace=True)
group.dropna(inplace=True)
# group by day and create average day
grouped_by_hour = group.groupby(lambda x: pd.to_timedelta(x.hour, unit='H'))

average_day = grouped_by_hour.value.agg(['mean', 'min', 'max', 'std'])

grouped_by_day = group.groupby(lambda x: x.dayofyear)

means_of_days = grouped_by_day.value.agg(['min', 'max', 'mean', 'std'])

means_of_days.index.name = 'day_of_year'
means_of_days['date'] = [day_of_year_to_date(d, 2014) for d in means_of_days.index.values]
means_of_days.set_index('date', inplace=True)

alpha = 2.7
gamma = 4
beta = 3.5
m = np.reshape([1, 2], (2, 1))

night = [0, 1, 2, 3, 4, 23]
night_hours = np.zeros((24, 1), dtype=np.bool)
night_hours[night] = True

inactivity_anomaly_vectors = []
is_nocturnal_activity_vectors = []

for day, day_group in grouped_by_day:
    # day_group = grouped_by_day.get_group(day_of_year)

    # for day, day_group in grouped_by_day:
    day_statistics = day_group.resample('1H').value.agg(['mean', 'min', 'max', 'std'])
    day_statistics['offset'] = pd.to_timedelta(day_statistics.index.hour, unit='H')

    merged_statistics = day_statistics.merge(average_day, how='left', left_on=day_statistics.offset,
                                             right_on=average_day.index)

    night_activity = average_day.iloc[0:4, :].mean()
    expectations_to_inactivity = ((average_day['mean'] - night_activity['mean'])/night_activity['std']).values
    is_unexpected = expectations_to_inactivity > beta

    comparison_to_night_activity = ((merged_statistics['mean_x'] - night_activity['mean']) / night_activity['std']).values
    # comparison_to_night_activity.index.name = 'index'
    comparison_to_expectation = (merged_statistics['mean_x'] - merged_statistics['mean_y']) / merged_statistics[
        'mean_y']
    comparison_to_expectation.index.name = 'index'

    is_inactivity = comparison_to_night_activity < alpha
    is_inactivity_indices, = np.where(comparison_to_night_activity)
    nocturnal_activity_vector = np.logical_and(comparison_to_expectation.values > gamma, night_hours).astype(np.int)

    inactivity_anomaly_vector = np.sum(np.vstack((is_unexpected, is_inactivity)).astype(np.int32) * m, axis=0)
    inactivity_anomaly_vectors.append(inactivity_anomaly_vector)
    is_nocturnal_activity_vectors.append(nocturnal_activity_vector)

Y = np.hstack(inactivity_anomaly_vectors)

# plt.figure()
# plt.bar(comparison_to_night_activity.index.values, comparison_to_night_activity)
# plt.ylim(-3, 8)
# # break

unexpected_anomalies_count = 0
current_anomaly = []
unexpected_anomalies = []
min_anomaly_length = 5
year = 2014
for k, y in enumerate(Y):
    if y >= 2:
        if y >= 3:
            unexpected_anomalies_count += 1
        current_anomaly.append(k)
    else:
        if unexpected_anomalies_count >= min_anomaly_length:
            anomaly_range = \
                [
                    datetime.datetime(year, 1, 1) + datetime.timedelta(hours=int(current_anomaly[0])),
                    datetime.datetime(year, 1, 1) + datetime.timedelta(hours=int(current_anomaly[-1])),
                ]

            unexpected_anomalies.append(anomaly_range)

        current_anomaly = []
        unexpected_anomalies_count = 0

