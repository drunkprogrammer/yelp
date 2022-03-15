import pandas as pd
import os

def read_file(dataset):
    pd_reader = pd.read_csv(dataset, header=None, skiprows=0, encoding="utf-8", sep='\t\t', engine='python')
    documents = []
    for i in range(len(pd_reader[0])):
        document = list([pd_reader[0][i], pd_reader[1][i], pd_reader[3][i], pd_reader[2][i]])
        documents.append(document)
    return documents

def corporate_file(root1, root2, root3, filename1, filename2, filename3):
    os.makedirs(os.path.dirname(root3 + filename3), exist_ok=True)
    fname = open(root3 + filename3, "w", encoding="utf8")
    x = open(root1 + filename1,  "r", encoding="utf8")
    fname.write(x.read())
    y = open(root2 + filename2,  "r", encoding="utf8")
    fname.write(y.read())
    fname.close()
    return root3 + filename3

"""
----------------
# Train Data
----------------
"""

# root1 = "./data/yelp_13/"
# root2 = "./data/yelp_14/"
# root3 = "./data/corporate/"
# filename1 = "yelp-2013-seg-20-20.train.ss"
# filename2 = "yelp-2014-seg-20-20.train.ss"
# filename3 = "yelp-corporate-seg-20-20.train.ss"
#
# cor_train_filename = corporate_file(root1, root2, root3, filename1, filename2, filename3)
# train_yelp13 = read_file(root1 + filename1)
# train_yelp14 = read_file(root2 + filename2)
# train_corporate = read_file(cor_train_filename)
# print("train_yelp13 length: ")
# print(len(train_yelp13))
# print("train_yelp14 length: ")
# print(len(train_yelp14))
# print("corporate length: ")
# print(len(train_corporate))

"""
----------------
# Dev Data
----------------
"""

# root1 = "./data/yelp_13/"
# root2 = "./data/yelp_14/"
# root3 = "./data/corporate/"
# filename1 = "yelp-2013-seg-20-20.dev.ss"
# filename2 = "yelp-2014-seg-20-20.dev.ss"
# filename3 = "yelp-corporate-seg-20-20.dev.ss"
#
# cor_train_filename = corporate_file(root1, root2, root3, filename1, filename2, filename3)
# dev_yelp13 = read_file(root1 + filename1)
# dev_yelp14 = read_file(root2 + filename2)
# dev_corporate = read_file(cor_train_filename)
# print("dev_yelp13 length: ")
# print(len(dev_yelp13))
# print("dev_yelp14 length: ")
# print(len(dev_yelp14))
# print("corporate length: ")
# print(len(dev_corporate))


"""
----------------
# Test Data
----------------
"""
root1 = "./data/yelp_13/"
root2 = "./data/yelp_14/"
root3 = "./data/corporate/"
filename1 = "yelp-2013-seg-20-20.test.ss"
filename2 = "yelp-2014-seg-20-20.test.ss"
filename3 = "yelp-corporate-seg-20-20.test.ss"

cor_train_filename = corporate_file(root1, root2, root3, filename1, filename2, filename3)
test_yelp13 = read_file(root1 + filename1)
test_yelp14 = read_file(root2 + filename2)
test_corporate = read_file(cor_train_filename)
print("dev_yelp13 length: ")
print(len(test_yelp13))
print("dev_yelp14 length: ")
print(len(test_yelp14))
print("corporate length: ")
print(len(test_corporate))