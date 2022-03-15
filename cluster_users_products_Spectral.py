import numpy as np
import numpy.ma as ma
import pandas as pd
from read_file import read_file
from build_user_product_rating_matrix import mapping_users_products_labels, build_user_product_rating_matrix
from calculate_similarity_matrix import calculate_peason_coffecient_matrix, calculate_peason_coffecient_matrix_from_csv,calculate_peason_coffecient_matrix_from_txt
from matplotlib import pyplot as plt
from sklearn.cluster import SpectralClustering, KMeans
from collections import Counter, defaultdict
from save_clustering_csv import save_clustering_result_to_csv, save_clustering_users_to_csv

def build_lapacian_matrix(matrix):
    vectorizer = np.vectorize(lambda x: 1 if x > 0.5 else 0)
    # build the adjacency matrix
    adj_matrix = np.vectorize(vectorizer)(matrix)
    # build the degree matrix
    deg_matrix = np.diag(np.sum(adj_matrix, axis=1))
    # build lapacian matrix
    lap_matrix = deg_matrix - adj_matrix

    return adj_matrix, lap_matrix

def cluster_users_products_spectral():
    matrix = calculate_peason_coffecient_matrix_from_txt()
    adj_matrix, lap_matrix = build_lapacian_matrix(matrix)
    e, v = np.linalg.eig(lap_matrix)
    return matrix, adj_matrix, lap_matrix, e, v

def plot_eigenvalues_eigenvector(e,v):
    fig = plt.figure(figsize=[18, 6])

    ax1 = plt.subplot(221)
    plt.plot(e)
    ax1.title.set_text('eigenvalues')

    i = np.where(e < 25)[0]
    ax2 = plt.subplot(222)
    plt.plot(v[:, i[0]])

    ax3 = plt.subplot(223)
    plt.plot(v[:, i[1]])
    ax3.title.set_text('second eigenvector with eigenvalue close to 0')

    # ax4 = plt.subplot(224)
    # plt.plot(v[:, i[2]])
    # ax4.title.set_text('third eigenvector with eigenvalue close to 0')

    fig.tight_layout()
    plt.show()

def save_cluster_dict(labels):

    cluster_class_result = defaultdict(list)

    for k, v in enumerate(labels):
        cluster_class_result[v].append(k)

    save_clustering_result_to_csv(cluster_class_result)
    save_clustering_users_to_csv(list(labels))


matrix, adj_matrix, lap_matrix, e, v = cluster_users_products_spectral()
# # print(e)
# plot_eigenvalues_eigenvector(e,v)
# print(lap_matrix)

# k-means clustering
# i = np.where(e < 25)[0]
# U = np.array(v[:, i[1]])
# km = KMeans(init='k-means++', n_clusters=3)
# km_clustering = km.fit(U.reshape(-1,1))
# label = km_clustering.labels_
# print(km_clustering.labels_)
# numbers = np.unique(label, return_counts=True)
# print(numbers)

# spectral clustering
# i = np.where(e < 25)[0]
# U = np.array(v[:, i[0]])
delta = 0.5

# sparse matrix contain Nan
distance_matrix = - matrix
distance_matrix = distance_matrix.where(distance_matrix == np.nan, -1)
# print(distance_matrix)
U = np.exp(- distance_matrix ** 2 / (2. * delta ** 2))

sc = SpectralClustering(n_clusters=40, affinity='nearest_neighbors', random_state=0)
# sc = SpectralClustering(n_clusters=8, affinity='precomputed', random_state=0)
# sc = SpectralClustering(n_clusters=8, affinity='rbf', random_state=0)
sc_clustering = sc.fit(U)
print(U)
labels = sc_clustering.labels_
# print(sc_clustering.labels_)
numbers = np.unique(labels, return_counts=True)
print(labels)
save_cluster_dict(labels)
# print(numbers)
# print(numbers[0])
# print(numbers[1])
# print(sum(numbers[1]))

# plt.title(f'Spectral clustering results ')
# plt.scatter(U[:, 0], U[:, 1], s=50, c = label);

#plt.scatter(lap_matrix[:,0], lap_matrix[:,1], c=km_clustering.labels_, cmap='rainbow', alpha=0.7, edgecolors='b')