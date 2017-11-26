
from skimage.future.graph import rag_mean_color
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import networkx as nx

from modelo.construtor_modelo import ConstrutorModelo


def construir_modelo(imagem, marcadores, bordas, args):
    
    construtor = ConstrutorModelo(imagem)
    
    construtor.marcadores = marcadores
    construtor.bordas = bordas
    construtor.grafo = rag_mean_color(imagem, marcadores)
    
    construtor.mostrar_figura()
    
    return construtor.extrair_modelo()



def visualizar_modelo(grafo, marcadores, imagem):
    
    adicionados = marcadores + 1 
    propriedades = regionprops(adicionados)    

    figura = plt.figure(figsize=(8, 8))
    eixo = figura.add_axes([0.1, 0.3, 0.8, 0.6])
    
    posicoes = {}
    for regiao in propriedades:
        centroide = propriedades[regiao.label - 1].centroid
        posicoes[regiao.label - 1] = centroide[::-1] # Invertendo x e y

    nx.draw(grafo, pos=posicoes, ax=eixo)

    eixo.imshow(imagem)

    plt.show()        