import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print('hello world')






data = pd.read_csv("hackathon_EnBW_smart_meter_data_30_hh.csv", delimiter=';')

g1 = sns.pointplot(x="timestampLocal", y="value", hue = "id", data = data)

data = pd.read_csv("hackathon_EnBW_smart_meter_data_30_hh.csv", delimiter=';')
data['timestampLocal'] = pd.to_datetime(data.timestampLocal)
data.set_index(data.timestampLocal,inplace = True)
data.dropna()
feiertage = pd.read_csv("https://www.spiketime.de/feiertagapi/feiertage/csv/2014/2018", delimiter=';')

sonne = pd.read_csv("sonnenaufgang.csv",delimiter=";")

date = "01-11"


def getStart(date):
    sun = pd.read_json("https://api.sunrise-sunset.org/json?lat=48.776778&lng=-9.175148&&date=2012-"+date)
    sunrise = sun["results"].loc["civil_twilight_begin"]
    print(sunrise)
    return sunrise

def getEnd(date):
    sun = pd.read_json("https://api.sunrise-sunset.org/json?lat=48.776778&lng=-9.175148&&date=2012-"+date)
    sunset = sun["results"].loc["civil_twilight_end"]
    print(sunset)
    return sunset


sonne["start"]=sonne["date"].apply(getStart)
sonne["end"] = sonne["date"].apply(getEnd)

def getSun(date):
    if pd.notnull(date):
        datum = date.strftime("%m-%d")
        datum2 = date.strftime("%Y-%m-%d")
        daten = sonne[sonne.date == datum].iloc[0]

        start = daten.loc["start"]
        end = daten.loc["end"]

        start = datetime.strptime(datum2+" "+start, '%Y-%m-%d %I:%M:%S %p')
        end = datetime.strptime(datum2+" "+end, '%Y-%m-%d %I:%M:%S %p')
        if date > start and date < end:
            print(date)
            return 1
        else:
            print(date)
            return 0
    else:
        print(fehler)
        return 2



data["sun"] = data["timestampLocal"].apply(getSun)
