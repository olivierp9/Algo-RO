"""Ensemble de fonction necessaire a lalgo de HK."""
# D100 : missing docstring in public module
from edge import Edge
from copy import deepcopy
from kruskal import Kruskal
from prim import Prim
from graph import Graph
from dfs2 import dfs


def Otree(graph_ini, position=0, choice='Prim'):
    """Retourne un 1-tree de cout minimal."""
    # les paremetres sont initialise
    cost_1 = float('inf')  # cout modifie 1
    cost_2 = float('inf')  # cout modifie 1
    real_1 = float('inf')  # cout reel de l arete 1
    real_2 = float('inf')  # cout reel de l arete 2
    key_1 = None  # autre noeud de l arete 1
    key_2 = None  # autre noeud de l arete 2
    G = deepcopy(graph_ini)  # une copie du graphe original est faite
    mat = G.mat_adj
    # Les deux arretes de poids modifies minimales incidentes au noeud choisi
    # seront sauvegardes pour le 1-tree
    for node in G.get_neighbors(G.nodes[position]):
        if cost_1 > mat[G.nodes[position]][node].get_vcost():  # v
            cost_2 = deepcopy(cost_1)
            real_2 = deepcopy(real_1)
            key_2 = node
            cost_1 = deepcopy(mat[G.nodes[position]][node].get_vcost())  # v
            real_1 = deepcopy(mat[G.nodes[position]][node].cost)
            key_1, key_2 = key_2, key_1
        elif cost_2 > mat[G.nodes[position]][node].get_vcost():  # v
            cost_2 = deepcopy(mat[G.nodes[position]][node].get_vcost())  # v
            real_2 = deepcopy(mat[G.nodes[position]][node].cost)
            key_2 = node
    # le noeud choisi est efface
    G.delete_node(G.nodes[position])
    new_node = deepcopy(graph_ini.nodes[position])
    # un arbre de recouvrement est fait selon le choix de lutilisateur
    if str.lower(choice) == 'kruskal':
        One_tree = Kruskal(G)
    elif str.lower(choice) == 'prim':
        if position >= len(G.nodes):
            position = len(G.nodes)-1
        One_tree = Prim(G, G.nodes[position])
    # le noeud efface est rajoute au 1-tree
    One_tree[1].add_node(new_node)
    node_OT = One_tree[1].nodes
    for node in node_OT:
        if node.get_id() == key_1.get_id():
            key_1 = node
        elif node.get_id() == key_2.get_id():
            key_2 = node
    # les deux aretes minimales sont rajoute au 1-tree pour finir sa creation
    One_tree[1].add_edge(Edge(start=new_node, end=key_1, cost=real_1))
    One_tree[1].add_edge(Edge(start=new_node, end=key_2, cost=real_2))
    # le cout modifier ainsi que le graphe sont retourne
    return One_tree[1], One_tree[1].get_vcost()


def Hkcycle(graph_ini, position, t, period, choice):
    """Determiner un cycle a laide de lalgo de HK."""
    copy = deepcopy(graph_ini)
    "INITIALISATION DES VARIABLES"
    W = -float('inf')
    # T contient le 1-tree et L_T son cout modifie
    T, L_T = Otree(copy, position, choice)
    pi = copy.get_pi()
    w = L_T - 2.*sum(pi)
    W = max(W, w)
    # pour le nombre diteration entre par lutilisateur
    for i in xrange(period):
        if all(v == 0 for v in T.get_v()):  # on retourne si on a un cycle
            return T
        for node in T.nodes:
            for nodez in copy.nodes:
                if node.get_id() == nodez.get_id():  # sinon les pi_i sont maj
                    nodez.set_pi(nodez.get_pi() +
                                 t*(T.get_nb_neighbors(node)-2)*0.7 +
                                 t*(nodez.get_olddeg()-2)*0.3)
                    nodez.set_olddeg(T.get_nb_neighbors(node))
        pi = copy.get_pi()
        T, L_T = Otree(copy, position, choice)
        w = L_T - 2.*sum(pi)
        W = max(W, w)
    # on retourne le graphe
    return T


def Cycle_creation(graph, graph_ini):
    """Cree un cycle a partir dun graphe."""
    G = deepcopy(graph)
    tsp = Graph()
    # on reinitialise les attribut de visite des noeuds
    for node in G.nodes:
        node.reset_visited()
    # par la suite on prend un noeud et on lajoute a la liste
    # quand on noeud est ajoute, il est visite
    first = G.nodes[0]
    lis = [first]
    first.set_visited()
    tsp.add_node(first)
    # tant que la liste ne contient pas tous les noeuds
    while len(lis) != len(G.nodes):
        candidate = None
        weight = float('inf')
        for neighbor in G.get_neighbors(first):
            if not neighbor.is_visited():
                if G.mat_adj[first][neighbor].cost < weight:
                    candidate = neighbor
                    weight = G.mat_adj[first][neighbor].cost
        # on prend le voisin du graphe donne le plus proche sil nest pas visite
        # sil est visite on prend le voisin le plus proche du graphe initial
        # qui na pas encore ete visite
        if candidate is None:
            for node in G.nodes:
                if not node.is_visited():
                    if graph_ini.get_edge_copy(node, first).cost < weight:
                        candidate = node
                        weight = graph_ini.get_edge_copy(node, first).cost
        candidate.set_visited()
        lis.append(candidate)
        tsp.add_node(candidate)
        tsp.add_edge(Edge(start=first, end=candidate, cost=weight))
        # le cadidant ansi que larete sont ajouter au grpahe
        first = candidate
    tsp.add_edge(Edge(start=lis[0], end=first,
                      cost=graph_ini.get_edge_copy(lis[0], first).cost))
    # on retourne le graphe
    return tsp


def Post_op(graph, g_ini):
    """Effectue la post op pour un cycle hamiltonien."""
    G = deepcopy(graph)
    to_ret = deepcopy(graph)
    flag = 1  # le flag signifie quil y a eu modification au dernier essai
    while flag == 1:
        flag = 0
        nodes1 = (G.nodes)
        nodes2 = (G.nodes)
        for n1 in nodes1:  # pour chaque paire de noeuds et chaque pair de leur
                            # voisin
            for n2 in nodes2:
                if n1 != n2:
                    neighbors1 = (G.get_neighbors(n1))
                    neighbors2 = (G.get_neighbors(n2))
                    for nei1 in neighbors1:
                        for nei2 in neighbors2:
                            var = decision(n1, n2, nei1, nei2, G, g_ini)
                            # on verifie si la modification entraine une
                            # reduction de cout du graphe
                            if var[0] == 1:
                                flag = 1
                                to_ret = var[1]
    return to_ret


def decision(n1, n2, nei1, nei2, G, g_ini):
    """Fonction qui determine si un changement reduit le cout  du cycle."""
    flag = 0
    to_ret = None
    # on verifie une quantite de condition
    if (((n1 != nei2) and (n2 != nei1) and (nei1 != nei2)) and
       (G.edge_exist(n1, nei1) and G.edge_exist(n2, nei2)) and not
       (G.edge_exist(n1, nei2) or G.edge_exist(n2, nei1))):

        cost1 = (G.mat_adj[n1][nei1].cost +
                 G.mat_adj[n2][nei2].cost)
        cost2 = (g_ini.get_edge_copy(n1, nei2).cost +
                 g_ini.get_edge_copy(n2, nei1).cost)
        if cost2 < cost1:  # si la somme des nouvelles aretes est plus petite
                            # que le somme des anciennes on essaie le nouveau
                            # graphe avec les nouvelles aretes
            G.delete_edge(n1, nei1)
            G.delete_edge(n2, nei2)
            G.add_edge(Edge(start=n1, end=nei2,
                            cost=g_ini.get_edge_copy(n1, nei2).cost))
            G.add_edge(Edge(start=n2, end=nei1,
                            cost=g_ini.get_edge_copy(n2, nei1).cost))
            if dfs(G) > 1:  # si le graphe reste connexe on garde les
                            # les modifications sinon on enelve les
                            # modifications apporte
                G.delete_edge(n1, nei2)
                G.delete_edge(n2, nei1)
                G.add_edge(Edge(start=n1, end=nei1,
                                cost=g_ini.get_edge_copy(n1, nei1).cost)
                           )
                G.add_edge(Edge(start=n2, end=nei2,
                                cost=g_ini.get_edge_copy(n2, nei2).cost)
                           )
            else:
                to_ret = deepcopy(G)  # on sauvegarde le nouveau graphe
                flag = 1  # on indique qune modification a ete apporte
    return flag, to_ret
