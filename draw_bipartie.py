import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

# Initialise the graph
G = nx.Graph()

# Add nodes with the node attribute "bipartite"
top_nodes = ['A1','A2','A3','A4']
bottom_nodes = ['B1','B2','B3']
G.add_nodes_from(top_nodes, bipartite=0)
G.add_nodes_from(bottom_nodes, bipartite=1)

# Add edges with weights
# G.add_edges_from([('A1', "B3"),('A4', "B1"),('A2', "B2"),('A2', "B3"),('A3', "B1")])
# Weighted bipartite graph
G.add_edge('A1', "B3", weight=1)
G.add_edge('A1', "B3", weight=2)
G.add_edge('A4', "B1", weight=2)
G.add_edge('A2', "B2", weight=4)
G.add_edge('A2', "B3", weight=3)
G.add_edge('A3', "B1", weight=2)
bipartite.is_bipartite(G)

#visualize the graph
# nx.draw_networkx(G, pos=nx.drawing.layout.bipartite_layout(G, ['A1','A2','A3','A4']), width=2)
#
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_edge_labels(G,pos=nx.drawing.layout.bipartite_layout(G, ['A1','A2','A3','A4']), edge_labels=labels)

pos=nx.drawing.layout.bipartite_layout(G, ['A1','A2','A3','A4'])
nx.draw_networkx(G,pos)
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

plt.axis("off")
plt.show()