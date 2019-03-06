"""Une classe generique pour representer les forets d'un graphe."""
# D100 : missing docstring in public module
from node import Node


class Unionfind(Node):
    """Une classe generique pour representer les forets d'un graphe."""

    def __init__(self, name='Sans nom', data=None):
        """initilise les varaibles du unionfind."""
        super(Unionfind, self).__init__(name, data)
        self.__parent = self
        self.__rank = 0
        self.__visited = False
        self.__pi = 0
        self.__olddeg = 0

    def get_parent(self):
        """Retourne le parent du noeud."""
        return self.__parent

    def set_parent(self, new_parent):
        """Change le parent du noeud."""
        self.__parent = new_parent

    def get_rank(self):
        """Retourne le rang du noeud."""
        return self.__rank

    def update_rank(self):
        """Augmente le rang du noeud."""
        self.__rank += 1

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

    def find(self):
        """Retourne le parent du noeud et effectue la compression."""
        if self.get_parent() == self:
            return self
        else:
            self.__parent = self.__parent.find()
            return self.__parent.find()

    def union(self, OtherUN):
        """Effectue l union entre deux ensemble non connexe."""
        OtherUN_root = OtherUN.find()
        self_root = self.find()

        if self_root.rank > OtherUN_root.rank:
            OtherUN_root.parent = self_root

        elif self_root.rank <= OtherUN_root.rank:
            self_root.parent = OtherUN_root

            if self_root.rank == OtherUN_root.rank:
                OtherUN_root.update_rank()

    parent = property(get_parent, set_parent)
    rank = property(get_rank)
    pi = property(get_pi, set_pi)
