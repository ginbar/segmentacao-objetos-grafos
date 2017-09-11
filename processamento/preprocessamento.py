
from processamento.segmentacao import marcad_bordas_grafo
from caracteristicas.momentos import cromaticidade
from armazenamento.segmentacoes import salvar_segmentacao

def preprocessar_video():
    pass

def preprocessar_imagem(imagem, args):
    marcadores, bordas, grafo = marcad_bordas_grafo(imagem, args)
    momentos = cromaticidade(imagem, marcadores)
    salvar_segmentacao()
