import plotly
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


def str2float(x):
    return float(x.replace(',', '.'))


def visualize_household(id, start_date, end_date, anomaly_list):

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

    print(g)

    y = g['value'].values
    y_holiday = g['holiday'].values

    x = g['timestampLocal'].values

    #fig, ax1 = plt.subplots()
    #ax2 = ax1.twinx()

    plt.plot(x, y, 'g-', zorder=1)
    #ax1.plot(x,y_anomaly, 'r-')
    #ax2.plot(x, y_holiday, 'b-')

    for a in anomaly_list:
        plt.axvspan(xmin=a[0], xmax = a[1], facecolor='r', alpha=0.5, zorder=2)


    plt.show()




anomaly_list = [['2014-01-10 00:00:00', '2014-01-21 00:00:00'],
                ['2014-02-10 00:00:00', '2014-02-21 00:00:00']]

visualize_household(3, '2014-01-01 00:00:00', '2014-12-31 00:00:00', anomaly_list)








