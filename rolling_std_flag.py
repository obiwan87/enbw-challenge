import plotly
import plotly.graph_objs as go
import numpy as np

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

def str2float(x):
    return float(x.replace(',', '.'))


def get_low_std_windows(data, resample_dim, window_mean, window_std):
    id = data['id'].iloc[0]
    data = data.set_index('timestampLocal')
    data = data.resample(resample_dim).agg({'value': np.sum, 'id': np.mean, 'sun': np.mean, 'holiday': np.mean})

    data['rolling_4'] = data['value'].rolling(window=window_mean, center=True).mean()
    data['std_12'] = data['value'].rolling(window=window_std, center=True).std()

    #data['score'] = 1 / (data['std_12'] * data['rolling_4'])
    data['score'] = 1 / data['std_12']
    data.score[data['rolling_4'] == 0] = 0

    quantile = data['score'].quantile(0.95)
    median = data['score'].median()
    std = data['score'].std()
    threshold = median + 2.5 * std

    data['anomaly_flag'] = data['score'] > threshold
    data['anomaly_flag'] = data['anomaly_flag'].astype(int)

    return data



df = pd.read_csv("data/data-sun-holidays.csv", sep=';', na_values = ['NA'], converters = {'value': str2float})
df['timestampLocal'] = pd.to_datetime(df.timestampLocal)

grouped = df.groupby("id")

g = grouped.get_group(2)
g_new = get_low_std_windows(g, "h", 4, 20)
print(g_new)
