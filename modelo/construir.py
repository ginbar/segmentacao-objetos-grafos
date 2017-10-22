
from skimage.io import imread
from skimage.future.graph import rag_mean_color

from modelo.construtor_modelo import ConstrutorModelo
from processamento.preprocessamento import carregar_imagem_prepros, marcadores_e_bordas


def construir_modelo(imagem, args):
    
    construtor = ConstrutorModelo(imagem)
    marcadores, bordas = None, None

    if args.cache:
        marcadores, bordas = carregar_imagem_prepros(args.dirdest)
    else:
        marcadores, bordas = marcadores_e_bordas(imagem, args)

    construtor.marcadores = marcadores
    construtor.bordas = bordas
    construtor.grafo = rag_mean_color(imagem, marcadores)
    
    construtor.mostrar_figura()
    
    return construtor.extrair_modelo()


def salvar_modelo(marcadores, grafo, marc_por_no):
    pass
