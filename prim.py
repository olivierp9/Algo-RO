"""Retourne l arbre de cout minimal a laide de l algorithme de Prim."""
# D100 : missing docstring in public module
from graph import Graph
from queue import PriorityMinQueue
from edge import Edge
from copy import deepcopy
from copy import copy


def Prim(graph_ini, root=None):  # la fonction prend la graphe et la racine
    """Retourne l arbre de cout minimal a laide de l algorithme de Prim."""
    G = deepcopy(graph_ini)
    mat_adj = G.get_mat_adj()
    nodes = G.nodes

    if root is None:
        root = nodes[0]
    else:
        for node in nodes:
            if node.get_id() == root.get_id():
                root = node

    G_p = Graph()  # le graph contient le graph de prim

    min_queue = PriorityMinQueue()  # file de priorite des noeuds

    root.min_weight = 0  # le poid est mis a 0

    G_p.add_node(root)  # la racine est ajouter au graph

    for node in nodes:  # tous les noeuds sont ajoute dans le graphe et dans
                        # dans la file si le noeud est different de la racine
        if node != root:
            node.min_weight = float('inf')
            min_queue.enqueue(node)
            G_p.add_node(node)

    update = root  # update est le noeud pour lequel ces voisins seront m.a.j.
    c = 0  # le cout total de l arbre est initialise
    while not min_queue.is_empty():  # tant que la file n est pas vide

        for node in mat_adj[update].keys():  # pour tous les noeuds voisin

            for item in min_queue.items:  # pour tous les noeuds dans la file

                if (item == node) and (mat_adj[update][node].get_vcost()
                                       < item.min_weight):
                    # le poids est mis a jour sil est plus petit que le
                    # precedant quand les deux objets sont le meme

                    item.min_weight = copy(mat_adj[update][node].get_vcost())
                    item.parent = update  # le parent est mis a jour
                    # dans cette situation le parent est le noeud ayant
                    # l arete de poids minimum

        new = min_queue.dequeue()  # on enleve le noeud faisant partie
        # de larete de poids minimum
        G_p.add_edge(Edge(start=new.parent, end=new,
                          cost=mat_adj[new.parent][new].get_cost()))
        # larete est ajouter au graphe
        c += mat_adj[new.parent][new].get_vcost()
        # le cout est ajoute au total
        update = new  # on change le noeud update pour mettre a jour les poids
    return c, G_p
