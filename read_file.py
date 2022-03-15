import pandas as pd

def read_file(filename):
    pd_reader = pd.read_csv(filename, header=None, skiprows=0, encoding="utf-8", sep='\t\t', engine='python') # pandas中read_csv是随机读的
    documents = []
    for i in range(len(pd_reader[0])):
        document = list([pd_reader[0][i], pd_reader[1][i], pd_reader[3][i], pd_reader[2][i]])
        documents.append(document)
    return documents

def read_file_user_product_rating(filename):
    pd_reader = pd.read_csv(filename, header=None, skiprows=0, encoding="utf-8", sep='\t\t', engine='python') # pandas中read_csv是随机读的
    documents = []
    users = set()
    products = set()

    for i in range(len(pd_reader[0])):
        document = list([pd_reader[0][i], pd_reader[1][i], pd_reader[2][i]])
        documents.append(document)
        users.add(pd_reader[0][i])
        products.add(pd_reader[1][i])

    return documents, users, products

def read_file_user_mapping_id(filename):
    pd_reader = pd.read_csv(filename)
    df = pd.DataFrame(pd_reader)
    cols = [0, 1]
    df = df[df.columns[cols]]
    df = df.drop_duplicates(subset=['User ID'])
    # df.set_index("User ID", drop=True, inplace=True)
    # user_dict = df.to_dict(orient="index")
    # print(df)
    user_id_dict = dict(zip(df['User ID'], df['User']))
    #print(user_dict)
    return user_id_dict

def read_file_user_cluster(filename):
    pd_reader = pd.read_csv(filename) # pandas中read_csv是随机读的
    df = pd.DataFrame(pd_reader)
    user_cluster_dict = dict(zip(df['User ID'], df['Cluster']))
    #print(user_cluster_dict)
    return user_cluster_dict

# rfilename1 = './data/csv/yelp-2013-cluster-user-results.csv'
# read_file_user_cluster(rfilename1)
