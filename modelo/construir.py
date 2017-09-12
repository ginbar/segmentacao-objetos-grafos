
from skimage.io import imread
from skimage.future.graph import rag_mean_color

from modelo.construtor_modelo import ConstrutorModelo
from processamento.segmentacao import marcadores_e_bordas
from processamento.preprocessamento import carregar_imagem_prepros

def construir_modelo(args):
    
    imagem = imread(args.arq)

    construtor = ConstrutorModelo(imagem)

    marcadores, bordas = None, None

    if args.cache:
        marcadores, bordas = carregar_imagem_prepros(args.dirdest)
        print imagem, marcadores
    else:
        marcadores, bordas = marcadores_e_bordas(imagem, args)

    construtor.marcadores = marcadores
    construtor.bordas = bordas
    construtor.grafo = rag_mean_color(imagem, marcadores)

    construtor.mostrar_figura()
    
    return construtor.extrair_grafo()

