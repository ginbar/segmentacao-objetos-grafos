
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage.io import imread
from skimage.future.graph import show_rag
from skimage import data
import argparse
import matplotlib.pyplot as plt

from caracteristicas.momentos import cromaticidade
from modelo.construir import construir_modelo 
from processamento.preprocessamento import preprocessar_video, preprocessar_imagem 


def main():

    parser = argparse.ArgumentParser(description='Segmentacao de objetos com grafos.')
    
    """Parametros obrigatorios"""
    parser.add_argument('-arq', type=str, 
        help='Arquivo para segmentacao.')
    
    """Parametros opcionais"""
    parser.add_argument('-video', type=bool, default=False,
        help='Algoritmo de segmentacao para construcao do modelo.')
    parser.add_argument('-prepros', type=bool, default=False,
        help='Preprocessar uma sequencia de video.')
    parser.add_argument('-dirdest', type=str, default='/teste',
        help='Diretorio de destino para o resultado do preprocessamento.')
    parser.add_argument('-cache', type=bool, default=False,
        help='Utilizar.')
    parser.add_argument('-sog', type=bool, default='isom',
        help='Algoritmo de grafos para propagacao da segmentacao.')
    parser.add_argument('-segm', type=str, default='slic',
        help='Algoritmo de segmentacao para construcao do modelo.')
    parser.add_argument('-segs', type=str, default='slic',
        help='Algoritmo de segmentacao para sequencia de video.')
    parser.add_argument('-k', type=int, default=100,
        help='Valor de k para o kmeans do slic.')
    parser.add_argument('-compactness', type=int, default=50,
        help='Compactness do slic|watershed.')
    parser.add_argument('-sigma', type=int, default=5,
        help='Kernel para a gaussiana do filtro.')
    parser.add_argument('-distmax', type=int, default=20, 
        help='Distancia maxima para o quickshift.')
    parser.add_argument('-filtro', type=str, default='sobel',
        help='Filtro de deteccao de bordas para o watershed.')
    parser.add_argument('-slico', type=bool, default=False, 
        help='Slic zero.')

    
    args = parser.parse_args()

    imagem = imread(args.arq)
    #imagem = data.horse()

    if args.prepros:
        preprocessar_imagem(args)        
    else:
        if args.dirdest is None:
            raise Error('Argumento -dirdist vazio.')
        marcadores, grafo, marc_por_no = construir_modelo(args)
        for no in grafo.nodes():
            print no, marc_por_no[no]
        show_rag(marcadores, grafo, imagem)
        plt.show()
    

if __name__ == '__main__':
    main()