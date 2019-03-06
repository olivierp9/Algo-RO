class Stack(object):
    "Une implementation de la structure de donnees << pile >>."

    def __init__(self):
        self.items = []

    def push(self, item):
        "Ajoute `item` sur le dessus de la pile."
        self.items.append(item)

    def pop(self):
        "Retire l'objet du dessus de la pile."
        if len(self.items) == 0:
            raise IndexError("pile vide")
        return self.items.pop()  # Les listes implementent deja pop() !

    def top(self):
        "Consulte l'objet du dessus de la pile."
        return self.items[-1]    # L'item reste dans la pile.

    def is_empty(self):
        "Verifie si la pile est vide."
        return (len(self.items) == 0)

    def __repr__(self):
        return repr(self.items)
