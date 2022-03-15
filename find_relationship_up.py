from collections import Counter
from collections import defaultdict
import pandas as pd

def read_file(dataset):
    pd_reader = pd.read_csv(dataset, header=None, skiprows=0, encoding="utf-8", sep='\t\t', engine='python')
    documents = []
    #label_documents = []
    file1 = open('yelp13_label_documents.txt', 'w')
    for i in range(len(pd_reader[0])):
        # if i == 100:
        #     break
        # [ user, product, review, lable]
        document = list([pd_reader[0][i], pd_reader[1][i], pd_reader[3][i], pd_reader[2][i]])
        documents.append(document)
        label_document = pd_reader[0][i]+"    "+pd_reader[1][i]+ "   "+str(pd_reader[2][i])+"\n"
        #label_documents.append(label_document)
        file1.write(label_document)
    file1.close()
    return documents

def get_relationships(datasets):
    users = Counter()
    products = Counter()

    user_map_products = defaultdict(list)
    product_map_users = defaultdict(list)
    ATTR_MAP = {
        'user': int(0),
        'product': int(1),
        'label': int(3),
        'review': int(2)
    }
    for document in datasets:
        users.update([document[ATTR_MAP["user"]]])
        products.update([document[ATTR_MAP["product"]]])
        user_map_products[document[ATTR_MAP["user"]]].append([document[ATTR_MAP["product"]], document[ATTR_MAP["label"]], document[ATTR_MAP["review"]]])
        product_map_users[document[ATTR_MAP["product"]]].append([document[ATTR_MAP["user"]], document[ATTR_MAP["label"]], document[ATTR_MAP["review"]]])

    return users, products, user_map_products, product_map_users


documents_train = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')
user_train, product_train, user_map_products, product_map_users = get_relationships(documents_train)
print(user_train)
specific_product = 'b5cEoKR8iQliq-yT2_O0LQ'
print(product_train[specific_product])

# labels = []
# sum_labels = 0
# file2 = open('specific_product_documents.txt', 'w')
# for u in product_map_users[specific_product]:
#     product_document = u[0] + '\t' + specific_product + '\t' + u[2] + '\t' + str(u[1])+ '\n'
#     file2.write(product_document)
#     labels.append(u[1])
#     sum_labels = sum_labels + u[1]
# print(sum_labels/len(labels))
# file2.close()
#

"""
find the outliner product review: which value < 3
"""
# file3 = open('specific_product_outliner_documents.txt', 'w')
# for u in product_map_users[specific_product]:
#     if u[1] < 3:
#         product_document = u[0] + '\t' + specific_product + '\t' + u[2] + '\t' + str(u[1])+ '\n'
#         file3.write(product_document)
# file3.close()

file4 = open('specific_product_345_documents.txt', 'w')
for u in product_map_users[specific_product]:
    if u[1] >= 3:
        product_document = u[0] + '\t' + specific_product + '\t' + u[2] + '\t' + str(u[1])+ '\n'
        file4.write(product_document)
file4.close()
