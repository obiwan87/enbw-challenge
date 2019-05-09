import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

data = pd.read_csv("data/data-sonne.csv", delimiter=',')
data['timestampLocal'] = pd.to_datetime(data.timestampLocal)

data.dropna()
feiertage = pd.read_csv("additional_data/feiertage.csv")

# sonne = pd.read_csv("additional_data/sonnenstunden.csv")
# sonne.set_index(sonne.date, inplace=True)
#
# def getSun(date):
#     if pd.notnull(date):
#         datum = date.strftime("%m-%d")
#         datum2 = date.strftime("%Y-%m-%d")
#         daten = sonne.loc[datum, :]
#
#         start = daten.loc["start"]
#         end = daten.loc["end"]
#
#         start = datetime.strptime(datum2 + " " + start, '%Y-%m-%d %I:%M:%S %p')
#         end = datetime.strptime(datum2 + " " + end, '%Y-%m-%d %I:%M:%S %p')
#         if start < date < end:
#             #print(date)
#             return 1
#         else:
#             #print(date)
#             return 0
#     else:
#         #print('fehler')
#         return -1
#
#
# data["sun"] = data["timestampLocal"].apply(getSun)
# data.to_csv('data/data-sonne.csv')

unique_dates = feiertage["Datum"].unique()


def isHoliday(date):
    if pd.notnull(date):
        datum = date.strftime("%Y-%m-%d")

        is_weekend = date.isoweekday() >= 6
        is_holiday = datum in unique_dates

        if is_holiday:
            return 1
        elif is_weekend:
            return 2
        else:
            return 0
    else:
        return -1


data["holiday"] = data["timestampLocal"].apply(isHoliday)
data.to_csv('data/data-sonne-feiertage.csv')
