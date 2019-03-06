"""Une classe generique pour representer les aretes d'un graphe."""
# D100 : missing docstring in public module


class Edge(object):
    """Une classe generique pour representer les aretes d'un graphe."""

    __edge_count = -1   # Compteur global partage par toutes les instances.

    def __init__(self, name='Sans nom',
                 start=None, end=None, cost=0):
        """Initialise l arete."""
        self.__name = name
        Edge.__edge_count += 1
        self.__id = Edge.__edge_count
        self.__cost = cost
        self.__start = start
        self.__end = end

    def get_name(self):
        """Donne le nom de l arete."""
        return self.__name

    def get_cost(self):
        """Donne le cout de l arete."""
        return self.__cost

    def get_vcost(self):
        """Donne le cout de l arete."""
        return self.__cost + self.__start.get_pi() + self.__end.get_pi()

    def get_startnode(self):
        """Donne un des noeuds incidents de l arrete."""
        return self.__start

    def get_endnode(self):
        """Donne l autre noeud incident de l arrete."""
        return self.__end

    def get_id(self):
        """Donne le numero d'identification de l arete."""
        return self.__id

    def __lt__(self, other):
        """Comparaison riche."""
        return self.get_vcost() < other.get_vcost()

    def __le__(self, other):
        """Comparaison riche."""
        return self.get_vcost() <= other.get_vcost()

    def __repr__(self):
        """Represente l arete."""
        id = self.get_id()
        name = self.get_name()
        start = self.get_startnode()
        end = self.get_endnode()
        cost = self.get_cost()
        s = 'Arete %s (id %d)' % (name, id)
        s += ' reliant les noeuds : ' + repr(start) + \
            ' et : ' + repr(end) + ' Cout : %d' % (cost)
        return s

    start = property(get_startnode)
    end = property(get_endnode)
    cost = property(get_cost)    


if __name__ == '__main__':

    edges = []
    for k in xrange(5):
        edges.append(Edge())

    for edge in edges:
        print edge
