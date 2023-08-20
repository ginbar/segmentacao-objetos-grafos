
from scipy.spatial.distance import euclidean
import numpy as np
from random import shuffle
import math
import networkx as nx

from modelo.visualzacao import visualizar_grafo_marcadores



class Isom(object):


    def __init__(self, graph, normal_momts, num_momts, normal_centr, cooling=0.8, ratio=0.5, epocas=20):
        self.cooling = cooling
        self.graph = graph
        self.normal_centr = normal_centr
        self.normal_momts = normal_momts
        self.n_momts = num_momts
        self.radius = 5
        self.max_radius = 5
        self.min_radius = 1 
        self.min_adapting = 0.15
        self.max_adapting = 0.6
        self.interval = 3
        self.max_epochs = epocas
        self.current_epoch = 1
        self.similarities = []
        self.superpxs, self.centroides = None, None
        self.ratio = ratio




    def novos_superpxs(self, superpxs, centroides):
        self.superpxs = superpxs
        self.centroides = {label: centr for label, centr in centroides} 
        self.current_epoch = 1
        self.radius = 5




    def epoch(self):
        
        adapting = max(self.min_adapting, math.exp(-self.cooling * self.current_epoch / self.max_epochs) * self.max_adapting)
        
        self.similarities = self.calc_similarities(self.graph, self.superpxs) 

        superpxs = list(self.superpxs)

        shuffle(superpxs)

        for label_spx, _ in superpxs:
            winner = self.get_winner(self.graph, label_spx, self.similarities)
            # Se no ha vencedor, quer dizer que o superpx foi considerado parte do background
            if winner is not None: 
                neighbours_distances = self.get_neighbours(self.graph, winner, distance=self.radius)
                for neighbour, distance in neighbours_distances:
                    self.graph.node[neighbour]['momentos'] -= math.pow(2, -distance) * adapting
                    self.graph.node[neighbour]['centroide'] -= math.pow(2, -distance) * adapting 
                neighbours = [neighbour for neighbour, _ in neighbours_distances]
                self.recalc_similarities(neighbours)

        print('raio:{}, adaptacao:{}, epoca:{}'.format(self.radius, adapting, self.current_epoch))

        self.current_epoch += 1
  
        if self.current_epoch % self.interval == 0 and self.radius > self.min_radius:
            self.radius -= 1




    def has_converged(self):
        return self.current_epoch > self.max_epochs




    def get_winner(self, graph, superpx_index, similarities):
        winner_index = np.argmin(similarities[superpx_index]) 
        print(graph.nodes()[winner_index])
        return graph.nodes()[winner_index]
    



    def calc_similarities(self, graph, superpxs):
        
        simils, sqrt_num_momts = {}, math.sqrt(self.n_momts)

        for label, momts in superpxs:
        
            centr = self.centroides[label]
            simils[label] = range(self.graph.number_of_nodes())
            
            for index, node in enumerate(self.graph.nodes()):
                
                normalized_node_mts = np.divide(graph.node[node]['momentos'], self.normal_momts)
                normalized_mts_spx = np.divide(momts, self.normal_momts)
                
                dist_momts = euclidean(normalized_mts_spx, normalized_node_mts) / sqrt_num_momts
                dist_centr =  euclidean(centr, graph.node[node]['centroide']) / self.normal_centr
                
                simils[label][index] = dist_momts * self.ratio + dist_centr  * (1 - self.ratio) 
                # simils[label][indice] = euclidean(grafo.node[no]['momentos'], momts)

        return simils




    def recalc_similarities(self, alterados):
        
        nodes = self.graph.nodes()
        raiz_num_momts = math.sqrt(self.n_momts)
        indices_alterados = [nodes.index(alterado) for alterado in alterados]
        
        for label, moments in self.superpxs:
            
            centroide = self.centroides[label]
            
            for ind_alter in indices_alterados:
                mts_no_normalizados = np.divide(self.graph.node[nodes[ind_alter]]['momentos'], self.normal_momts)
                mts_spx_normalizados = np.divide(moments, self.normal_momts)
                
                dist_momts = euclidean(mts_spx_normalizados, mts_no_normalizados)
                dist_centr = euclidean(centroide, self.graph.node[nodes[ind_alter]]['centroide'])

                # self.similaridades[label][ind_alter] = (dist_momts / raiz_num_momts)* self.ratio + (dist_centr / self.normal_centr) * (1 - self.ratio)
                self.similarities[label][ind_alter] = euclidean(moments, self.graph.node[nodes[ind_alter]]['momentos'])




    def get_neighbours(self, graph, node, distance=1):
        paths = nx.single_source_shortest_path_length(graph, node, cutoff=distance)
        return [(neighbour, dist) for neighbour, dist in paths.iteritems() if dist <= distance and neighbour != node]




    def node_per_superpx(self):
        return [self.get_winner(self.graph, label_spx, self.similarities) for label_spx, _ in self.superpxs]