
from pylab import *
from matplotlib.widgets import Button, RadioButtons
from  matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import numpy as np
import modelo.cores as cores 

class ConstrutorModelo(object):
    

    def __init__(self, imagem=None, marcadores=None, bordas=None, grafo=None):
        self.imagem = imagem
        self.marcadores = marcadores
        self.grafo = grafo
        self.marcador_por_superpixel = {}
        self.esta_prescionado = False
        self.marcados = set()

        self.cores = cores.opcoes_cores
        self.rgb_cor = cores.intensidade_por_cor



    def mostrar_figura(self, bloquear=True):
        self.figura = plt.figure(figsize=(8, 8))
        self.eixo = self.figura.add_axes([0.1, 0.3, 0.8, 0.6])
        
        self.larg_img = self.imagem.shape[0]  
        self.altu_img = self.imagem.shape[1]
        
        self.mascara = np.empty((self.larg_img, self.altu_img)) * np.nan

        self.figura.canvas.mpl_connect('button_press_event', self.prescionado)
        self.figura.canvas.mpl_connect('button_release_event', self.solto)
        self.figura.canvas.mpl_connect('motion_notify_event', self.movimentado)
        
        self.eixo.imshow(self.imagem)
        self.eixo.imshow(self.bordas)
        
        '''Configuracao dos botoes'''
        self.botao_criar = Button(plt.axes([0.85, 0.005, 0.1, 0.075]), 
            'Criar', color='green', hovercolor='blue')

        self.botao_reiniciar = Button(plt.axes([0.05, 0.005, 0.1, 0.075]), 
            'Reiniciar', color='red', hovercolor='blue')
        
        self.botao_criar.on_clicked(self.evento_botao_criar)
        self.botao_reiniciar.on_clicked(self.evento_botao_reiniciar)

        '''Configuracao seletor de cores'''
        self.seletor_cores = RadioButtons(plt.axes([0.38, 0.005, 0.2, 0.16]), self.cores)

        plt.show()



    def evento_botao_criar(self, evento):
        plt.close()



    def evento_botao_reiniciar(self, evento):
        self.mascara = np.empty((self.larg_img, self.altu_img)) * np.nan 
        self.marcador_por_superpixel.clear()
        self.eixo.clear()
        self.eixo.imshow(self.imagem)
        self.eixo.imshow(self.bordas)
        self.eixo.imshow(self.mascara)
        self.figura.canvas.draw()



    def extrair_modelo(self):
        subgrafo = self.grafo.subgraph(self.marcador_por_superpixel.keys())
        return self.marcadores, subgrafo, self.marcador_por_superpixel



    def prescionado(self, evento):
        self.esta_prescionado = True



    def solto(self, evento):
        self.esta_prescionado = False
        cor = self.rgb_cor[self.seletor_cores.value_selected]
        for marcador in self.marcados:
            np.putmask(self.mascara, self.marcadores == marcador, cor)
        self.eixo.clear()
        self.eixo.imshow(self.imagem)
        self.eixo.imshow(self.bordas)
        self.eixo.imshow(self.mascara, norm=Normalize(0, 100), cmap=cm.jet, alpha=.6)
        self.figura.canvas.draw()
        self.marcados.clear()



    def movimentado(self, evento):
        if self.esta_prescionado and evento.inaxes:
            x, y = int(evento.xdata), int(evento.ydata)
            marcador = self.marcadores[y, x]
            cor = self.seletor_cores.value_selected
            if cor == 'Apagar':
                self.marcados.discard(marcador)
                if marcador in self.marcador_por_superpixel:
                    self.marcador_por_superpixel.pop(marcador)
                    np.putmask(self.mascara, self.marcadores == marcador, np.nan)
            else: 
                self.marcados.add(marcador)
                self.marcador_por_superpixel[marcador] = cor 