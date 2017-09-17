
from os import path, makedirs
from skimage.io import imread
import numpy as np

from processamento.segmentacao import marcadores_e_bordas
from caracteristicas.momentos import cromaticidade

def preprocessar_video():
    pass


def preprocessar_imagem(args):

    imagem = imread(args.arq)

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