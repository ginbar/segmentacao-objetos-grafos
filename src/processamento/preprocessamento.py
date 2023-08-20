
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



def labels_and_borders(image, args):
    '''
    Cons
    '''
    labels, borders = get_labels_and_borders(image, args), None

    if args.segm == 'wtshed':
        grey_image = rgb2gray(image) 
        borders = sobel(image)
    elif args.segm =='qcshift' or args.segm == 'slic' or args.segm == 'felzenszwalb':
        borders = mark_boundaries(image, labels)
    else:
        raise ValueError('Algoritmo de segmentacao nao suportado')

    return labels, borders




def preprocessar_video(video, background, args):
    
    if not path.exists('cache/video'):
        makedirs('cache/video')

    full_directory = 'cache/video/' + args.dirdest

    if not path.exists(full_directory):
        makedirs(full_directory)

    bksubtr = cv2.bgsegm.createBackgroundSubtractorMOG()

    bksubtr.apply(background, learningRate=0)

    while video.isOpened():
 
        _, frame = video.read()

        masc_bkground = bksubtr.apply(frame, learningRate=0.5)

        marcadores, bordas = labels_and_borders(imagem, args)
        momentos = mts.cromaticidade(imagem, marcadores, masc_bkground)

        np.save( '{}/{}-momentos-{}'.format(full_directory, args.dirdest, indice), momentos)
        np.save('{}/{}-marcadores-{}'.format(full_directory, args.dirdest, indice), marcadores)
        np.save('{}/{}-bordas-{}'.format(full_directory, args.dirdest, indice), bordas)



def preprocessar_imagem(imagem, args):

    marcadores, bordas = labels_and_borders(imagem, args)

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

    bksubtr, masc_bkground = None, None

    for indice, imagem in enumerate(imagens): 

        if indice != 0:
            bksubtr = cv2.bgsegm.createBackgroundSubtractorMOG()
            bksubtr.apply(background, learningRate=0)               
            masc_bkground = bksubtr.apply(imagem, learningRate=0.5)  

        marcadores, bordas = labels_and_borders(imagem, args)
        
        momentos = mts.cromaticidade(imagem, marcadores, mascbkgnd=masc_bkground)

        propriedades = regionprops(marcadores)
        centroides = np.array([(label, np.array(propriedades[label - 1].centroid)) for (label, _) in momentos], dtype=object) 

        np.save( '{}/{}-centroides-{}'.format(dir_completo, args.dirdest, indice), centroides)
        np.save( '{}/{}-momentos-{}'.format(dir_completo, args.dirdest, indice), momentos)
        np.save('{}/{}-marcadores-{}'.format(dir_completo, args.dirdest, indice), marcadores)
        np.save('{}/{}-bordas-{}'.format(dir_completo, args.dirdest, indice), bordas)




def load_processement(args):
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




def load_processed_images(directory):
    full_directory = 'cache/imagens/' + directory

    if not path.exists(full_directory):
        raise Erro('Carregando de um diretorio inexistente')
    
    labels = np.load(full_directory + '/marcadores.npy')
    borders = np.load(full_directory + '/bordas.npy')

    return labels, borders




def get_labels_and_borders(image, args):
    """
    Retorna os marcadores de uma imagem utilizando os argumentos para escolha do
    algoritmo e parametros. 
    """
    markers = None

    if args.segm == 'wtshed':
        imagem_cinza = rgb2gray(image) 
        markers = watershed(bordas, 100)
    elif args.segm =='rdwalker':
        alg_segmentacao = random_walker
    elif args.segm =='qcshift':
        markers = quickshift(image, max_dist=args.distmax, sigma=args.sigma)
    elif args.segm == 'slic': 
        markers = slic(img_as_float(image), n_segments=args.k, 
            compactness=args.compactness, sigma=args.sigma, slic_zero=args.slico)
    elif args.segm == 'felzenszwalb':
        markers = felzenszwalb(image, sigma=args.sigma)
    else:
        raise ValueError('Algoritmo de segmentacao nao suportado')

    return markers




def read_bkg_and_images(directory):
    """
    Ler uma sequencia de imagens dentro de um diretorio.
    """
    files = [path.join(directory, file_name) for file_name in listdir(directory) if path.isfile(path.join(directory, file_name))]

    files.sort() # Lembrando que o formato dos arquivos deve ser <nome>-<numero>.<formato>
    images = [imread(arq) for arq in files if 'background' not in arq]
    
    backgrounds = [imread(arq) for arq in files if 'background' in arq]
    background = backgrounds[0] if len(backgrounds) > 0 else None

    return background, images