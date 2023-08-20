

from skimage.measure import regionprops
import matplotlib.pyplot as plt
import networkx as nx



def visualize_model_graph(graph, labels, image):
    
    # Para que o regionprops considere a regiao zero
    shifted_labels = labels + 1 

    proprities = regionprops(shifted_labels)

    figure = plt.figure(figsize=(8, 8))
    axis = figure.add_axes([0.1, 0.3, 0.8, 0.6])
    
    positions = {}

    for regiao in proprities:
        centroide = proprities[regiao.label - 1].centroid
        positions[regiao.label - 1] = centroide[::-1] # Trocando x e y

    nx.draw(graph, pos=positions, ax=axis)

    axis.imshow(image)

    plt.show()



def visualize_graph_labels(graph, labels, image):
    
    # Para que o regionprops considere a regiao zero
    shifted_labels = labels + 1 

    proprities = regionprops(shifted_labels)    

    figure = plt.figure(figsize=(8, 8))
    graph_axis = figure.add_axes([0.1, 0.3, 0.8, 0.6])
    label_axis = figure.add_axes([0.1, 0.3, 0.8, 0.6])

    positions = {}

    for regiao in proprities:
        centroide = proprities[regiao.label - 1].centroid
        positions[regiao.label - 1] = centroide[::-1] # Trocando x e y

    nx.draw(graph, pos=positions, ax=graph_axis)

    graph_axis.imshow(image)
    
    label_axis.imshow(image)
    label_axis.imshow(labels)

    plt.show()