import datetime

import pandas as pd
import sklearn
import numpy as np
from scipy.spatial.distance import pdist

from sklearn.cluster import DBSCAN, KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from sklearn.preprocessing import normalize

from utils.io import read_enbw_dataset

TOTAL_DAYS_YEAR = 365

data = read_enbw_dataset('data/hackathon_EnBW_smart_meter_data_30_hh.csv')

groups = data.groupby('id')

group = groups.get_group(9)
timeslice = group.iloc[3600:8000, :]
timeslice.dropna(inplace=True)

timeslice.value.plot()
timeslice.set_index(timeslice.timestampLocal, inplace=True)
timeslice = timeslice.resample('1H').mean()
timeslice_groups = timeslice.groupby(lambda x: x.dayofyear)

plt.figure()
timeslice['value'].rolling(window=100).mean().plot()

plt.figure()
timeslice.value.plot()
quantiles = timeslice.quantile([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.6, 0.8, 0.9, 1])
