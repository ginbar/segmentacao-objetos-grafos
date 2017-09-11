
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.segmentation import slic, watershed, random_walker, quickshift, felzenszwalb, mark_boundaries
from skimage.future.graph import rag_mean_color, rag_boundary, show_rag
from skimage.util import img_as_float
from skimage.filters import sobel


def marcad_bordas_grafo(imagem, args):
    
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
        raise Error('Algoritmo de segmentacao nao suportado')

    grafo = rag_mean_color(imagem, marcadores, mode='similarity', connectivity=100)

    return marcadores, bordas, grafo