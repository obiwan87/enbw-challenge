import plotly
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


def str2float(x):
    return float(x.replace(',', '.'))


def visualize_household(id, start_date, end_date, anomaly_start, anomaly_end):

    df = pd.read_csv("data/data-sun-holidays.csv", sep=';', na_values=['NA'], converters={'value': str2float})
    df['timestampLocal'] = pd.to_datetime(df.timestampLocal)

    # print(df.isnull().sum())
    # print(df[df.timestampLocal.isnull()])

    grouped = df.groupby('id')

    data_list = []

    g = grouped.get_group(id)
    g.set_index('timestampLocal')

    g.dropna(inplace=True)

    g = g.dropna()
    g['time'] = [d.time() for d in g['timestampLocal']]
    g['date'] = [d.date() for d in g['timestampLocal']]

    # time range
    g['timestampLocal'] = pd.to_datetime(g['timestampLocal'])
    g = g[(g['timestampLocal'] > start_date) & (g['timestampLocal'] < end_date)]
    g['anomaly'] = 0
    g.anomaly[(g['timestampLocal'] > anomaly_start) & (g['timestampLocal'] < anomaly_end)] = 1
    g.anomaly = g.anomaly * g.value

    print(g)

    y = g['value'].values
    y_holiday = g['holiday'].values
    y_anomaly = g['anomaly'].values

    x = g['timestampLocal'].values

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x, y, 'g-')
    ax1.plot(x,y_anomaly, 'r-')
    ax2.plot(x, y_holiday, 'b-')

    plt.show()

visualize_household(3, '2014-01-01 00:00:00', '2014-12-31 00:00:00', '2014-01-20 00:00:00', '2014-01-21 00:00:00')








