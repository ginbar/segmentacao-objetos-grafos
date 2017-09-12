from os import path, makedirs

from processamento.segmentacao import marcad_bordas_grafo
from caracteristicas.momentos import cromaticidade
from armazenamento.segmentacoes import salvar_segmentacao

def preprocessar_video():
    pass

def preprocessar_imagem(imagem, args):
    
    marcadores, bordas, grafo = marcad_bordas_grafo(imagem, args)
    momentos = cromaticidade(imagem, marcadores)
    
    if not path.exists('preprocessamento'):
        makedirs('preprocessamento')
    
    dir_completo = 'preprocessamento/' + args.dirdist

    if not path.exists(dir_completo):
        makedirs(dir_completo)

    
