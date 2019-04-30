import numpy as np
import networkx as nx

np.set_printoptions(suppress=True)

g = nx.Graph()

datas = np.loadtxt('graph.txt')
for data in datas:
    g.add_nodes_from(list(data))
    g.add_edge(data[0], data[1])

nx.draw(g, pos=nx.random_layout(g), node_color='blue', edge_color='black', with_labels=False, font_size=18, node_size=20)
# pr_value = nx.pagerank(g, alpha=1)
# print("Naive pagerank is：", pr_value)

pr_impro_value = nx.pagerank(g, alpha=0.85)
print("Pagerank is：", pr_impro_value)