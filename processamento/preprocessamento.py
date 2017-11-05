
from os import path, makedirs
from os import listdir
from skimage.io import imread
import numpy as np

from skimage.color import rgb2gray
from skimage.segmentation import slic, watershed, random_walker, quickshift, felzenszwalb, mark_boundaries
from skimage.util import img_as_float
from skimage.filters import sobel

import caracteristicas.momentos as mts



def marcadores_e_bordas(imagem, args):
    '''
    Cons
    '''
    marcadores, bordas = None, None

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
    
    if not path.exists('cache'):
        makedirs('cache/imagens')
    
    dir_completo = 'cache/imagens/' + args.dirdest

    if not path.exists(dir_completo):
        makedirs(dir_completo)

    np.save(dir_completo + '/marcadores.npy', marcadores)
    np.save(dir_completo + '/bordas.npy', bordas)



def preprocessar_seq_imgs(imagens, args):
    """
    Preprocessa uma sequencia de imagens
    """
    
    if not path.exists('cache'):
        makedirs('cache/imagens')

    dir_completo = 'cache/imagens/' + args.dirdest

    for indice in range(len(imagens)):

        imagem = imagens[indice]

        marcadores, bordas = marcadores_e_bordas(imagem, args)
        momentos = mts.cromaticidade(imagem, marcadores)

        if not path.exists(dir_completo):
            makedirs(dir_completo)

        np.save( '{}/{}-momentos-{}'.format(dir_completo, args.dirdest, indice), momentos)
        np.save('{}/{}-marcadores-{}'.format(dir_completo, args.dirdest, indice), marcadores)
        np.save('{}/{}-bordas-{}'.format(dir_completo, args.dirdest, indice), bordas)



def carregar_prepros_seq_imagens(args):
    """
    Carrega os resultados de preprocessamento(marcadores, bordas e momentos)
    """
    diretorio = 'cache/imagens/' + args.dirdest
    
    arquivos = [path.join(diretorio, arq) for arq in listdir(diretorio) if path.isfile(path.join(diretorio, arq))]

    n_frames = len(arquivos) / 3

    marcs, bordas, momts = [], [], []

    for indice in range(n_frames):
        marcs.append(np.load('{}/{}-marcadores-{}.npy'.format(diretorio, args.dirdest, indice))) 
        bordas.append(np.load('{}/{}-bordas-{}.npy'.format(diretorio, args.dirdest, indice)))
        momts.append(np.load('{}/{}-momentos-{}.npy'.format(diretorio, args.dirdest, indice)))

    return marcs, bordas, momts



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
    algoritmo e parametros. 
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



def ler_seq_imagens(diretorio):
    """
    Ler uma sequencia de imagens dentro de um diretorio.
    """
    arquivos = [path.join(diretorio, arq) for arq in listdir(diretorio) if path.isfile(path.join(diretorio, arq))]
    arquivos.sort() # Lembrando que o formato dos arquivos deve ser <nome>-<numero>.<formato>
    imagens = [imread(arq) for arq in arquivos]
    return imagens