import networkx as nx
import matplotlib.pyplot as plt

# For GraphML
# G = nx.read_graphml("semantic.graphml")

# For GML
G = nx.read_gml("static.gml")

plt.figure(figsize=(10,8))
nx.draw(G, with_labels=True, node_size=500)
plt.show()