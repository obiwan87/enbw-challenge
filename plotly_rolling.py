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


df = pd.read_csv("data/hackathon_EnBW_smart_meter_data_30_hh.csv", sep=';', na_values = ['NA'], converters = {'value': str2float})
df['timestampLocal'] = pd.to_datetime(df.timestampLocal)

#print(df.isnull().sum())
#print(df[df.timestampLocal.isnull()])


grouped = df.groupby("id")

data_list = []

for n, g in grouped:
    id = g['id'].iloc[0]
    #print(id)
    g = g.set_index('timestampLocal')
    g = g.resample("h").sum()

    g['rolling_4'] = g['value'].rolling(window = 4).mean()
    g['std_12'] = g['value'].rolling(window = 20, center = True).std()
    #print(g)

    g['index'] = range(1,len(g)+1)
    print(g)
    g.set_index('index')

    graph_data = go.Scatter(
        x=g['index'].values,
        #x = g['timestampLocal'],
        y=g['value'].values,
        name= 'Haushalt' + str(id),
        line=dict(
            color=('blue'),
            width=2)
    )

    graph_data_rolling = go.Scatter(
        x=g['index'].values,
        # x = g['timestampLocal'],
        y=g['rolling_4'].values,
        name='Haushalt rolling' + str(id),
        line=dict(
            color=('red'),
            width=2)
    )

    graph_data_std = go.Scatter(
        x=g['index'].values,
        # x = g['timestampLocal'],
        y=g['std_12'].values,
        name='Haushalt rolling' + str(id),
        line=dict(
            color=('black'),
            width=2)
    )

    data_list.append(graph_data)

    layout = dict(
        xaxis=dict(title='Date-Time'),
        yaxis=dict(title='Watt'),
        showlegend=True,
    )

    data = [graph_data_rolling, graph_data_std]

    if id == 6:

        fig = dict(data=data, layout=layout)
        plotly.offline.plot(fig, auto_open=True, include_plotlyjs=True)
        break;