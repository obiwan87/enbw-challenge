import pandas as pd
import numpy as np

from utils.io import read_enbw_dataset

data_filepath = 'data/hackathon_EnBW_smart_meter_data_30_hh.csv'
data = read_enbw_dataset(data_filepath)


data_set_range = pd.date_range(start='2014-01-01 00:00', )
