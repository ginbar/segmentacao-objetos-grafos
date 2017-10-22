

from skimage.measure import regionprops
import matplotlib.pyplot as plt
import networkx as nx



def visualizar_grafo_modelo(grafo, marcadores, imagem):
    
    # Para que o regionprops considere a regiao zero
    adicionados = marcadores + 1 

    propriedades = regionprops(adicionados)    

    figura = plt.figure(figsize=(8, 8))
    eixo = figura.add_axes([0.1, 0.3, 0.8, 0.6])
    
    posicoes = {}

    for regiao in propriedades:
        centroide = propriedades[regiao.label - 1].centroid
        posicoes[regiao.label - 1] = centroide[::-1] # Trocando x e y

    nx.draw(grafo, pos=posicoes, ax=eixo)

    eixo.imshow(imagem)

    plt.show()



def visualizar_grafo_marcadores(grafo, marcadores, imagem):
    
    # Para que o regionprops considere a regiao zero
    adicionados = marcadores + 1 

    propriedades = regionprops(adicionados)    

    figura = plt.figure(figsize=(8, 8))
    eixo_grafo = figura.add_axes([0.1, 0.3, 0.8, 0.6])
    eixo_marcadores = figura.add_axes([0.1, 0.3, 0.8, 0.6])

    posicoes = {}

    for regiao in propriedades:
        centroide = propriedades[regiao.label - 1].centroid
        posicoes[regiao.label - 1] = centroide[::-1] # Trocando x e y

    nx.draw(grafo, pos=posicoes, ax=eixo_grafo)

    eixo_grafo.imshow(imagem)
    
    eixo_marcadores.imshow(imagem)
    eixo_marcadores.imshow(marcadores)

    plt.show()