import pandas as pd
from collections import Counter, defaultdict

def read_file(dataset):
    pd_reader = pd.read_csv(dataset, header=None, skiprows=0, encoding="utf-8", sep='\t\t', engine='python')
    documents = []
    for i in range(len(pd_reader[0])):
        document = list([pd_reader[0][i], pd_reader[1][i], pd_reader[3][i], pd_reader[2][i]])
        documents.append(document)
    return documents

def get_each_product_rating_history(dataset):
    product_rating_history = defaultdict(list)
    ATTR_MAP_2 = {
        'product': int(1),
        'label': int(3),
    }
    for document in dataset:
        product_map = ATTR_MAP_2["product"]
        product = document[product_map]
        lab_map = ATTR_MAP_2["label"]
        lab = document[lab_map]
        product_rating_history[product].append(lab)

    return product_rating_history

def calculate_product_rating_quality(data):
    product_rating_quality = defaultdict()
    for k, v in data.items():
        # k = d[0]
        # v = d[1]
        product_rating_quality[k] = round(sum(v) / len(v))
    return product_rating_quality


def calculate_product_each_label_probability(product_rating_history):
    # calculate the product each rating label %
    product_rating_probability = defaultdict()
    for k, v in product_rating_history.items():
        occurrence = Counter(v)
        for l, t in occurrence.items():
            occurrence[l] = t / len(v)
        product_rating_probability[k] = occurrence

    return product_rating_probability

def rule1(name, value, average):
    if name == "IMDB":
        threshold = 2
    else:
        threshold = 1
    # based on the average product rating and the defined threshold
    if abs(value - average) > threshold:
        return False
    return True

def rule2(name, rating_probability, rating):
    # based on the probability
    if name == "IMDB":
        probability = 0.08
    else:
        probability = 0.20

    if rating_probability[rating] < probability:
        return False

    return True


def construct_new_dataset(name, dataset, product_rating_history, product_rating_quality, product_rating_probability):
    # remove outlier label from the old dataset based on the rule 1 or rule 2
    ATTR_MAP_3 = {
        'user': int(0),
        'product': int(1),
        'label': int(3),
        'review': int(2)
    }
    new_documents = []
    new_documents_2 = []
    # product_rating_history = dict(product_rating_history)
    # product_rating_quality = dict(product_rating_quality)

    for document in dataset:
        user_map = ATTR_MAP_3["user"]
        user = document[user_map]
        product_map = ATTR_MAP_3["product"]
        product = document[product_map]
        lab_map = ATTR_MAP_3["label"]
        lab = document[lab_map]
        review_map = ATTR_MAP_3["review"]
        review = document[review_map]
        product_average = product_rating_quality[product]
        product_history = product_rating_probability[product]
        if rule1(name, lab, product_average):
            new_document = list([user, product, review, lab])
            new_documents.append(new_document)
        if rule2(name, product_history, lab):
            new_document_2 = list([user, product, review, lab])
            new_documents_2.append(new_document_2)

    return new_documents, new_documents_2

"""
imdb
"""
# documents = read_file('./data/imdb/imdb.train.txt.ss')
# product_rating_history = get_each_product_rating_history(documents)
# product_rating_quality = calculate_product_rating_quality(product_rating_history)
# product_rating_probability = calculate_product_each_label_probability(product_rating_history)
# name = "IMDB"
# new_documents, new_documents_2 = construct_new_dataset(name, documents, product_rating_history, product_rating_quality, product_rating_probability)
#
# print(len(documents))
# print(len(new_documents))
# print(len(new_documents_2))

"""
yelp2013
"""
# documents = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')
# product_rating_history = get_each_product_rating_history(documents)
# product_rating_quality = calculate_product_rating_quality(product_rating_history)
# product_rating_probability = calculate_product_each_label_probability(product_rating_history)
# name = "yelp"
# new_documents, new_documents_2 = construct_new_dataset(name, documents, product_rating_history, product_rating_quality, product_rating_probability)
#
# print(len(documents))
# print(len(new_documents))
# print(len(new_documents_2))

"""
yelp2013
"""
documents_1 = read_file('./data/yelp_13/yelp-2013-seg-20-20.test.ss')
print(len(documents_1))

"""
yelp2014
"""
documents_2 = read_file('./data/yelp_14/yelp-2014-seg-20-20.test.ss')
print(len(documents_2))