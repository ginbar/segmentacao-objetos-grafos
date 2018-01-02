
from os import path, makedirs
from os import listdir
from skimage.io import imread
import numpy as np
import cv2
from skimage.color import rgb2gray
from skimage.segmentation import slic, watershed, random_walker, quickshift, felzenszwalb, mark_boundaries
from skimage.util import img_as_float
from skimage.filters import sobel
from skimage.measure import regionprops

import skimage.io as io


import caracteristicas.momentos as mts

"""

"""

def marcadores_e_bordas(imagem, args):
    '''
    Cons
    '''
    marcadores, bordas = calc_marcadores(imagem, args), None

    if args.segm == 'wtshed':
        imagem_cinza = rgb2gray(imagem) 
        bordas = sobel(imagem)
    elif args.segm =='qcshift':
        bordas = mark_boundaries(imagem, marcadores)
    elif args.segm == 'slic': 
        bordas = mark_boundaries(imagem, marcadores)
    elif args.segm == 'felzenszwalb':
        bordas = mark_boundaries(imagem, marcadores)
    else:
        raise ValueError('Algoritmo de segmentacao nao suportado')

    return marcadores, bordas




def preprocessar_video(video, background, args):
    
    if not path.exists('cache/video'):
        makedirs('cache/video')

    dir_completo = 'cache/video/' + args.dirdest

    if not path.exists(dir_completo):
        makedirs(dir_completo)

    bksubtr = cv2.bgsegm.createBackgroundSubtractorMOG()

    bksubtr.apply(background, learningRate=0)

    while video.isOpened():
 
        _, frame = video.read()

        masc_bkground = bksubtr.apply(frame, learningRate=0.5)

        marcadores, bordas = marcadores_e_bordas(imagem, args)
        momentos = mts.cromaticidade(imagem, marcadores, masc_bkground)

        np.save( '{}/{}-momentos-{}'.format(dir_completo, args.dirdest, indice), momentos)
        np.save('{}/{}-marcadores-{}'.format(dir_completo, args.dirdest, indice), marcadores)
        np.save('{}/{}-bordas-{}'.format(dir_completo, args.dirdest, indice), bordas)
 

    # for indice in range(len(imagens)): 
        
    #     imagem = imagens[indice]
    #     masc_bkground = bksubtr.apply(imagem, learningRate=0.5) 

    #     marcadores, bordas = marcadores_e_bordas(imagem, args)
    #     momentos = mts.cromaticidade(imagem, marcadores, masc_bkground)

    #     np.save( '{}/{}-momentos-{}'.format(dir_completo, args.dirdest, indice), momentos)
    #     np.save('{}/{}-marcadores-{}'.format(dir_completo, args.dirdest, indice), marcadores)
    #     np.save('{}/{}-bordas-{}'.format(dir_completo, args.dirdest, indice), bordas)
   



def preprocessar_imagem(imagem, args):

    marcadores, bordas = marcadores_e_bordas(imagem, args)

    print mts.cromaticidade(imagem, marcadores)

    if not path.exists('cache'):
        makedirs('cache/imagens')
    
    dir_completo = 'cache/imagens/' + args.dirdest

    if not path.exists(dir_completo):
        makedirs(dir_completo)

    np.save(dir_completo + '/marcadores.npy', marcadores)
    np.save(dir_completo + '/bordas.npy', bordas)




def preprocessar_seq_imgs(imagens, background, args):
    """
    Preprocessa uma sequencia de imagens
    """
    
    if not path.exists('cache'):
        makedirs('cache/imagens')

    dir_completo = 'cache/imagens/' + args.dirdest

    if not path.exists(dir_completo):
        makedirs(dir_completo)

    # Treina o subtrador para detectar o fundo
    # bksubtr.apply(background, learningRate=0)

    for indice, imagem in enumerate(imagens): 
        
        bksubtr = cv2.bgsegm.createBackgroundSubtractorMOG()

        if indice != 0:
            bksubtr.apply(background, learningRate=0)

        masc_bkground = bksubtr.apply(imagem, learningRate=0.5) if indice != 0 else None 

        marcadores, bordas = marcadores_e_bordas(imagem, args)
        
        momentos = mts.cromaticidade(imagem, marcadores, mascbkgnd=masc_bkground)
        
        propriedades = regionprops(marcadores)
        centroides = np.array([(label, propriedades[label - 1].centroid) for (label, _) in momentos], dtype=object) 
        
        np.save( '{}/{}-centroides-{}'.format(dir_completo, args.dirdest, indice), centroides)
        np.save( '{}/{}-momentos-{}'.format(dir_completo, args.dirdest, indice), momentos)
        np.save('{}/{}-marcadores-{}'.format(dir_completo, args.dirdest, indice), marcadores)
        np.save('{}/{}-bordas-{}'.format(dir_completo, args.dirdest, indice), bordas)




def carregar_prepros_seq_imagens(args):
    """
    Carrega os resultados de preprocessamento(marcadores, bordas e momentos)
    """
    diretorio = 'cache/imagens/' + args.dirdest
    
    arquivos = [path.join(diretorio, arq) for arq in listdir(diretorio) if path.isfile(path.join(diretorio, arq))]

    n_frames = len(arquivos) / 4 # n matrizes para bordas, marcadores, centroides e momentos

    marcs, bordas, momts, centrs = [], [], [], []

    for indice in range(n_frames):
        marcs.append(np.load('{}/{}-marcadores-{}.npy'.format(diretorio, args.dirdest, indice))) 
        bordas.append(np.load('{}/{}-bordas-{}.npy'.format(diretorio, args.dirdest, indice)))
        momts.append(np.load('{}/{}-momentos-{}.npy'.format(diretorio, args.dirdest, indice)))
        centrs.append(np.load('{}/{}-centroides-{}.npy'.format(diretorio, args.dirdest, indice)))

    return marcs, bordas, momts, centrs




def carregar_imagem_prepros(diretorio):
    dir_completo = 'cache/imagens/' + diretorio

    if not path.exists(dir_completo):
        raise Erro('Carregando de um diretorio inexistente')
    
    marcadores = np.load(dir_completo + '/marcadores.npy')
    bordas = np.load(dir_completo + '/bordas.npy')

    return marcadores, bordas




def calc_marcadores(imagem, args):
    """
    Retorna os marcadores de uma imagem utilizando os argumentos para escolha do
    algoritmo e parametros. 
    """
    marcadores = None

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
    imagens = [imread(arq) for arq in arquivos if 'background' not in arq]
    return imagens