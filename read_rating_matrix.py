import pandas as pd
import numpy as np

def read_sparse_rating_matrix(filename):
    names = ['user_id', 'item_id', 'rating']
    data = pd.read_csv(filename, skiprows=1, names=names,
                       engine='python')
    u_uniq = data.user_id.unique()
    i_uniq = data.item_id.unique()
    row_num = len(u_uniq)
    column_num = len(i_uniq)
    upr_matrix = np.matrix(np.zeros((row_num, column_num)))

    for row in data.iterrows():
        index = row[0]
        u = row[1][0]
        i = row[1][1]
        r = row[1][2]
        # r = row[2]
        upr_matrix[int(u), int(i)] = r
       # print(u, i, r)

    return upr_matrix

def read_sparse_rating_matrix_from_txt(filename):
    names = ['user_id', 'item_id', 'rating']
    data = pd.read_csv(filename, names=names, sep="  ", header=None, engine='python')
    u_uniq = data.user_id.unique()
    i_uniq = data.item_id.unique()
    row_num = len(u_uniq)
    column_num = len(i_uniq)
    upr_matrix = np.matrix(np.zeros((row_num, column_num)))

    for row in data.iterrows():
        u = row[1][0]
        i = row[1][1]
        r = row[1][2]
        upr_matrix[int(u), int(i)] = float(r)

    return upr_matrix

# rfilename1 = './data/csv/yelp-2013-rating-matrix.csv'
# rfilename1 = './data/csv/yelp-2013-rating-prediction-matrix.txt'
# upr_matrix = read_sparse_rating_matrix_from_txt(rfilename1)
# print(np.nonzero(upr_matrix))