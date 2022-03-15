import numpy as np
import numpy.ma as ma
import pandas as pd
from read_file import read_file
from build_user_product_rating_matrix import mapping_users_products_labels, build_user_product_rating_matrix
from read_rating_matrix import read_sparse_rating_matrix, read_sparse_rating_matrix_from_txt

def calculate_peason_coffecient_matrix():
    # calculate the peason coffecient matrix
    documents_train = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')
    user_map_products, users_ids_dict, products_ids_dict = mapping_users_products_labels(documents_train)
    upr_matrix = build_user_product_rating_matrix(user_map_products, users_ids_dict, products_ids_dict)

    upr_matrix_transpose = pd.DataFrame(upr_matrix.transpose())
    R1 = upr_matrix_transpose.corr()

    return R1


def calculate_peason_coffecient_matrix_from_csv():
    # calculate the peason coffecient matrix
    filename = './data/csv/yelp-2013-rating-prediction-matrix.csv'
    upr_matrix = read_sparse_rating_matrix(filename)
    upr_matrix_transpose = pd.DataFrame(upr_matrix.transpose())
    R1 = upr_matrix_transpose.corr()

    return R1

def calculate_peason_coffecient_matrix_from_txt():
    # calculate the peason coffecient matrix
    filename = './data/csv/yelp-2013-rating-prediction-matrix.txt'
    upr_matrix = read_sparse_rating_matrix_from_txt(filename)
    upr_matrix_transpose = pd.DataFrame(upr_matrix.transpose())
    R1 = upr_matrix_transpose.corr()

    return R1

# # R1 = np.corrcoef(ma.masked_invalid(upr_matrix))
# print(R1)

"""
cosine similarity
"""

"""
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

A_sparse = sparse.csr_matrix(upr_matrix)

similarities = cosine_similarity(A_sparse)
print('pairwise dense output:\n {}\n'.format(similarities))

#also can output sparse matrices
similarities_sparse = cosine_similarity(A_sparse,dense_output=False)
print('pairwise sparse output:\n {}\n'.format(similarities_sparse))
"""
