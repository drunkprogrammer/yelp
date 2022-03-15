import pandas as pd
from collections import Counter, defaultdict

def read_file(dataset):
    pd_reader = pd.read_csv(dataset, header=None, skiprows=0, encoding="utf-8", sep='\t\t', engine='python')
    print("total number:")
    print(len(pd_reader[0]))
    documents = []
    for i in range(len(pd_reader[0])):
        # if i == 100:
        #     break
        # [ user, product, review, lable]
        document = list([pd_reader[0][i], pd_reader[1][i], pd_reader[3][i], pd_reader[2][i]])
        documents.append(document)
    return documents

def get_pair_attributes(datasets):
    user_product_pair = defaultdict()
    ATTR_MAP = {
        'user': int(0),
        'product': int(1),
    }
    for document in datasets:
        user = document[ATTR_MAP["user"]]
        product = document[ATTR_MAP["product"]]
        key = tuple([user, product])
        user_product_pair[key] = user_product_pair.get(key, 0) + 1
    return user_product_pair


###### IMDB ######
"""
documents_train = read_file('./data/imdb/imdb.train.txt.ss')
pair_train = get_pair_attributes(documents_train)
num = 0
max_num = 0
for key, value in pair_train.items():
    if int(value) > 1:
        num += 1
        max_num = max(max_num,value)
        # print(key)
        # print(value)
print("repeat number:")
print(num)
print("repeat max times:")
print(max_num)
pair_train_set = set(pair_train)
print("occur first number:")
print(len(pair_train_set))


print('-'*50)
documents_dev = read_file('./data/imdb/imdb.dev.txt.ss')
pair_dev = get_pair_attributes(documents_dev)

num_dev = 0
max_num_dev = 0
for key, value in pair_dev.items():
    if int(value) > 1:
        num_dev += 1
        max_num_dev = max(max_num_dev,value)

print("repeat number:")
print(num_dev)
print("repeat max times:")
print(max_num_dev)

pair_dev_set = set(pair_dev)
print("occur first number:")
print(len(pair_dev_set))


print('-'*50)
documents_test = read_file('./data/imdb/imdb.test.txt.ss')
pair_test = get_pair_attributes(documents_test)

num_test = 0
max_num_test = 0
for key, value in pair_test.items():
    if int(value) > 1:
        num_test += 1
        max_num_test = max(max_num_test, value)

print("repeat number:")
print(num_test)
print("repeat max times:")
print(max_num_test)

pair_test_set = set(pair_test)
print("occur first number:")
print(len(pair_test_set))

# judge whether the dev pair occurs in train
for key in pair_dev.items():
    if key in pair_train:
        print(key)

# judge whether the test pair occurs in train
for key in pair_test.items():
    if key in pair_train:
        print(key)
"""

###### Yelp2013 ######
"""
documents_train = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')
pair_train = get_pair_attributes(documents_train)
num = 0
max_num = 0
for key, value in pair_train.items():
    if int(value) > 1:
        num += 1
        max_num = max(max_num,value)
        # print(key)
        # print(value)
print("repeat number:")
print(num)
print("repeat max times:")
print(max_num)
pair_train_set = set(pair_train)
print("occur first number:")
print(len(pair_train_set))


print('-'*50)
documents_dev = read_file('./data/yelp_13/yelp-2013-seg-20-20.dev.ss')
pair_dev = get_pair_attributes(documents_dev)

num_dev = 0
max_num_dev = 0
for key, value in pair_dev.items():
    if int(value) > 1:
        num_dev += 1
        max_num_dev = max(max_num_dev,value)

print("repeat number:")
print(num_dev)
print("repeat max times:")
print(max_num_dev)

pair_dev_set = set(pair_dev)
print("occur first number:")
print(len(pair_dev_set))


print('-'*50)
documents_test = read_file('./data/yelp_13/yelp-2013-seg-20-20.test.ss')
pair_test = get_pair_attributes(documents_test)

num_test = 0
max_num_test = 0
for key, value in pair_test.items():
    if int(value) > 1:
        num_test += 1
        max_num_test = max(max_num_test, value)

print("repeat number:")
print(num_test)
print("repeat max times:")
print(max_num_test)

pair_test_set = set(pair_test)
print("occur first number:")
print(len(pair_test_set))

# judge whether the dev pair occurs in train
for key in pair_dev.items():
    if key in pair_train:
        print(key)

# judge whether the test pair occurs in train
for key in pair_test.items():
    if key in pair_train:
        print(key)
"""

###### Yelp2013 ######
documents_train = read_file('./data/yelp_14/yelp-2014-seg-20-20.train.ss')
pair_train = get_pair_attributes(documents_train)
num = 0
max_num = 0
for key, value in pair_train.items():
    if int(value) > 1:
        num += 1
        max_num = max(max_num,value)
        # print(key)
        # print(value)
print("repeat number:")
print(num)
print("repeat max times:")
print(max_num)
pair_train_set = set(pair_train)
print("occur first number:")
print(len(pair_train_set))


print('-'*50)
documents_dev = read_file('./data/yelp_14/yelp-2014-seg-20-20.dev.ss')
pair_dev = get_pair_attributes(documents_dev)

num_dev = 0
max_num_dev = 0
for key, value in pair_dev.items():
    if int(value) > 1:
        num_dev += 1
        max_num_dev = max(max_num_dev,value)

print("repeat number:")
print(num_dev)
print("repeat max times:")
print(max_num_dev)

pair_dev_set = set(pair_dev)
print("occur first number:")
print(len(pair_dev_set))


print('-'*50)
documents_test = read_file('./data/yelp_14/yelp-2014-seg-20-20.test.ss')
pair_test = get_pair_attributes(documents_test)

num_test = 0
max_num_test = 0
for key, value in pair_test.items():
    if int(value) > 1:
        num_test += 1
        max_num_test = max(max_num_test, value)

print("repeat number:")
print(num_test)
print("repeat max times:")
print(max_num_test)

pair_test_set = set(pair_test)
print("occur first number:")
print(len(pair_test_set))

# judge whether the dev pair occurs in train
for key in pair_dev.items():
    if key in pair_train:
        print(key)

# judge whether the test pair occurs in train
for key in pair_test.items():
    if key in pair_train:
        print(key)