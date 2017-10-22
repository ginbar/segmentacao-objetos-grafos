
from scipy.spatial.distance import euclidean
import numpy as np
from random import shuffle

from modelo.visualzacao import visualizar_grafo_marcadores


class Isom(object):


    def __init__(self, grafo, superpixels, cooling=0.8, epocas=20):
        self.superpixels = superpixels
        self.taxa_aprendizagem = tx_apren
        self.grafo = grafo
        self.mascara = np.array([])
        self.raio = 1
        self.raio_max = 5
        self.intervalo = 2
        self.raio_min = 1 
        self.adaptacao_min = 0.15
        self.adaptacao_max = 0.6
        self.cooling = cooling


    def epoca(self, parameter_list):
        
        adaptacao = max(self.adaptacao_min, math.exp(-self.cooling * self.epoca_atual / self.epocas) * self.adaptacao_max)
        
        self.similaridades = self.calc_similaridades(superpxs_grafo, superpxs)
        
        for spx in shuffle(superpxs):
            vencedor = definir_vencedor(grafo, spx, similaridades)
            # Se no ha vencedor, quer dizer que o superpx foi considerado parte do background
            if vencedor is not None: 
                vizinhos = self.vizinhos(self.grafo, vencedor,  distancia=self.raio)
                for viz in vizinhos:
                    viz.momentos = viz.momentos - math.pow(2, -1) * 1
                recalc_similiridades(vizinhos, superpxs, similaridades)
        
        epoca += 1
        if self.raio % intervalo == 0 and self.raio > self.raio_min:
            self.raio -= 1


    def covergiu(self):
        return self.epoca_atual > self.epocas


    def definir_vencedor(self, grafo, superpx, similaridades):
        indices = np.argmin(similaridade, superpx.label) 
        if similar > 2: 
            return None
        return indeces[0]
    

    def calc_similaridades(self, superpxs_grafo, nos, superpxs):
        return np.array([euclidean(spx.momentos, superpxs_grafo[n]) for spx in superpxs for n in nos])


    def recalc_similaridades(self, alterados, superpxs, similaridades):
        for spx in superpxs:
            for alter in alterados:
                similaridades[superpxs.marcador, alter] = euclidean(superpxs.momentos, superpxs_grafo[alter])


    def vizinhos(self, grafo, no, distancia=1):
         caminhos = nx.single_source_dijkstra_path_length(grafo, no)
         return [(no, dist) for no, dist in caminhos.iteritems() if dist <= distancia]