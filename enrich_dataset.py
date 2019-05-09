import pandas as pd
import numpy as np

holidays = pd.read_csv('additional_data/feiertage.csv')
sun = pd.read_csv('additional_data/sonnenstunden.csv')


pd.to_datetime(sun.start)