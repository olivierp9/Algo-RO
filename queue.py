"""Une implementation de la structure de donnees file."""
# D100 : missing docstring in public module


class Queue(object):
    """Une implementation de la structure de donnees file."""

    def __init__(self):
        """Initialisation des variables."""
        self.items = []

    def enqueue(self, item):
        """Ajoute `item` a la fin de la file."""
        self.items.append(item)

    def dequeue(self):
        """Retire l'objet du debut de la file."""
        return self.items.pop(0)

    def is_empty(self):
        """Verifie si la file est vide."""
        return (len(self.items) == 0)

    def __contains__(self, item):
        """Retourne les elements de la file."""
        return (item in self.items)

    def __repr__(self):
        """Represnete la file."""
        return (self.items)


class PriorityQueue(Queue):
    """Une implementation de la structure de donnees file."""

    def dequeue(self):
        """Retire l'objet ayant la plus haute priorite."""
        highest = self.items[0]
        for item in self.items[1:]:
            if item > highest:
                highest = item
        idx = self.items.index(highest)
        return self.items.pop(idx)

    def enqueue(self, item):
        """Insere l'objet en ordre croissant de priorite."""
        if self.is_empty():
            self.items.append(item)
        else:
            for i in xrange(0, len(self.items)):
                if item < self.items[i]:
                    self.items.insert(i, item)
                    return
            self.items.append(item)


# Les items de priorite nous permettent d'utiliser min() et max().

class PriorityMinQueue(Queue):
    """Une implementation d une file qui enleve le min."""

    def dequeue(self):
        """Retire l'objet ayant la plus petite priorite."""
        return self.items.pop(self.items.index(min(self.items)))


class PriorityMaxQueue(Queue):
    """Une implementation d une file qui enleve le max."""

    def dequeue(self):
        """Retire l'objet ayant la plus haute priorite."""
        return self.items.pop(self.items.index(max(self.items)))


class PriorityStack(Queue):
    """Une implementation d une file qui agit comme une pile."""

    __priority = -1

    def enqueue(self, item):
        """Ajoute l'objet comme une pile."""
        PriorityStack.__priority += 1
        item.set_priority(PriorityStack.__priority)
        return self.items.append(item)

    def dequeue(self):
        """Retire l'objet comme une pile."""
        return self.items.pop(self.items.index(max(self.items)))
