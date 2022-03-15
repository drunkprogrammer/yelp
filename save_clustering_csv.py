import csv
from read_file import read_file_user_mapping_id, read_file_user_cluster

def save_clustering_result_to_csv(cluster_results):
    # cluster; cluster value

    wfilename1 = './data/csv/yelp-2013-cluster-results.csv'
    # header = ["Cluster " + str(i) for i in range(1, 41)]   # cluster 1, cluster 2, ... cluster 40
    header = ["Cluster", "Users ID"]

    with open(wfilename1, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for key, value in cluster_results.items():
            writer.writerow([key, value])
            print(key, value)

    f.close()

def save_clustering_users_to_csv(cluster_user_results, user_mapping):
    # user id; user; cluster_number

    wfilename2 = './data/csv/yelp-2013-cluster-user-id-results.csv'
    header = ["User ID", "User", "Cluster"]

    with open(wfilename2, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for u, c in cluster_user_results.items():
            writer.writerow([u, user_mapping[u], c])
            print(u, user_mapping[u], c)

        f.close()

# cluster_results = {
#     1: [3, 4, 5],
#     2: [6, 7, 8]
# }
#
# cluster_user_results = [1, 2, 4, 3, 4]
# save_clustering_result_to_txt(cluster_results)
rfilename1 = './data/csv/yelp-2013-rating-history.csv'
rfilename2 = './data/csv/yelp-2013-cluster-user-results.csv'
user_mapping = read_file_user_mapping_id(rfilename1)
cluster_user_results = read_file_user_cluster(rfilename2)
save_clustering_users_to_csv(cluster_user_results, user_mapping)

# wfilename1 = ""