import pandas as pd
from read_file import read_file_user_product_rating
from collections import defaultdict
import csv
import numpy as np

def save_rating_history_csv(rfilename, wfilename1, wfilename2):
    header1 = ["User", "User ID", "Product", "Product ID", "Rating"]
    header2 = ["User ID", "Product ID", "Rating"]
    documents, users, products = read_file_user_product_rating(rfilename)
    users2idx = {o: i for i, o in enumerate(users)}
    products2idx = {o: i for i, o in enumerate(products)}
    user_map_products = defaultdict(lambda: defaultdict(list))
    with open(wfilename1, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header1)
        for document in documents:
            product_id = products2idx[document[1]]
            user_id = users2idx[document[0]]
            label = document[2]
            user_map_products[user_id][product_id].append(label)
            writer.writerow([document[0], user_id, document[1], product_id, label])

    row_num = len(users2idx)
    column_num = len(products2idx)
    print(row_num)
    print(column_num)
    upr_matrix = defaultdict()

    for k1, v1 in user_map_products.items():
        for k2, v2 in v1.items():
            upr_matrix[k1, k2] = sum(v2)/len(v2)

    product_user_id = defaultdict()
    with open(wfilename2, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header2)
        for document in documents:
            product_id = products2idx[document[1]]
            user_id = users2idx[document[0]]
            if (user_id, product_id) not in product_user_id:
                writer.writerow([user_id, product_id, upr_matrix[(user_id, product_id)]])
                product_user_id[user_id, product_id] = upr_matrix[(user_id, product_id)]


rfilename = './data/yelp_13/yelp-2013-seg-20-20.train.ss'
wfilename1 = './data/csv/yelp-2013-rating-history.csv'
wfilename2 = './data/csv/yelp-2013-rating-matrix.csv'
# save the user-item-rating to the csv file
save_rating_history_csv(rfilename, wfilename1, wfilename2)