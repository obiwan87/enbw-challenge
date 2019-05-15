import pandas as pd
import sklearn
import numpy as np
import matplotlib.cm as cm
from scipy.spatial.distance import pdist
from sklearn.cluster import DBSCAN
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

from utils.io import read_enbw_dataset

TOTAL_DAYS_YEAR = 365

data = read_enbw_dataset('data/hackathon_EnBW_smart_meter_data_30_hh.csv')

groups = data.groupby('id')

group_id = 9
group = groups.get_group(group_id)

window_sizes = [16, 24, 32]
group = group.set_index(group.timestampLocal)
group = group.resample('2h').sum()
for window_size in window_sizes:
    group['mean_' + str(window_size)] = group['value'].rolling(window=window_size).mean()
    group['std_' + str(window_size)] = group['value'].rolling(window=window_size).std()

group['day_of_year'] = group.index.dayofyear / TOTAL_DAYS_YEAR

selected_features = [ 'mean_16', 'std_16', 'mean_24', 'std_24', 'mean_32', 'std_32']
s = slice(400, 1000)
X = group.loc[:, selected_features].dropna().values

X = X[s, :]
X = stats.zscore(X)
d = pdist(X)

sns.distplot(d)

clustering_algorithm = DBSCAN(eps=0.1, min_samples=2)
clustering = clustering_algorithm.fit(X)
clustering_labels = clustering.labels_
print(clustering_labels)

df = pd.DataFrame(data=X, columns=selected_features)
df['label'] = clustering_labels
df.reset_index(inplace=True)
sns.lmplot(x='index', y='mean_16', hue='label', fit_reg=False, data=df)

plt.figure()
plt.plot(df['mean_16'].values)

unique_clusters = np.unique(clustering_labels)
points = df['mean_16'].values
x = np.arange(10)
ys = [i+x+(i*x)**2 for i in range(len(unique_clusters))]
colors = iter(cm.rainbow(np.linspace(0, 1, len(ys))))
for cluster in unique_clusters:
    cluster_points_indices, = np.where(clustering_labels == cluster)
    plt.scatter(x=cluster_points_indices, y=points[cluster_points_indices], color=next(colors))