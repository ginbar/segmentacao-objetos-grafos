
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from  matplotlib.colors import Normalize
from pylab import cm
from os import path, makedirs
from os import listdir
import time
import numpy as np

from preprocessamento import read_bkg_and_images


index_masc = 0

def salvar_mascaras_seq_imagens(mascaras, args):

    diretorio = 'resultados/' + args.dirdest

    _criar_ser_nao_existe('resultados')
    _criar_ser_nao_existe(diretorio)
    
    digitos = len(str(len(mascaras))) # numero de digitos que o numero de mascaras tem

    for indice, mascara in enumerate(mascaras):
        np.save( '{}/{}-segmentacao-{}'.format(diretorio, args.dirdest, str(indice).zfill(digitos)), mascara)



def ler_mascaras_seq_imagens(args):
    diretorio = 'resultados/' + args.dirdest
    arqs = [path.join(diretorio, arq) for arq in listdir(diretorio) if path.isfile(path.join(diretorio, arq))]
    arqs.sort()
    for arq in arqs:
        print(arq)
    return [np.load(arq) for arq in arqs]



def mudar_visualizacao(imagens, mascaras, eixo, figura):
    
    global index_masc

    if index_masc == len(mascaras):
        plt.close()
    else:        
        eixo.clear()
        eixo.imshow(imagens[index_masc])
        eixo.imshow(mascaras[index_masc], norm=Normalize(0, 100), cmap=cm.jet, alpha=.6)
        figura.canvas.draw()
    
    index_masc = index_masc + 1



def visualizar_segm_seq_imagens(imagens, args):

    diretorio = 'imagens/' + args.dirdest

    mascaras = ler_mascaras_seq_imagens(args)

    # print mascaras

    figura = plt.figure(figsize=(8, 8))
    eixo = figura.add_axes([0.1, 0.3, 0.8, 0.6])

    botao_prox = Button(plt.axes([0.85, 0.005, 0.1, 0.075]), 
            '>', color='green', hovercolor='blue')    

    index = 0

    botao_prox.on_clicked(lambda evento: mudar_visualizacao(imagens, mascaras, eixo, figura))

    plt.show()



def _criar_ser_nao_existe(diretorio):
    if not path.exists(diretorio):
        makedirs(diretorio)
