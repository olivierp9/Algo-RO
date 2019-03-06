from graph import Graph
from copy import deepcopy


def Kruskal(G):  # la fonction prend la liste de edges et de union find
    """Retourne l arbre de cout minimal a laide de l algorithme de Kruskal."""
    edges = G.edges
    unionfind_list = G.nodes
    G_k = Graph()  # le graph contient le graph de kruskal
    dim = len(unionfind_list)  # dimension du nombre de sommet du graph
    kruskal_cost = 0  # initilisation du cout du graphe

    sorted_edges = deepcopy(edges)
    sorted_edges.sort()  # copy et triage des aretes par cout croissant
    # pour chaque arete on recupere les deux noeuds de leur extremite
    for edge in sorted_edges:
        unionfind_a = edge.get_startnode()
        unionfind_b = edge.get_endnode()
        # s'ils ont deux racines differentes
        if unionfind_a.find() != unionfind_b.find():
            G_k.add_node(unionfind_a)
            G_k.add_node(unionfind_b)
            # on ajoute les deux noeuds et l'arete dans l'arbre de kruskal
            G_k.add_edge(edge)
            # on met a jour le cout
            kruskal_cost += edge.get_vcost()
            unionfind_a.union(unionfind_b)
        # si le nombre d'arete de l'arbre de kruskal est
        # egal au nombre de sommet-1
        # on retourne l'arbre de kruskal et son cout
        if G_k.get_nb_edges() == dim - 1:
            return kruskal_cost, G_k
    return kruskal_cost, G_k
