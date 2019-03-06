"""Une classe generique pour representer les noeuds d'un graphe."""
# D100 : missing docstring in public module
from node import Node


class Primnode(Node):
    """Une classe generique pour representer les noeuds d'un graphe."""

    def __init__(self, name='Sans nom', data=None):
        """initilise les varaibles du primnode."""
        super(Primnode, self).__init__(name, data)
        self.__parent = self
        self.__min_weight = float('inf')
        self.__visited = False
        self.__pi = 0
        self.__olddeg = 0

    def get_parent(self):
        """Retourne le parent du noeud."""
        return self.__parent

    def set_parent(self, new_parent):
        """Change le parent du noeud."""
        self.__parent = new_parent

    def set_min_weight(self, weight):
        """Change le poids minimal lie au noeud."""
        self.__min_weight = weight

    def get_min_weight(self):
        """Retourne le poids minimal lie au noeud."""
        return self.__min_weight

    def is_visited(self):
        """Retourne si le noeud a ete visite."""
        return self.__visited

    def set_visited(self):
        """Change lattribut par visiter."""
        self.__visited = True

    def reset_visited(self):
        """Change lattribut par  non visiter."""
        self.__visited = False

    def get_pi(self):
        """Retoune le pi du noeud pour lalgo de HK."""
        return self.__pi

    def set_pi(self, val):
        """Change le pi du noeud pour lalgo de HK."""
        self.__pi = val

    def get_olddeg(self):
        """Retourne l'ancien degre du noeud."""
        return self.__olddeg

    def set_olddeg(self, val):
        """Change l'ancien degre du noeud."""
        self.__olddeg = val

    def __lt__(self, other):
        """Compare les poids des objets unionfind."""
        return self.min_weight < other.min_weight

    def __le__(self, other):
        """Compare les poids des objets unionfind."""
        return self.min_weight <= other.min_weight

    parent = property(get_parent, set_parent)
    min_weight = property(get_min_weight, set_min_weight)
    pi = property(get_pi, set_pi)
