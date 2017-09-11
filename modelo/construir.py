
from modelo.construtor_modelo import ConstrutorModelo
from processamento.segmentacao import marcad_bordas_grafo


def construir_modelo(imagem, args):
    
    construtor = ConstrutorModelo(imagem)

    marcadores, bordas, grafo = marcad_bordas_grafo(imagem, args)

    construtor.marcadores = marcadores
    construtor.bordas = bordas
    construtor.grafo = grafo

    construtor.mostrar_figura()
    
    return construtor.extrair_grafo()

