"""Retourne le parcours en preordre de larbre de recouvrement mininmal."""
# D100 : missing docstring in public module
from prim import Prim
from kruskal import Kruskal
from dfs2 import dfs_visit
from graph import Graph
from edge import Edge


def Rsl(G, root=None, choice='prim'):
    """Retourne le parcours en preordre de larbre de recouvrement mininmal."""
    if str.lower(choice) == 'prim':
        cost, arbre_min = Prim(G, root)

    elif str.lower(choice) == 'kruskal':
        cost, arbre_min = Kruskal(G)

    if root is None:  # si la racine nest pas donne le premier noeud est pris
        order, temp = dfs_visit(arbre_min, arbre_min.nodes[0])
    else:
        order, temp = dfs_visit(arbre_min, root)
    c = 0
    cycle = Graph()  # un graphe est cree
    for node in order:  # les noeuds sont ajouter au grpahe
        cycle.add_node(node)
    for i in xrange(len(order)-1):  # les aretes sont ajouter au graphe
                                    # a laide du cycle obtenue de dfs_visit
        temp_c = G.get_edge_copy(order[i], order[i+1]).get_cost()
        cycle.add_edge(Edge(start=order[i], end=order[i+1], cost=temp_c))
        c += temp_c

    return cycle, c
