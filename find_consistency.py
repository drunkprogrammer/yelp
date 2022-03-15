import pandas as pd
from collections import Counter, defaultdict

def read_file(dataset):
    pd_reader = pd.read_csv(dataset, header=None, skiprows=0, encoding="utf-8", sep='\t\t', engine='python')
    documents = []
    for i in range(len(pd_reader[0])):
        # if i == 100:
        #     break
        # [ user, product, review, lable]
        document = list([pd_reader[0][i], pd_reader[1][i], pd_reader[3][i], pd_reader[2][i]])
        documents.append(document)
    return documents

def get_attributes(datasets):
    users = set()
    products = set()
    ATTR_MAP = {
        'user': int(0),
        'product': int(1),
    }
    for document in datasets:
        users.add(document[ATTR_MAP["user"]])
        products.add(document[ATTR_MAP["product"]])
    return users, products

###### IMDB ######
"""
documents_train = read_file('./data/imdb/imdb.train.txt.ss')
user_train, product_train = get_attributes(documents_train)

documents_dev = read_file('./data/imdb/imdb.dev.txt.ss')
user_dev, product_dev = get_attributes(documents_dev)

documents_test = read_file('./data/imdb/imdb.test.txt.ss')
user_test, product_test = get_attributes(documents_test)
"""


###### Yelp2013 ######
"""
documents_train = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')
user_train, product_train = get_attributes(documents_train)

documents_dev = read_file('./data/yelp_13/yelp-2013-seg-20-20.dev.ss')
user_dev, product_dev = get_attributes(documents_dev)

documents_test = read_file('./data/yelp_13/yelp-2013-seg-20-20.test.ss')
user_test, product_test = get_attributes(documents_test)
"""

###### Yelp2014 ######
documents_train = read_file('./data/yelp_14/yelp-2014-seg-20-20.train.ss')
user_train, product_train = get_attributes(documents_train)

documents_dev = read_file('./data/yelp_14/yelp-2014-seg-20-20.dev.ss')
user_dev, product_dev = get_attributes(documents_dev)

documents_test = read_file('./data/yelp_14/yelp-2014-seg-20-20.test.ss')
user_test, product_test = get_attributes(documents_test)


user_train_sorted = sorted(user_train)
user_test_sorted = sorted(user_test)
print("User: ")
print(len(user_train_sorted))
print(len(user_dev))
print(len(user_test_sorted))
if user_train_sorted == user_test_sorted:
    print(True)
else:
    print(False)

product_train_sorted = sorted(product_train)
product_test_sorted = sorted(product_test)
print("product: ")
print(len(product_train_sorted))
print(len(product_test_sorted))
print(len(product_dev))
if product_train_sorted == product_test_sorted:
    print(True)
else:
    print(False)


num_new = 0
for p in product_test_sorted:
    if p not in product_train_sorted:
        num_new += 1

print(num_new)