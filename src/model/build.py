
from skimage.future.graph import rag_mean_color
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import networkx as nx

from modelo.construtor_modelo import ModelConstructionUI


def build_model(image, labels, borders, args):
    
    constructor = ModelConstructionUI(image)
    
    constructor.labels = labels
    constructor.bordas = borders
    constructor.graph = rag_mean_color(image, labels)
    
    constructor.show()
    
    return constructor.get_model()



def visualize_model(graph, labels, image):
    
    added = labels + 1 
    properties = regionprops(added)    

    figure = plt.figure(figsize=(8, 8))
    axis = figure.add_axes([0.1, 0.3, 0.8, 0.6])
    
    centroids = {}
    for region in properties:
        centroide = properties[region.label - 1].centroid
        centroids[region.label - 1] = centroide[::-1] # Invertendo x e y

    nx.draw(graph, pos=centroids, ax=axis)

    axis.imshow(image)

    plt.show()        