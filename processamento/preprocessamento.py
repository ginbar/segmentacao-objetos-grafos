
from os import path, makedirs
from skimage.io import imread
import numpy as np

from skimage.color import rgb2gray
from skimage.segmentation import slic, watershed, random_walker, quickshift, felzenszwalb, mark_boundaries
from skimage.util import img_as_float
from skimage.filters import sobel

from caracteristicas.momentos import cromaticidade


def marcadores_e_bordas(imagem, args):
    '''
    Cons
    '''
    marcadores = None
    bordas = None

    if args.segm == 'wtshed':
        imagem_cinza = rgb2gray(imagem) 
        bordas = sobel(imagem)
        marcadores = watershed(bordas, 100)
    elif args.segm =='rdwalker':
        alg_segmentacao = random_walker
    elif args.segm =='qcshift':
        marcadores = quickshift(imagem, max_dist=args.distmax, sigma=args.sigma)
        bordas = mark_boundaries(imagem, marcadores)
    elif args.segm == 'slic': 
        marcadores = slic(img_as_float(imagem), n_segments=args.k, 
            compactness=args.compactness, sigma=args.sigma, slic_zero=args.slico)
        bordas = mark_boundaries(imagem, marcadores)
    elif args.segm == 'felzenszwalb':
        marcadores = felzenszwalb(imagem, sigma=args.sigma)
        bordas = mark_boundaries(imagem, marcadores)
    else:
        raise ValueError('Algoritmo de segmentacao nao suportado')

    return marcadores, bordas


def preprocessar_video(video, args):
    pass


def preprocessar_imagem(imagem, args):

    marcadores, bordas = marcadores_e_bordas(imagem, args)
    momentos = cromaticidade(imagem, marcadores)
    
    if not path.exists('cache'):
        makedirs('cache/imagens')
    
    dir_completo = 'cache/imagens/' + args.dirdest

    if not path.exists(dir_completo):
        makedirs(dir_completo)

    np.save(dir_completo + '/marcadores.npy', marcadores)
    np.save(dir_completo + '/bordas.npy', bordas)
    #write_gexf(grafo, 'grafo.gexf')




def carregar_imagem_prepros(diretorio):
    dir_completo = 'cache/imagens/' + diretorio

    if not path.exists(dir_completo):
        raise Erro('Carregando de um diretorio inexistente')
    
    marcadores = np.load(dir_completo + '/marcadores.npy')
    bordas = np.load(dir_completo + '/bordas.npy')

    return marcadores, bordas


def marcadores(imagem, args):
    """
    Retorna os marcadores de uma imagem utilizando os argumentos para escolha do
    algoritmo e parametros 
    """
    if args.segm == 'wtshed':
        imagem_cinza = rgb2gray(imagem) 
        marcadores = watershed(bordas, 100)
    elif args.segm =='rdwalker':
        alg_segmentacao = random_walker
    elif args.segm =='qcshift':
        marcadores = quickshift(imagem, max_dist=args.distmax, sigma=args.sigma)
    elif args.segm == 'slic': 
        marcadores = slic(img_as_float(imagem), n_segments=args.k, 
            compactness=args.compactness, sigma=args.sigma, slic_zero=args.slico)
    elif args.segm == 'felzenszwalb':
        marcadores = felzenszwalb(imagem, sigma=args.sigma)
    else:
        raise ValueError('Algoritmo de segmentacao nao suportado')

    return marcadores
