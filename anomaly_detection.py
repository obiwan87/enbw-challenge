import datetime

import pandas as pd
import numpy as np

from utils.datetime_utils import day_of_year_to_date
from utils.io import read_enbw_dataset

from visualize import visualize_household


def detect_anomalies(filepath, output_file, visualize=True):
    data = read_enbw_dataset(filepath)
    new_data = []
    groups = data.groupby('id')

    m = np.reshape([1, 2], (2, 1))

    alpha = 0.005
    gamma = 4
    beta = 1 / 2

    year = 2009  # TODO: extract from file

    # get customer
    for household_id, group in groups:

        group.set_index(group.timestampLocal, inplace=True)
        group.dropna(inplace=True)

        first = group.loc[group.index[0], 'timestampLocal']
        last = group.loc[group.index[-1], 'timestampLocal']

        # group by day and create average day
        grouped_by_hour = group.groupby(lambda x: pd.to_timedelta(x.hour, unit='H'))

        average_day = grouped_by_hour.value.agg(['mean', 'min', 'max', 'std'])
        grouped_by_day = group.groupby(lambda x: datetime.datetime(x.year, x.month, x.day))

        assumed_inactivity = average_day.sort_values(by='mean').iloc[0:4, :].mean()
        assumed_inactivity_std = assumed_inactivity['std']
        overall_std = group.value.std()

        night = [0, 1, 2, 3, 4, 23]
        night_hours = np.zeros((24, 1), dtype=np.bool)
        night_hours[night] = True

        inactivity_anomaly_vectors = []
        is_nocturnal_activity_vectors = []

        day_manual = 0
        seasonal_mean = group.resample('1W').mean()
        dates = []
        for date, day_group in grouped_by_day:
            try:
                if day_manual > 0:
                    day_group = grouped_by_day.get_group(day_manual)
                day_statistics = day_group.resample('1H').value.agg(['mean', 'min', 'max', 'std'])
                day_statistics['offset'] = pd.to_timedelta(day_statistics.index.hour, unit='H')

                seasonal_mean['sort_val'] = abs((seasonal_mean.index - date).days)
                overall_mean = seasonal_mean.sort_values('sort_val').iloc[0]['value'] + beta * assumed_inactivity_std

                merged_statistics = day_statistics.merge(average_day, how='left', left_on=day_statistics.offset,
                                                         right_on=average_day.index)

                is_unexpected = average_day['mean'] > overall_mean

                deviation_from_inactivity = (
                        (merged_statistics['mean_x'] - assumed_inactivity['mean']) / assumed_inactivity['std']).values
                # comparison_to_night_activity.index.name = 'index'

                deviation_from_expectation = (
                        (merged_statistics['mean_x'] - merged_statistics['mean_y']) / merged_statistics[
                    'mean_y']).values

                is_inactivity = deviation_from_inactivity < alpha * overall_std

                inactivity_anomaly_vector = np.sum(np.vstack((is_unexpected, is_inactivity)).astype(np.int32) * m,
                                                   axis=0)
                inactivity_anomaly_vectors.append(inactivity_anomaly_vector)

                # 2. anomaly: nocturnal activity
                nocturnal_activity_vector = \
                    np.logical_and(deviation_from_expectation > gamma, night_hours).astype(np.int)
                is_nocturnal_activity_vectors.append(nocturnal_activity_vector)

                date_vector = (merged_statistics.key_0 + date).values
                dates.extend(date_vector)
                if day_manual > 0:
                    break
            except ValueError:
                continue

        Y = np.hstack(inactivity_anomaly_vectors)

        unexpected_anomalies_count = 0
        current_anomaly = []
        unexpected_anomalies = []
        min_anomaly_length = 5

        for k, y in enumerate(Y):
            if y >= 3:
                unexpected_anomalies_count += 1
                current_anomaly.append(dates[k])
            else:
                if unexpected_anomalies_count >= min_anomaly_length:
                    anomaly_range = \
                        [
                            current_anomaly[0],
                            current_anomaly[-1],
                        ]

                    unexpected_anomalies.append(anomaly_range)

                current_anomaly = []
                unexpected_anomalies_count = 0


        if visualize:
            unexpected_anomalies_str = [[pd.to_datetime(str(x)) .strftime('%Y-%m-%d %H:%M:%S') for x in r] for r in unexpected_anomalies]
            visualize_household(group, first, last, unexpected_anomalies_str)

        num_columns = len(group.columns)

        group['isAnomaly'] = 0
        group['anomalyType'] = 'None'
        for start, end in unexpected_anomalies:
            b = np.logical_and(start <= group.index, group.index <= end)
            idx, = np.where(b)

            group.iloc[idx.tolist(), num_columns] = 1
            group.iloc[idx.tolist(), num_columns + 1] = 'lowActivity'

        new_data.append(group)

    new_df = pd.concat(new_data)
    # new_df = new_df.reset_index()
    new_df.to_csv(output_file)


detect_anomalies('data/hackathon_EnBW_smart_meter_data_9_hh_anomalies.csv', 'team-a.csv',
                 True)
