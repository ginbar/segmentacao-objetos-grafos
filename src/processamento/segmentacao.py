
from skimage.io import imread
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from  matplotlib.colors import Normalize
from pylab import cm
import cv2
import math 
import skvideo.io 
# from skvideo.io import vwriter

import caracteristicas.momentos  as mts
from modelo.construir import build_model, visualize_model
from modelo.visualzacao import visualize_model_graph
from processamento.sog import Isom
from processamento.preprocessamento import  load_processement
from modelo.cores import intensidade_por_cor
from resultado import salvar_mascaras_seq_imagens


def segmentar_video(video, args):
    """
    Segmenta uma sequencia de video.
    """    
    _, frame = video.read()

    marcadores, grafo, cor_por_no =  build_model(frame, args)
    
    superpxs = mts.cromaticidade(video, marcadores)

    figura = plt.figure(figsize=(8, 8))
    eixo = figura.add_axes([0.1, 0.3, 0.8, 0.6])

    sog = Isom(grafo, cor_por_no, )

    while not sog.convergiu():
        sog.epoch()
        
        #if args.prepros == False:
        #    visualizar_grafo_marcadores()
        plt.show()




def segmentar_seq_imagens(imagens, args):
    """
    Segmenta uma conjunto de imagens parecidas. As imagens devem ser passadas 
    como um array. 
    """
    
    marcadores, bordas, momentos, centroides = load_processement(args)    

    prim_img, prim_momnts = imagens[0],  momentos[0]
    prim_bordas, prim_marcs = bordas[0], marcadores[0]
    prim_centrs = centroides[0]

    grafo, segm_usuario =  build_model(prim_img, prim_marcs, prim_bordas, args)

    visualize_model(grafo, prim_marcs, prim_img)

    mts_por_superpx = {label: momts for (label, momts) in prim_momnts if label in grafo}
    centr_por_superpx = {label: centr for (label, centr) in prim_centrs if label in grafo}

    # Usando os momentos da primeira figura como momentos do modelo
    nx.set_node_attributes(grafo, 'momentos', mts_por_superpx)     
    nx.set_node_attributes(grafo, 'centroide', centr_por_superpx)

    larg, altu, _ = prim_img.shape 
    mascara = np.empty((larg, altu)) * np.nan
    
    norm_centr = _normal_centroides(larg, altu)
    num_momts, norm_momts =  _normal_momentos(momentos[0])

    sog = Isom(grafo, norm_momts, num_momts, norm_centr, epocas=20, ratio=args.ratio)
    
    frames_segmentados = [segm_usuario]

    for img, marcs, momts, centrs in zip(imagens[1:], marcadores[1:], momentos[1:], centroides[1:]):

        sog.novos_superpxs(momts, centrs)
        
        while not sog.convergiu():
            sog.epoch()
        
        resultado = sog.node_per_superpx()
        
        for (label_spx, _), no in zip(momts, resultado):
            np.putmask(mascara, marcs == label_spx, intensidade_por_cor[grafo.node[no]['cor']])

        frames_segmentados.append(mascara)
        mascara = np.empty((larg, altu)) * np.nan        


    salvar_mascaras_seq_imagens(frames_segmentados, args)




def segmentar_imagem(imagem, args):
    """
    
    """
    marcadores, bordas = None, None

    if args.cache:
        marcadores, bordas = carregar_imagem_prepros(args.dirdest)
    else:
        marcadores, bordas = marcadores_e_bordas(imagem, args)

    marcadores, grafo, marc_por_no = build_model(imagem, marcadores, bordas, args)

    visualize_model_graph(grafo, marcadores, imagem)




def visualizar_segmen_video(video, args):
    pass




def salvar_video(frames, dimensoes, args, fps=0.5):

    writer = skvideo.io.LibAVWriter('videos/output.avi', inputdict={ '-r': str(fps) })

    lista_inter = range(0, 10)

    for frame in frames:
        for _ in lista_inter:
            writer.writeFrame(frame)

    writer.close()




def _normal_centroides(largura, altura):
    return math.sqrt(math.pow(largura, 2) + math.pow(altura, 2))


def _normal_momentos(momentos):
    
    matriz = np.array([momts for _, momts in momentos])    
    num_momts = matriz[0].size

    valores_max = np.array([np.max(matriz[:,indice]) for indice in range(num_momts)])

    return num_momts, valores_max