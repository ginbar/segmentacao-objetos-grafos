
"""
Docad
"""

from math import pow
from itertools import product, islice, permutations, combinations
from caracteristicas.superpixel import SuperPixel
from skimage.color import rgb2xyz
import numpy as np 



def cromaticidade(imagem, marcadores, numero_momentos=5):
    """
    Extrair momentos de cromaticidade.    
    """

    superpixels = separar_superpixels(rgb2xyz(imagem), marcadores)

    espacos_xy = [espaco_xy(pixels) for (_, pixels) in superpixels]
    
    matrizes = [criar_matriz(xy) for xy in espacos_xy]

    indices = indices_momentos(numero_momentos)
    
    momentos = np.array([[momentos_por_indices(matriz, m, l) for m, l in indices] for matriz in matrizes])
    
    return [SuperPixel(label, mts[:, 0], mts[:, 1]) for (label, _), mts in zip(superpixels, momentos)]



def separar_superpixels(imagem, marcadores):
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
    T = [[0 for _ in range(101)] for _ in range(101)]
    for x, y in valores_xy:
        T[x][y] += 1
    return np.array(T, dtype=int)



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
    valores = range(numero / 2 + 1)
    combinacoes = product(valores, repeat=2)  
    validos = [(x,y) for x, y in combinacoes if x == 0 or y == 0]    
    return list(islice(validos, numero))