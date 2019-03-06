"""Une classe generique pour representer un graphe."""
# D100 : missing docstring in public module


class Graph(object):
    """Une classe generique pour representer un graphe."""

    def __init__(self, name='Sans nom'):
        """Initialisation du graphe."""
        self.__name = name
        self.__nodes = []   # Attribut prive.
        self.__edges = []
        self.__mat_adj = {}
        self.__pi = []
        self.__v = []

    def add_node(self, node):
        """Ajoute un noeud au graphe."""
        if node not in self.__mat_adj:
            self.__nodes.append(node)
            self.__mat_adj[node] = {}

    def add_edge(self, edge):
        """Ajoute une arete."""
        if (edge.get_startnode() != edge.get_endnode()):
            self.__edges.append(edge)
            self.__mat_adj[edge.start][edge.end] = edge
            self.__mat_adj[edge.end][edge.start] = edge

    def edge_exist(self, node_a, node_b):
        """Verifie si l arete existe."""
        if node_a in self.__mat_adj:
            if node_b in self.__mat_adj[node_a]:
                return True
        return False

    def get_edge_cost(self, node_a, node_b):
        """Retourne le cout de l arete si elle existe, infini sinon."""
        if not self.edge_exist(node_a, node_b):
            return float('Inf')
        else:
            return self.__mat_adj[node_a][node_b].get_cost()

    def delete_node(self, node):
        """Enleve le noeud et les arretes associe."""
        del self.__mat_adj[node]
        for edge in self.__edges:
            if edge.get_endnode() == node:
                if self.edge_exist(edge.start, edge.end):
                    del self.__mat_adj[edge.start][edge.end]
        for edge in self.__edges:
            if edge.get_endnode() == node:
                if self.edge_exist(edge.start, edge.end):
                    del self.__mat_adj[edge.start][edge.end]
        for edge in self.__edges:  # Le processus est repete deux fois a cause
                                    # D un bug qui ne retire pas tout ce qui
                                    # est associe
            if edge.end == node or edge.start == node:
                self.__edges.remove(edge)
        for edge in self.__edges:
            if edge.end == node or edge.start == node:
                self.__edges.remove(edge)
        self.__nodes.remove(node)

    def delete_edge(self, node1, node2):
        """Efface l'arrete entre le node1 et node2."""
        for node in self.__nodes:
            if node1.get_id() == node.get_id():
                key1 = node
            if node2.get_id() == node.get_id():
                key2 = node
        if self.edge_exist(key1, key2):
            if self.__mat_adj[key1][key2] in self.__edges:
                self.__edges.remove(self.__mat_adj[key1][key2])
            del self.__mat_adj[key1][key2]
        if self.edge_exist(node2, node1):
            if self.__mat_adj[key2][key1] in self.__edges:
                self.__edges.remove(self.__mat_adj[key2][key1])
            del self.__mat_adj[key2][key1]

    def get_name(self):
        """Donne le nom du graphe."""
        return self.__name

    def get_nodes(self):
        """Donne la liste des noeuds du graphe."""
        return self.__nodes

    def get_edge_copy(self, node1, node2):
        """Retourne une arrete a partir des id."""
        for node in self.__nodes:
            if node.get_id() == node1.get_id():
                node1 = node
            elif node.get_id() == node2.get_id():
                node2 = node
        if self.edge_exist(node1, node2):
            return self.__mat_adj[node1][node2]
        if self.edge_exist(node2, node1):
            return self.__mat_adj[node2][node1]

    def get_edges(self):
        """Donne la liste des aretes du graphe."""
        return self.__edges

    def get_nb_nodes(self):
        """Donne le nombre de noeuds du graphe."""
        return len(self.__nodes)

    def get_nb_edges(self):
        """Donne le nombre d'aretes du graphe."""
        return len(self.__edges)

    def get_mat_adj(self):
        """Retourne la matrice d adjacence."""
        return self.__mat_adj

    def get_neighbors(self, node):
        """Retourne les voisins d un noeud dans lorde des id."""
        for nodez in self.nodes:
            if node.get_id() == nodez.get_id():
                node = nodez
        nodes = self.__mat_adj[node].keys()
        for i in xrange(0, len(nodes)):
            for j in xrange(0, len(nodes)):
                if i != j:
                    if nodes[i].get_id() < nodes[j].get_id():
                        nodes[i], nodes[j] = nodes[j], nodes[i]
        return nodes

    def get_nb_neighbors(self, node):
        """Retourne les voisins d un noeud."""
        return len(self.__mat_adj[node].keys())

    def get_cost(self):
        """Retourne le cout du graphe."""
        cost = 0
        for edge in self.__edges:
            cost += edge.get_cost()
        return cost

    def get_vcost(self):
        """Retourne le cout du graphe de HK."""
        cost = 0
        for edge in self.__edges:
            cost += edge.get_vcost()
        return cost

    def get_pi(self):
        """Retourne le vecteur pi de HK."""
        self.__pi = []
        for node in self.__nodes:
            self.__pi.append(node.pi)
        return self.__pi

    def get_v(self):
        """Retourne le vecteur v de HK."""
        self.__v = []
        for node in self.__nodes:
            self.__v.append(self.get_nb_neighbors(node)-2)
        return self.__v

    def print_cost_matrix(self):
        """Affiche la sous-matrice inferieure des couts."""
        s = 'Sous-matrice des couts \n'
        for node_i in xrange(self.get_nb_nodes()):
            for node_j in xrange(self.get_nb_nodes()):
                if node_i >= node_j:
                    if self.edge_exist(self.get_nodes()[node_i],
                                       self.get_nodes()[node_j]):
                        s += '%.1f' % (self.get_edge_cost(
                                                    self.get_nodes()[node_i],
                                                    self.get_nodes()[node_j]))
                        s += ' '
                    else:
                        s += '%.1f' % float('Inf') + ' '
            s += '\n'
        print s

    def print_adjacence_matrix(self):
        """Affiche la sous-matrice inferieure de precedences."""
        s = 'Sous-matrice inferieure d adjacence \n'
        for node_i in xrange(self.get_nb_nodes()):
            for node_j in xrange(self.get_nb_nodes()):
                if node_i >= node_j:
                    s += '%d' % (self.edge_exist(self.get_nodes()[node_i],
                                                 self.get_nodes()[node_j]))
                    s += ' '
            s += '\n'
        print s

    def __repr__(self):
        """Represente le graphe."""
        name = self.get_name()
        nb_nodes = self.get_nb_nodes()
        nb_edges = self.get_nb_edges()
        s = 'Graphe %s comprenant %d noeuds et %d arretes' % (name, nb_nodes,
                                                              nb_edges)
        s += ' \n L ensemble des noeud du graphe :   '
        for node in self.get_nodes():
            s += '\n  ' + repr(node)
        s += ' \n L ensemble des aretes du graphe :   '
        for edge in self.get_edges():
            s += '\n  ' + repr(edge)
        return s

    cost = property(get_edge_cost)
    name = property(get_name)
    nodes = property(get_nodes)
    edges = property(get_edges)
    mat_adj = property(get_mat_adj)


if __name__ == '__main__':

    from edge import Edge
    from primnode import Primnode

    G_cours = Graph(name='cours')
    for num in xrange(0, 9):
        G_cours.add_node(Primnode())

    G_cours.add_edge(Edge(start=G_cours.get_nodes()[0],
                          end=G_cours.get_nodes()[1],
                          cost=4
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[1],
                          end=G_cours.get_nodes()[2],
                          cost=8
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[2],
                          end=G_cours.get_nodes()[3],
                          cost=7
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[3],
                          end=G_cours.get_nodes()[4],
                          cost=9
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[4],
                          end=G_cours.get_nodes()[5],
                          cost=10
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[3],
                          end=G_cours.get_nodes()[5],
                          cost=14
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[2],
                          end=G_cours.get_nodes()[5],
                          cost=4
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[5],
                          end=G_cours.get_nodes()[6],
                          cost=2
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[6],
                          end=G_cours.get_nodes()[7],
                          cost=1
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[7],
                          end=G_cours.get_nodes()[8],
                          cost=7
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[6],
                          end=G_cours.get_nodes()[8],
                          cost=6
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[2],
                          end=G_cours.get_nodes()[8],
                          cost=2
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[0],
                          end=G_cours.get_nodes()[8],
                          cost=8
                          )
                     )
    G_cours.add_edge(Edge(start=G_cours.get_nodes()[1],
                          end=G_cours.get_nodes()[8],
                          cost=11
                          )
                     )

    G_cours.delete_node(G_cours.get_nodes()[0])
    print G_cours
