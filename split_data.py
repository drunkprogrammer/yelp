import pandas as pd
import os
import numpy as np
from mxnet import gluon, np
import matplotlib.pyplot as plt

def read_data_yelp2013(filename):
    names = ['user_id', 'item_id', 'rating']
    data = pd.read_csv(filename, skiprows=1, names=names,
                       engine='python')
    num_users = data.user_id.unique().shape[0]
    num_items = data.item_id.unique().shape[0]
    return data, num_users, num_items

def split_data_yelp2013(data, test_ratio=0.1):

    mask = [True if x == 1 else False for x in np.random.uniform(
        0, 1, (len(data))) < 1 - test_ratio]
    neg_mask = [not x for x in mask]
    train_data, test_data = data[mask], data[neg_mask]

    return train_data, test_data

def load_data_yelp2013(data, num_users, num_items, feedback='explicit'):
    users, items, scores = [], [], []
    inter = np.zeros((num_items, num_users)) if feedback == 'explicit' else {}
    for line in data.itertuples():
        user_index, item_index = int(line[1] - 1), int(line[2] - 1)
        score = int(line[3]) if feedback == 'explicit' else 1
        users.append(user_index)
        items.append(item_index)
        scores.append(score)
        if feedback == 'implicit':
            inter.setdefault(user_index, []).append(item_index)
        else:
            inter[item_index, user_index] = score
    return users, items, scores, inter

def split_and_load_yelp2013(feedback='explicit',
                          test_ratio=0.1, batch_size=256, filename=""):
    data, num_users, num_items = read_data_yelp2013(filename)
    train_data, test_data = split_data_yelp2013(
        data, test_ratio)
    train_u, train_i, train_r, _ = load_data_yelp2013(
        train_data, num_users, num_items, feedback)
    test_u, test_i, test_r, _ = load_data_yelp2013(
        test_data, num_users, num_items, feedback)
    train_set = gluon.data.ArrayDataset(
        np.array(train_u), np.array(train_i), np.array(train_r))
    test_set = gluon.data.ArrayDataset(
        np.array(test_u), np.array(test_i), np.array(test_r))
    train_iter = gluon.data.DataLoader(
        train_set, shuffle=True, last_batch='rollover',
        batch_size=batch_size)
    test_iter = gluon.data.DataLoader(
        test_set, batch_size=batch_size)
    return num_users, num_items, train_iter, test_iter

filename = './data/csv/yelp-2013-rating-matrix.csv'
data, num_users, num_items = read_data_yelp2013(filename)
sparsity = 1 - len(data) / (num_users * num_items)
print(len(data))
print(f'number of users: {num_users}, number of items: {num_items}')
print(f'matrix sparsity: {sparsity:f}')
print(data.head(5))
print(num_users)
print(num_items)

# plt.hist(data['rating'], bins=5, ec='black')
# plt.xlabel('Rating')
# plt.ylabel('Count')
# plt.title('Distribution of Ratings in Yelp2013')
# plt.show()

# train_data, test_data = split_data_yelp2013(data)
# print(train_data)
# print(test_data)

num_users, num_items, train_iter, test_iter = split_and_load_yelp2013(feedback='explicit',test_ratio=0.1, batch_size=256, filename=filename)
print(num_users)
print(num_items)
print(train_iter)
print(test_iter)