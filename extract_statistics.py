import datetime
from datetime import timedelta

import pandas as pd
import numpy as np

from utils.datetime_utils import day_of_year_to_date
from utils.io import read_enbw_dataset
import seaborn as sns
import matplotlib.pyplot as plt

from visualize import visualize_household

data = read_enbw_dataset('data/data-sun-holidays.csv')

groups = data.groupby('id')

# get customer
household_id = 3
group = groups.get_group(household_id)
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

alpha = 0.005
gamma = 4
beta = 1 / 2
m = np.reshape([1, 2], (2, 1))

assumed_inactivity = average_day.sort_values(by='mean').iloc[0:4, :].mean()
assumed_inactivity_std = assumed_inactivity['std']
overall_std = group.value.std()

night = [0, 1, 2, 3, 4, 23]
night_hours = np.zeros((24, 1), dtype=np.bool)
night_hours[night] = True

inactivity_anomaly_vectors = []
is_nocturnal_activity_vectors = []

# for day, day_group in grouped_by_day:
day_manual = 0
# day = 229

seasonal_mean = group.resample('1W').mean()

for day, day_group in grouped_by_day:
    try:
        if day_manual > 0:
            day_group = grouped_by_day.get_group(day_manual)
        day_statistics = day_group.resample('1H').value.agg(['mean', 'min', 'max', 'std'])
        day_statistics['offset'] = pd.to_timedelta(day_statistics.index.hour, unit='H')

        date = day_of_year_to_date(day, 2014)
        seasonal_mean['sort_val'] = abs((seasonal_mean.index - date).days)
        overall_mean = seasonal_mean.sort_values('sort_val').iloc[0]['value'] + beta * assumed_inactivity_std

        merged_statistics = day_statistics.merge(average_day, how='left', left_on=day_statistics.offset,
                                                 right_on=average_day.index)

        expectations_to_inactivity = (
                    (average_day['mean'] - assumed_inactivity['mean']) / assumed_inactivity['std']).values
        is_unexpected = average_day['mean'] > overall_mean

        deviation_from_inactivity = (
                (merged_statistics['mean_x'] - assumed_inactivity['mean']) / assumed_inactivity['std']).values
        # comparison_to_night_activity.index.name = 'index'

        deviation_from_expectation = ((merged_statistics['mean_x'] - merged_statistics['mean_y']) / merged_statistics[
            'mean_y']).values

        is_inactivity = deviation_from_inactivity < alpha * overall_std
        is_inactivity_indices, = np.where(deviation_from_inactivity)

        inactivity_anomaly_vector = np.sum(np.vstack((is_unexpected, is_inactivity)).astype(np.int32) * m, axis=0)
        inactivity_anomaly_vectors.append(inactivity_anomaly_vector)

        # 2. anomaly: nocturnal activity
        nocturnal_activity_vector = np.logical_and(deviation_from_expectation > gamma, night_hours).astype(np.int)
        is_nocturnal_activity_vectors.append(nocturnal_activity_vector)
        if day_manual > 0:
            break
    except ValueError:
        continue

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

first = '2014-01-01 00:00:00'
last = '2014-12-31 23:59:59'
unexpected_anomalies_str = [[x.strftime('%Y-%m-%d %H:%M:%S') for x in r] for r in unexpected_anomalies]

group['isAnomaly'] = 0
group['anomalyType'] = 'None'
start, end = unexpected_anomalies[0]
b = np.logical_and(start <= group.index, group.index <= end)
idx, = np.where(b)

group.iloc[idx.tolist(), 5] = 1
group.iloc[idx.tolist(), 6] = 'lowActivity'


unexpected_anomalies_count = 0
current_anomaly = []
unexpected_anomalies = []
min_anomaly_length = 5
year = 2014
for k, y in enumerate(Y):
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

first = '2014-01-01 00:00:00'
last = '2014-12-31 23:59:59'
unexpected_anomalies_str = [[x.strftime('%Y-%m-%d %H:%M:%S') for x in r] for r in unexpected_anomalies]
visualize_household(group, first, last, unexpected_anomalies_str)