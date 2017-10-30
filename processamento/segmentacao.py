
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.segmentation import slic, watershed, random_walker, quickshift, felzenszwalb, mark_boundaries
from skimage.util import img_as_float
from skimage.filters import sobel
import matplotlib.pyplot as plt
import networkx as np

import caracteristicas.momentos  as mts
from modelo.construir import construir_modelo
from modelo.visualzacao import visualizar_grafo_modelo
from processamento.sog import Isom
from processamento.preprocessamento import  marcadores, carregar_prepros_seq_imagens



def segmentar_video(video, args):
    """
    Segmenta uma sequencia de video.
    """    
    _, frame = video.read()

    marcadores, grafo, cor_por_no =  construir_modelo(frame, args)
    
    superpxs = mts.cromaticidade(video, marcadores)

    figura = plt.figure(figsize=(8, 8))
    eixo = figura.add_axes([0.1, 0.3, 0.8, 0.6])

    sog = Isom(grafo, cor_por_no, )

    while not sog.convergiu():
        sog.epoca()
        
        #if args.prepros == False:
        #    visualizar_grafo_marcadores()
        plt.show()



def segmentar_seq_imagens(imagens, args):
    """
    Segmenta uma conjunto de imagens parecidas. As imagens devem ser passadas 
    como um array. 
    """
    
    marcadores, bordas, momentos = carregar_prepros_seq_imagens(args)    

    prim_img = imagens[0]

    marcadores, grafo =  construir_modelo(prim_img, marcadores[0], bordas[0], args)

    mts_por_superpx = {}
    for no in grafo.nodes():
        mts_por_superpx[no] = momentos[0][no]

    # Usando os momentos da primeira figura como momentos do modelo
    np.set_node_attributes(grafo, 'momentos', mts_por_superpx)     

    figura = plt.figure(figsize=(8, 8))
    eixo = figura.add_axes([0.1, 0.3, 0.8, 0.6])

    sog = Isom(grafo)
    imagens = [prim_img,  prim_img,  prim_img]

    for img, mts in zip(imagens[1:], momentos):
        sog.superpxs = mts
        while not sog.convergiu():
            sog.epoca()
        sog.no_por_superpx()            



def segmentar_imagem(imagem, args):
    """
    
    """
    marcadores, bordas = None, None

    if args.cache:
        marcadores, bordas = carregar_imagem_prepros(args.dirdest)
    else:
        marcadores, bordas = marcadores_e_bordas(imagem, args)

    marcadores, grafo, marc_por_no = construir_modelo(imagem, marcadores, bordas, args)

    visualizar_grafo_modelo(grafo, marcadores, imagem)


def visualizar_grafo_marcadores():
    pass


def visualizar_segmen_video(video, args):
    pass