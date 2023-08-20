
from pylab import *
from matplotlib.widgets import Button, RadioButtons
from  matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import modelo.cores as cores 

color_options = ('Azul', 'Vermelho', 'Verde', 'Amarelo',  'Laranja', 'Turquesa', 'Apagar')

intensity_per_color = {
    'Azul':  0, 
    'Vermelho': 100, 
    'Verde':  50, 
    'Amarelo': 65, 
    'Laranja': 80, 
    'Turquesa': 40, 
    'Apagar': None
}


class ModelConstructionUI(object):


    def __init__(self, image=None, labels=None, borders=None, graph=None):
        self.image = image
        self.labels = labels
        self.graph = graph
        self.label_by_superpixel = {}
        self.is_pressed = False
        self.touched_clusters = set()



    def show(self):
        self.figure = plt.figure(figsize=(8, 8))
        self.axis = self.figure.add_axes([0.1, 0.3, 0.8, 0.6])
        
        self.img_width = self.image.shape[0]
        self.img_height = self.image.shape[1]
        
        self.mask = np.empty((self.img_width, self.img_height)) * np.nan

        self.figure.canvas.mpl_connect('button_press_event', self._press_event)
        self.figure.canvas.mpl_connect('button_release_event', self._release_event)
        self.figure.canvas.mpl_connect('motion_notify_event', self._motion_event)
        
        self.axis.imshow(self.image)
        self.axis.imshow(self.borders)
        
        '''Configuracao dos botoes'''
        self.create_btn = Button(plt.axes([0.85, 0.005, 0.1, 0.075]), 
            'Criar', color='green', hovercolor='blue')

        self.reset_btn = Button(plt.axes([0.05, 0.005, 0.1, 0.075]), 
            'Reiniciar', color='red', hovercolor='blue')
        
        self.create_btn.on_clicked(self._create_btn_event)
        self.reset_btn.on_clicked(self._reset_btn_event)

        '''Configuracao seletor de cores'''
        self.color_selector = RadioButtons(plt.axes([0.38, 0.005, 0.2, 0.16]), color_options)

        plt.show()



    def get_model(self):
        subgraph = self.graph.subgraph(self.label_by_superpixel.keys())
        nx.set_node_attributes(subgraph, 'cor', self.label_by_superpixel)
        return  subgraph, self.mask



    def _create_btn_event(self, evento):
        plt.close()



    def _reset_btn_event(self, evento):
        self.mask = np.empty((self.img_width, self.img_height)) * np.nan 
        self.label_by_superpixel.clear()
        self.axis.clear()
        self.axis.imshow(self.image)
        self.axis.imshow(self.borders)
        self.axis.imshow(self.mask)
        self.figure.canvas.draw()



    def _press_event(self, evento):
        self.is_pressed = True



    def _release_event(self, evento):
        self.is_pressed = False
        color = intensity_per_color[self.color_selector.value_selected]
        
        for label in self.touched_clusters:
            np.putmask(self.mask, self.labels == label, color)
        
        self.axis.clear()
        
        self.axis.imshow(self.image)
        self.axis.imshow(self.borders)
        self.axis.imshow(self.mask, norm=Normalize(0, 100), cmap=cm.jet, alpha=.6)
        
        self.figure.canvas.draw()
        self.touched_clusters.clear()



    def _motion_event(self, event):
        if self.is_pressed and event.inaxes:
            x, y = int(event.xdata), int(event.ydata)
            label = self.labels[y, x]
            color = self.color_selector.value_selected
            if color == 'Apagar':
                self.touched_clusters.discard(label)
                if label in self.label_by_superpixel:
                    self.label_by_superpixel.pop(label)
                    np.putmask(self.mask, self.labels == label, np.nan)
            else: 
                self.touched_clusters.add(label)
                self.label_by_superpixel[label] = color
