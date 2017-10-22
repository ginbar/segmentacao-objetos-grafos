
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.segmentation import slic, watershed, random_walker, quickshift, felzenszwalb, mark_boundaries
from skimage.util import img_as_float
from skimage.filters import sobel
import matplotlib.pyplot as plt

import caracteristicas.momentos  as mts
from modelo.construir import construir_modelo
from modelo.visualzacao import visualizar_grafo_modelo
from processamento.sog import Isom
from processamento.preprocessamento import  marcadores



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
    
    prim_img = imagens[0]

    marcadores, grafo, cor_por_no =  construir_modelo(prim_img, args)
    
    superpxs = mts.cromaticidade(prim_img, marcadores)

    figura = plt.figure(figsize=(8, 8))
    eixo = figura.add_axes([0.1, 0.3, 0.8, 0.6])

    sog = Isom(grafo, cor_por_no)

    for img in imagens[1:]:
        superpxs = mts.cromaticidade(img, marcadores(img))
        while not sog.convergiu():
            sog.epoca()
            



def segmentar_imagem(imagem, args):
    marcadores, grafo, marc_por_no = construir_modelo(imagem, args)
    visualizar_grafo_modelo(grafo, marcadores, imagem)


def visualizar_grafo_marcadores():
    pass


def visualizar_segmen_video(video, args):
    pass