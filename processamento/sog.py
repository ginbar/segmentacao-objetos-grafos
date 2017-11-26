
from scipy.spatial.distance import euclidean
import numpy as np
from random import shuffle
import math
import networkx as nx

from modelo.visualzacao import visualizar_grafo_marcadores



class Isom(object):


    def __init__(self, grafo, cooling=0.8, epocas=20):
        self.cooling = cooling
        self.grafo = grafo
        self.raio = 5
        self.raio_max = 5
        self.intervalo = 2
        self.raio_min = 1 
        self.adaptacao_min = 0.15
        self.adaptacao_max = 0.6
        self.intervalo = 3
        self.max_epocas = epocas
        self.epoca_atual = 1
        self.similaridades = []
        self.superpxs = None



    def novos_superpxs(self, superpxs):
        self.superpxs = superpxs
        self.epoca_atual = 1
        self.raio = 5



    def epoca(self):
        
        adaptacao = max(self.adaptacao_min, math.exp(-self.cooling * self.epoca_atual / self.max_epocas) * self.adaptacao_max)
        
        self.similaridades = self.calc_similaridades(self.grafo, self.superpxs) 

        superpxs = list(self.superpxs)

        shuffle(superpxs)

        for label_spx, _ in superpxs:
            vencedor = self.definir_vencedor(self.grafo, label_spx, self.similaridades)
            # Se no ha vencedor, quer dizer que o superpx foi considerado parte do background
            if vencedor is not None: 
                vizinhos_distancias = self.vizinhos(self.grafo, vencedor,  distancia=self.raio)
                for viz, dist in vizinhos_distancias:
                    self.grafo.node[viz]['momentos'] -= math.pow(2, -dist) * adaptacao 
                vizinhos = [vizinho for vizinho, _ in vizinhos_distancias]
                self.recalc_similaridades(vizinhos, self.superpxs, self.similaridades)

        print 'raio:{}, adaptacao:{}, epoca:{}'.format(self.raio, adaptacao, self.epoca_atual)

        self.epoca_atual += 1
  
        if self.epoca_atual % self.intervalo == 0 and self.raio > self.raio_min:
            self.raio -= 1



    def convergiu(self):
        return self.epoca_atual > self.max_epocas



    def definir_vencedor(self, grafo, indice_superpx, similaridades):
        indice_vencedor = np.argmin(similaridades[indice_superpx]) 
        return grafo.nodes()[indice_vencedor]
    


    def calc_similaridades(self, grafo, superpxs):
        return {label: [euclidean(momts, grafo.node[n]['momentos']) for n in grafo.nodes()] for (label, momts) in superpxs}



    def recalc_similaridades(self, alterados, superpxs, similaridades):
        nos = self.grafo.nodes()
        indices_alterados = [nos.index(alterado) for alterado in alterados]
        for label_spx, momentos in superpxs:
            for ind_alter in indices_alterados:
                similaridades[label_spx][ind_alter] = euclidean(momentos, self.grafo.node[nos[ind_alter]]['momentos'])
        


    def vizinhos(self, grafo, no, distancia=1):
        caminhos = nx.single_source_shortest_path_length(grafo, no, cutoff=distancia)
        return [(viz, dist) for viz, dist in caminhos.iteritems() if dist <= distancia and viz != no]



    def no_por_superpx(self):
        return [self.definir_vencedor(self.grafo, label_spx, self.similaridades) for label_spx, _ in self.superpxs]