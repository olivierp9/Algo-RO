from stack import Stack


def dfs(G):
    """Fonction qui effectue un parcours en pre ordre dans un graphe."""
    c = 0
    for node in G.nodes:
        node.reset_visited()
    for node in G.nodes:
        if not node.is_visited():
            dfs_visit(G, node)
            c += 1
            if c > 1:
                return c

    return c


def dfs_visit(G, root):
    """Fonction qui effectue un parcours en pre ordre dans un arbre."""
    for node in G.nodes:
        if node.get_id() == root.get_id():
            root = node
    pile = Stack()
    pile.push(root)  # root devient racine d'une nouvelle arborescence.
    file1 = []
    c = 0

    while not pile.is_empty():

        u = pile.pop()
        u.set_visited()
        file1.append(u)
        c += 1
        for nei in G.get_neighbors(u):
            if not nei.is_visited():
                pile.push(nei)
    file1.append(root)

    return file1, c


if __name__ == '__main__':

    from markednode import MarkedNode
    from edge import Edge
    from graph import Graph

    G = Graph()

    r = MarkedNode(name='r')
    s = MarkedNode(name='s')
    t = MarkedNode(name='t')
    u = MarkedNode(name='u')
    v = MarkedNode(name='v')
    w = MarkedNode(name='w')
    x = MarkedNode(name='x')
    y = MarkedNode(name='y')

    G.add_node(r)
    G.add_node(s)
    G.add_node(t)
    G.add_node(u)
    G.add_node(v)
    G.add_node(w)
    G.add_node(x)
    G.add_node(y)
