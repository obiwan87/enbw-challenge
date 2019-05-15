import statsmodels.api as sm

from utils.io import read_enbw_dataset

data = read_enbw_dataset('data/hackathon_EnBW_smart_meter_data_30_hh.csv')

groups = data.groupby(data.id)
group = groups.get_group(1)
group.set_index(group.timestampLocal, inplace=True)
group = group.resample('H').mean()
group.dropna(inplace=True)
res = sm.tsa.seasonal_decompose(group.value)
resplot = res.plot()