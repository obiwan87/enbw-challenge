import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta


def str2float(x):
  return float(x.replace(',', '.'))
data = pd.read_csv("data-sun-holidays.csv", sep=';', na_values = ['NA'], converters = {'value': str2float})
data['timestampLocal'] = pd.to_datetime(data.timestampLocal)
data.describe()

datum = datetime.strptime("2014-06-28","%Y-%m-%d")


def lprofile (start,days, nid, data):
   if nid in data["id"]:
       data = data[data.id==nid]
       end = start + timedelta(days=days)
       mask = (data['timestampLocal'] > start) & (data['timestampLocal'] <= end)
       data = data.loc[mask]
       #data['weekday'] = data['timestampLocal'].dt.weekday_name()
       ax = sns.lineplot(x="timestampLocal", y="value", data=data)
       ax = plt.gca()
       # get current xtick labels
       xticks = ax.get_xticks()
       ax.set_xticklabels([pd.to_datetime(tm, unit='ms').strftime('%Y-%m-%d\n %H:%M:%S') for tm in xticks],
                 rotation=50)
       #ax2 = ax.twinx()
       #sns.lineplot(x="weekday", y="value", ax=ax2, data=data)
       #plt.xticks(np.arange(start, end, 5))
       return plt.show()
   else:
       return print("user or day not available")

lprofile(start,5,2,data)