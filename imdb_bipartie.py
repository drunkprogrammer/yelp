import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

def read_file(dataset):
    pd_reader = pd.read_csv(dataset, header=None, skiprows=0, encoding="utf-8", sep='\t\t', engine='python')
    print("total number:")
    print(len(pd_reader[0]))
    documents = []
    for i in range(len(pd_reader[0])):
        document = list([pd_reader[0][i], pd_reader[1][i], pd_reader[3][i], pd_reader[2][i]])
        documents.append(document)
    return documents

def get_edge_and_weight(datasets):
    edges = list([])
    users = set()
    products = set()
    ATTR_MAP = {
        'user': int(0),
        'product': int(1),
        'review': int(2),
        'label': int(3)
    }
    for document in datasets:
        userID = document[ATTR_MAP["user"]]
        productID = document[ATTR_MAP["product"]]
        labelValue = document[ATTR_MAP["label"]]
        users.add(userID)
        products.add(productID)
        edges.append([userID, productID, labelValue])

    return users, products, edges

def draw_imdb_bipartie_graph(edges):
    # Initialise the graph
    G = nx.Graph()

    # Add nodes with the node attribute "bipartite"
    top_nodes = set()
    bottom_nodes = set()

    for edge in edges:
        top_nodes.add(edge[0])
        bottom_nodes.add(edge[1])

    G.add_nodes_from(list(top_nodes), bipartite=0)
    G.add_nodes_from(list(bottom_nodes), bipartite=1)

    # Add edges with weights
    # G.add_edges_from([('A1', "B3"),('A4', "B1"),('A2', "B2"),('A2', "B3"),('A3', "B1")])
    # Weighted bipartite graph
    for edge in edges:
        print(edge[2])
        G.add_edge(edge[0], edge[1], weight=int(edge[2]))
    bipartite.is_bipartite(G)

    pos = nx.drawing.layout.bipartite_layout(G, top_nodes)
    nx.draw_networkx(G, pos)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.axis("off")
    plt.show()


documents_train = read_file('./data/imdb/imdb.test.txt.ss')
users, products, edges = get_edge_and_weight(documents_train)
users_list = list(users)
products_list = list(products)
draw_imdb_bipartie_graph(edges[:10])