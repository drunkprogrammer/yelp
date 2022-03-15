import pandas as pd
from collections import Counter, defaultdict

def read_file(dataset):
    pd_reader = pd.read_csv(dataset, header=None, skiprows=0, encoding="utf-8", sep='\t\t', engine='python')
    documents = []
    for i in range(len(pd_reader[0])):
        document = list([pd_reader[0][i], pd_reader[1][i], pd_reader[3][i], pd_reader[2][i]])
        documents.append(document)
    return documents

def store_review(documents):
    store_dict_times = defaultdict(int)
    store_dict_document = defaultdict(list)
    store_dict_repeat_document = defaultdict(list)
    for i, document in enumerate(documents):
        store_dict_times[document[2]] += 1
        store_dict_document[document[2]].append(list([i, document[2], document[0], document[1], document[3]]))

    for key, value in store_dict_document.items():
        if store_dict_times[key] > 1:
            store_dict_repeat_document[key] = store_dict_document[key]

    return store_dict_times, store_dict_document, store_dict_repeat_document

def judge_two_document_repeatment(documents1, documents2):

    repeat_times = 0
    repeat_times_1 = 0
    repeat_times_2 = 0
    repeatment_doc = defaultdict(list)
    for key, value in documents1.items():
        if key in documents2.keys():
            # print(value)
            # a = value[0][2]
            # print(a)
            # b = documents2[key][0][2]
            # print(b)
            repeat_times_1 += 1
            if value[0][2] == documents2[key][0][2] or value[0][3] == documents2[key][0][3]:
                repeat_times += 1
                repeatment_doc[key].append(value)

            if value[0][2] == documents2[key][0][2] and value[0][3] == documents2[key][0][3]:
                repeat_times_2 += 1
                repeatment_doc[key].append(value)

    return repeat_times_1, repeat_times, repeat_times_2, repeatment_doc





###### Yelp Corporate ######
# documents_train = read_file('./data/corporate/yelp-corporate-seg-20-20.train.ss')
# print(len(documents_train))
# store_dict, store_dict_document, store_dict_repeat_document = store_review(documents_train)
# print(store_dict_document)
# print(store_dict_repeat_document)


#
# documents_dev = read_file('./data/corporate/yelp-corporate-seg-20-20.dev.ss')
# user_dev, product_dev = read_file(documents_dev)

# documents_test = read_file('./data/corporate/yelp-corporate-seg-20-20.test.ss')
# store_dict = store_review(documents_test)

###### Yelp2013 ######
# documents_train = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')
# print(len(documents_train))
# store_dict, store_dict_document, store_dict_repeat_document = store_review(documents_train)
# print(store_dict_document)
# print(store_dict_repeat_document)

###### Yelp2014 ######
# documents_train = read_file('./data/yelp_14/yelp-2014-seg-20-20.train.ss')
# print(len(documents_train))
# store_dict, store_dict_document, store_dict_repeat_document = store_review(documents_train)
# print(store_dict_document)
# print(store_dict_repeat_document)

###### IMDB ######
# documents_train = read_file('./data/imdb/imdb.train.txt.ss')
# print(len(documents_train))
# store_dict, store_dict_document, store_dict_repeat_document = store_review(documents_train)
# print(store_dict_document)
# print(store_dict_repeat_document)

###### Judge Train Yelp2013 and Yelp2014 ######
# documents_train_yelp2013 = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')
# documents_train_yelp2014 = read_file('./data/yelp_14/yelp-2014-seg-20-20.train.ss')
# store_dict_yelp2013, store_dict_document_yelp2013, store_dict_repeat_document_yelp2013 = store_review(documents_train_yelp2013)
# store_dict_yelp2014, store_dict_document_yelp2014, store_dict_repeat_document_yelp2014 = store_review(documents_train_yelp2014)
# repeat_times_1, repeat_times, repeatment_doc = judge_two_document_repeatment(store_dict_document_yelp2013, store_dict_document_yelp2014)
# print(repeat_times_1)
# print(repeat_times)
#print(repeatment_doc)

###### Judge Test Yelp2013 and Yelp2014 ######
# documents_test_yelp2013 = read_file('./data/yelp_13/yelp-2013-seg-20-20.test.ss')
# documents_test_yelp2014 = read_file('./data/yelp_14/yelp-2014-seg-20-20.test.ss')
# store_dict_yelp2013, store_dict_document_yelp2013, store_dict_repeat_document_yelp2013 = store_review(documents_test_yelp2013)
# store_dict_yelp2014, store_dict_document_yelp2014, store_dict_repeat_document_yelp2014 = store_review(documents_test_yelp2014)
# repeat_times_1, repeat_times,repeat_times_2, repeatment_doc = judge_two_document_repeatment(store_dict_document_yelp2013, store_dict_document_yelp2014)
# print(repeat_times_1) # 935
# print(repeat_times_2) # 931
# print(repeat_times) # 934

###### Judge Yelp and Yelp2013 ######
# documents_test_yelp2013 = read_file('./data/yelp_13/yelp-2013-seg-20-20.test.ss')
# documents_test_yelp2014 = read_file('./data/corporate/yelp-corporate-seg-20-20.train.ss')
# store_dict_yelp2013, store_dict_document_yelp2013, store_dict_repeat_document_yelp2013 = store_review(documents_test_yelp2013)
# store_dict_yelp2014, store_dict_document_yelp2014, store_dict_repeat_document_yelp2014 = store_review(documents_test_yelp2014)
# repeat_times_1, repeat_times, repeat_times_2, repeatment_doc = judge_two_document_repeatment(store_dict_document_yelp2013, store_dict_document_yelp2014)
# print(repeat_times_1) # 6718
# print(repeat_times_2) # 6702
# print(repeat_times) # 6717

###### Judge Yelp train and Yelp2014 test ######
documents_test_yelp2013 = read_file('./data/yelp_14/yelp-2014-seg-20-20.test.ss')
documents_test_yelp2014 = read_file('./data/corporate/yelp-corporate-seg-20-20.train.ss')
store_dict_yelp2013, store_dict_document_yelp2013, store_dict_repeat_document_yelp2013 = store_review(documents_test_yelp2013)
store_dict_yelp2014, store_dict_document_yelp2014, store_dict_repeat_document_yelp2014 = store_review(documents_test_yelp2014)
repeat_times_1, repeat_times, repeat_times_2, repeatment_doc = judge_two_document_repeatment(store_dict_document_yelp2013, store_dict_document_yelp2014)
print(repeat_times_1) # 6520
print(repeat_times_2) # 6498
print(repeat_times) # 6515