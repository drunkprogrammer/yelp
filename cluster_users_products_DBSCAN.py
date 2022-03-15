import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import tools
from plotly.subplots import make_subplots
import plotly.offline as py
import plotly.express as px
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from read_file import read_file
from build_user_product_rating_matrix import mapping_users_products_labels, build_user_product_rating_matrix

plt.style.use('fivethirtyeight')
from warnings import filterwarnings
filterwarnings('ignore')

documents_train = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')

user_map_products, users_ids_dict, products_ids_dict = mapping_users_products_labels(documents_train)
upr_matrix = build_user_product_rating_matrix(user_map_products, users_ids_dict, products_ids_dict)

df = upr_matrix

scaler = StandardScaler()
scaler.fit(df)
X_scale = scaler.transform(df)
df_scale = pd.DataFrame(X_scale)
print(df_scale.head())

pca = PCA(n_components=3)
pca.fit(df_scale)
pca_scale = pca.transform(df_scale)
pca_df = pd.DataFrame(pca_scale)
# pca_df = pd.DataFrame(pca_scale, columns=['pc1', 'pc2', 'pc3'])
print(pca.explained_variance_ratio_)


km = KMeans(
    n_clusters=12, init='random',
    n_init=10, max_iter=300,
    tol=1e-04, random_state=0
)
y_km = km.fit(pca_df)

Scene = dict(xaxis=dict(title='PC1'), yaxis=dict(title='PC2'), zaxis=dict(title='PC3'))
labels = y_km.labels_
trace = go.Scatter3d(x=pca_df.iloc[:, 0], y=pca_df.iloc[:, 1], z=pca_df.iloc[:, 2], mode='markers', marker=dict(color=labels, colorscale='Viridis', size = 10, line = dict(color = 'gray',width = 5)))
layout = go.Layout(scene=Scene, height=1000, width=1000)
data = [trace]
fig = go.Figure(data=data, layout = layout)
fig.update_layout(title='KMeans clusters Derived from PCA', font=dict(size=12,))
fig.show()
numbers = np.unique(labels, return_counts=True)
print(numbers)

# Scene = dict(xaxis=dict(title='PC1'), yaxis=dict(title='PC2'), zaxis=dict(title='PC3'))
# trace = go.Scatter3d(x=pca_df.iloc[:, 0], y=pca_df.iloc[:, 1], z=pca_df.iloc[:, 2], mode='markers', marker=dict(colorscale ='Greys', opacity=0.3, size = 10, ))
# layout = go.Layout(margin=dict(l=0, r=0), scene=Scene, height=1000, width=1000)
# data = [trace]
# fig = go.Figure(data=data, layout=layout)
# fig.show()
#
# plt.figure(figsize=(10,5))
# nn = NearestNeighbors(n_neighbors=5).fit(pca_df)
# distances, idx = nn.kneighbors(pca_df)
# distances = np.sort(distances, axis=0)
# distances = distances[:,1]
# plt.plot(distances)
# plt.show()

# db = DBSCAN(eps=0.8, min_samples=4).fit(pca_df)
# labels = db.labels_
# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# n_noise_ = list(labels).count(-1)
# print('Estimated number of clusters: %d' % n_clusters_)
# print('Estimated number of noise points: %d' % n_noise_)
# print("Silhouette Coefficient: %0.3f" % silhouette_score(pca_df, labels))
#
# numbers = np.unique(labels, return_counts=True)
# print(numbers)
# Scene = dict(xaxis=dict(title='PC1'), yaxis=dict(title='PC2'), zaxis=dict(title='PC3'))
# labels = db.labels_

# trace = go.Scatter3d(x=pca_df.iloc[:, 0], y=pca_df.iloc[:, 1], z=pca_df.iloc[:, 2], mode='markers', marker=dict(color=labels, colorscale='Viridis', size = 10, line = dict(color = 'gray',width = 5)))
# layout = go.Layout(scene=Scene, height=1000, width=1000)
# data = [trace]
# fig = go.Figure(data=data, layout = layout)
# fig.update_layout(title='DBSCAN clusters (53) Derived from PCA', font=dict(size=12,))
# fig.show()