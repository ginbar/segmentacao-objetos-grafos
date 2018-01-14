
"""
Docad
"""

from __future__ import division

from math import pow
from itertools import product, islice, permutations, combinations
from caracteristicas.superpixel import SuperPixel
from skimage.color import rgb2xyz
import numpy as np 



def cromaticidade(imagem, marcadores, mascbkgnd=None, numero_momentos=5):
    """
    Extrair momentos de cromaticidade.    
    """

    img_xyz = rgb2xyz(imagem)
    superpixels = separar_superpx(img_xyz, marcadores) if mascbkgnd is None else superpxs_de_objeto(img_xyz, marcadores, mascbkgnd)
    
    espacos_xy = [espaco_xy(pixels) for (_, pixels) in superpixels]
    matrizes = [criar_matriz(xy) for xy in espacos_xy]
    indices = indices_momentos(numero_momentos)
    momentos = np.array([[momentos_por_indices(matriz, m, l) for m, l in indices] for matriz in matrizes])
        
    return np.array([(label, np.append(mts[:, 0], mts[:, 1])) for (label, _), mts in zip(superpixels, momentos)], dtype=object)



def superpxs_de_objeto(imagem, marcadores, mascbkgnd, porcent=0.5):
    labels = enumerate(np.unique(marcadores))
    px_obj_por_spx = [(label, imagem[np.logical_and(marcadores == label, mascbkgnd != 0)]) for (_, label) in labels]        
    labels = enumerate(np.unique(marcadores))
    superpxs = [(label, imagem[marcadores == label]) for (_, label) in labels]
    return [spx_obj for (spx, spx_obj) in zip(superpxs, px_obj_por_spx) if (len(spx_obj[1]) / len(spx[1])) > porcent]    



def cromaticidade_sem_mascara(imagem, marcadores, numero_momentos=5):
    """
    Extrair momentos de cromaticidade.    
    """

    superpixels = separar_superpx(rgb2xyz(imagem), marcadores)

    espacos_xy = [espaco_xy(pixels) for (_, pixels) in superpixels]
    
    matrizes = [criar_matriz(xy) for xy in espacos_xy]

    indices = indices_momentos(numero_momentos)
    
    momentos = np.array([[momentos_por_indices(matriz, m, l) for m, l in indices] for matriz in matrizes])
    
    return np.array([np.append(mts[:, 0], mts[:, 1]) for (label, _), mts in zip(superpixels, momentos)]) 

# comentar tempo de processamento 
# usar a mascara de segmentacao


def separar_superpx(imagem, marcadores):
    labels = enumerate(np.unique(marcadores))    
    return [(label, imagem[marcadores == label]) for (_, label) in labels]



def espaco_xy(valores_rgb):
    return np.array([xyz_para_xy(rgb) for rgb in valores_rgb])    



def xyz_para_xy(xyz):
    X, Y, Z = xyz
    soma = X + Y + Z
    if soma == 0:
        return (0, 0)
    else:
        return (int((X / soma) * 100), int((Y / soma) * 100))



def criar_matriz(valores_xy):
    T = np.array([[0 for _ in range(101)] for _ in range(101)], dtype=int)
    for x, y in valores_xy:
        T[x, y] += 1
    return T



def momentos_por_indices(matriz, m, l):
    somatorio_t, somatorio_d = 0, 0
    for x in range(100):
        for y in range(100):
            valor = matriz[x][y]
            if valor > 0:    
                somatorio_t += pow(x, m) * pow(y, l) * 1
            somatorio_d += pow(x, m) * pow(y, l) * valor
    return somatorio_t, somatorio_d



def indices_momentos(numero):
    valores = range(numero // 2 + 1)
    combinacoes = product(valores, repeat=2)  
    validos = [(x,y) for x, y in combinacoes if x == 0 or y == 0]    
    return list(islice(validos, numero))



def porcent_spxs(numerador, denominador):
    len_num, len_den = len(numerador[1]), len(denominador[1]) 
    return 0 if len_den == 0 else numerador / denominador