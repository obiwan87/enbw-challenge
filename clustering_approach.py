import datetime

import numpy as np
from scipy.spatial.distance import pdist

from sklearn.cluster import DBSCAN, KMeans
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import normalize

from utils.io import read_enbw_dataset

TOTAL_DAYS_YEAR = 365

data = read_enbw_dataset('data/hackathon_EnBW_smart_meter_data_30_hh.csv')

groups = data.groupby('id')

group_id = 3
group = groups.get_group(group_id)

window_sizes = [4, 6, 8]
group = group.set_index(group.timestampLocal)

grouped_by_day = group.groupby(lambda x: x.dayofyear)

selected_features = []
day_vectors = []
for key, day_data in grouped_by_day:
    resampled = day_data.resample('2H').value.mean()
    day_vector = resampled.values

    day_vectors.append(day_vector)
    #print(resampled)


# group['day_of_year'] = group.index.dayofyear / TOTAL_DAYS_YEAR

# s = slice(400, 1000)
X = np.vstack(day_vectors)
# X = normalize(X)
# X = group.loc[:, selected_features].dropna().values

# X = X[s, :]
# X = stats.zscore(X)
d = pdist(X, metric='correlation')

sns.distplot(d)
#
clustering_algorithm = DBSCAN(min_samples=4, eps=0.08, metric='correlation')
clustering = clustering_algorithm.fit(X)
clustering_labels = clustering.labels_

print(clustering_labels)

unique_clusters = np.unique(clustering_labels)

year = 2014
for cluster in unique_clusters:
    print('Cluster %i' % cluster)
    print('-' * 20)
    b = clustering_labels == cluster
    vectors_cluster = X[b]
    days,  = np.where(b)
    n = np.ceil(np.sqrt(len(days)))
    # plt.figure()
    for i, day in enumerate(days):
        # plt.subplot(n, n, i+1)
        current_date = datetime.datetime(year, 1, 1) + datetime.timedelta(int(day))
        # vector = X[day]
        whole_day = grouped_by_day.get_group(day+1)
        vector = whole_day.value.values

        # plt.plot(vector)

        date_string = current_date.strftime('%d.%m., %A')
        # plt.title(date_string)
        print(date_string)
    print('-' * 20)
    plt.show()


# df = pd.DataFrame(data=X, columns=selected_features)
# df['label'] = clustering.labels_
# df.reset_index(inplace=True)
# sns.lmplot(x='index', y=selected_features[0], hue='label', data=df, fit_reg=False)