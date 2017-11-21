
from skimage.io import imread
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from  matplotlib.colors import Normalize
from pylab import cm
import cv2 

import caracteristicas.momentos  as mts
from modelo.construir import construir_modelo
from modelo.visualzacao import visualizar_grafo_modelo
from processamento.sog import Isom
from processamento.preprocessamento import  carregar_prepros_seq_imagens
from modelo.cores import intensidade_por_cor


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

    prim_img, prim_momentos = imagens[0],  momentos[0]

    _, grafo =  construir_modelo(prim_img, marcadores[0], bordas[0], args)

    mts_por_superpx = {label: momts for (label, momts) in prim_momentos if label in grafo}
    
    # Usando os momentos da primeira figura como momentos do modelo
    nx.set_node_attributes(grafo, 'momentos', mts_por_superpx)     

    figura = plt.figure(figsize=(8, 8))
    eixo = figura.add_axes([0.1, 0.3, 0.8, 0.6])
    eixo.imshow(prim_img)

    larg, altu, _ = prim_img.shape 
    mascara = np.empty((larg, altu)) * np.nan
    
    sog = Isom(grafo, epocas=20)
    
    # para testes
    imagens = [prim_img,  prim_img]
    momentos = [momentos[0], momentos[0]]
    marcadores = [marcadores[0], marcadores[0]]

    frames_segmentados = []

    for img, marcs, momts in zip(imagens[1:], marcadores[1:], momentos[1:]):

        sog.novos_superpxs(momts)
        
        while not sog.convergiu():
            sog.epoca()
        
        resultado = sog.no_por_superpx()
        
        for (label_spx, _), no in zip(momts, resultado):
            np.putmask(mascara, marcs == label_spx, intensidade_por_cor[grafo.node[no]['cor']])

        eixo.imshow(mascara, norm=Normalize(0, 100), cmap=cm.jet, alpha=.6)
        plt.show()

        frames_segmentados.append(mascara)

    salvar_video(frames_segmentados, args.dirdest)



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


def salvar_video(frames, nome, fps=0.5):
    pass