import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from utils.io import read_enbw_dataset

data = read_enbw_dataset('data/data-sun-holidays.csv')

groups = data.groupby('id')

group = groups.get_group(1)
group.set_index(group.timestampLocal, inplace=True)
group.value.plot()