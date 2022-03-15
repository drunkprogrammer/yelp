from read_file import read_file
from collections import defaultdict
import numpy as np

def mapping_users_products_labels(datasets):

    users_ids = set()
    products_ids = set()


    user_map_products = defaultdict(lambda: defaultdict(list))

    ATTR_MAP = {
        'user': int(0),
        'product': int(1),
        'label': int(3),
    }
    for document in datasets:
        product_id = document[ATTR_MAP["product"]]
        user_id = document[ATTR_MAP["user"]]
        products_ids.add(product_id)
        users_ids.add(user_id)

    users_ids_dict = {k: v for v, k in enumerate(users_ids)}
    products_ids_dict = {k: v for v, k in enumerate(products_ids)}

    for document in datasets:
        product_id = products_ids_dict[document[ATTR_MAP["product"]]]
        user_id = users_ids_dict[document[ATTR_MAP["user"]]]
        label = document[ATTR_MAP["label"]]
        user_map_products[user_id][product_id].append(label) # build the mapping matrix about the {user{product{label}}}

    return user_map_products, users_ids_dict, products_ids_dict

def non_zero_mean(np_arr):
    exist = (np_arr != 0)
    num = np_arr.sum(axis=0)
    den = exist.sum(axis=0)
    return num/den

def build_user_product_rating_matrix(user_map_products, users_ids_dict, products_ids_dict):
    row_num = len(users_ids_dict)
    column_num = len(products_ids_dict)
    upr_matrix = np.matrix(np.zeros((row_num, column_num)))

    for k1, v1 in user_map_products.items():
        for k2, v2 in v1.items():
            upr_matrix[k1, k2] = sum(v2)/len(v2)

    # use the product average rating to implement the zero scores
    # avg_column = non_zero_mean(upr_matrix)
    # for r in range(row_num):
    #     for c in range(column_num):
    #         if upr_matrix[r, c] == 0:
    #              upr_matrix[r, c] = avg_column[0, c]

    #use np.Nan to implement the zero scores
    # for r in range(row_num):
    #     for c in range(column_num):
    #         if upr_matrix[r, c] == 0:
    #              upr_matrix[r, c] = np.NAN


    return upr_matrix

documents_train = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')
user_map_products, users_ids_dict, products_ids_dict = mapping_users_products_labels(documents_train)
upr_matrix = build_user_product_rating_matrix(user_map_products, users_ids_dict, products_ids_dict)
# print(user_map_products[1497][108]) # [1497, 108, 5]
# print(upr_matrix[1437])#1549, 800, 19