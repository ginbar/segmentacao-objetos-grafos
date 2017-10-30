
from skimage.io import imread
from skimage.future.graph import rag_mean_color
import networkx as nx

from modelo.construtor_modelo import ConstrutorModelo
from processamento.preprocessamento import carregar_imagem_prepros, marcadores_e_bordas


def construir_modelo(imagem, marcadores, bordas, args):
    
    construtor = ConstrutorModelo(imagem)
    
    construtor.marcadores = marcadores
    construtor.bordas = bordas
    construtor.grafo = rag_mean_color(imagem, marcadores)
    
    construtor.mostrar_figura()
    
    marcadores, subgrafo, marc_por_superpx = construtor.extrair_modelo()   
    
    nx.set_node_attributes(subgrafo, 'cor', marc_por_superpx)
    
    return marcadores, subgrafo


def salvar_modelo(marcadores, grafo, marc_por_no):
    pass
