
from skimage.io import imread
from skimage import data
import argparse

from processamento.preprocessamento import preprocessar_video, preprocessar_imagem, ler_seq_imagens, preprocessar_seq_imgs 
from processamento.segmentacao import segmentar_video, segmentar_imagem, visualizar_segmen_video, segmentar_seq_imagens
                                                                                        


def main():

    parser = argparse.ArgumentParser(description='Segmentacao de objetos com grafos.')
    
    """Parametros obrigatorios"""
    parser.add_argument('-arq', type=str, help='Arquivo para segmentacao.')
    
    """Parametros opcionais"""
    parser.add_argument('-formato', type=str, default='jpg',
        help='Formato do arquivo passado como parametro.')
    parser.add_argument('-tipo', type=str, default='seqimgs',
        help='Algoritmo de segmentacao para construcao do modelo.')
    parser.add_argument('-modo', type=str, default='segmen',
        help='Preprocessar uma sequencia de video.')
    parser.add_argument('-dirdest', type=str,
        help='Diretorio de destino para o resultado do preprocessamento.')
    parser.add_argument('-cache', type=bool, default=False,
        help='Utilizar.')
    parser.add_argument('-sog', type=bool, default='isom',
        help='Algoritmo de grafos para propagacao da segmentacao.')
    parser.add_argument('-segm', type=str, default='qcshift',
        help='Algoritmo de segmentacao para construcao do modelo.')
    parser.add_argument('-segs', type=str, default='quickshift',
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
    imagem = imread(args.arq) if args.tipo == 'imagem'  else None
    video = None if args.tipo == 'video' else None
    imagens = ler_seq_imagens(args.arq) if args.tipo == 'seqimgs' else None
    background = imread('{}/background.{}'.format(args.arq, args.formato)) if args.tipo == 'seqimgs' else None

    if args.modo == 'prepros' and args.tipo == 'imagem':
        preprocessar_imagem(imagem, args)
    elif args.modo == 'prepros' and args.tipo == 'video':
        preprocessar_video(video, args)        
    elif args.modo == 'visual':
        visualizar_segmen_video(video, args)
    elif args.modo == 'segmen' and args.tipo == 'imagem':
        segmentar_imagem(imagem, args)
    elif args.modo == 'segmen' and args.tipo == 'video':
        segmentar_video(video, args)
    elif args.modo == 'segmen' and args.tipo == 'seqimgs':
        segmentar_seq_imagens(imagens, args)
    elif args.modo == 'prepros' and args.tipo == 'seqimgs':
        preprocessar_seq_imgs(imagens, background, args)
    else:
        raise ValueError('Modo desconhecido.')

    # import numpy as np
    # import cv2

    # cap = cv2.VideoCapture(0)

    # # Define the codec and create VideoWriter object
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    # while(cap.isOpened()):
    #     ret, frame = cap.read()
    #     if ret==True:
    #         frame = cv2.flip(frame,0)

    #         # write the flipped frame
    #         out.write(frame)

    #         cv2.imshow('frame',frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #     else:
    #         break

    # # Release everything if job is finished
    # cap.release()
    # out.release()
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()