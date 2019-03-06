"""Fonction principale."""
# D100 : missing docstring in public module
if __name__ == '__main__':
    import sys
    from read_stsp import read_header, read_nodes, read_edges, plot_graph2
    from edge import Edge
    from primnode import Primnode
    from unionfind import Unionfind
    from graph import Graph
    from rsl import Rsl
    from hkcycle import Hkcycle
    from hkcycle import Cycle_creation
    from hkcycle import Post_op

    finstance = sys.argv[1]
    with open(finstance, "r") as fd:
        header = read_header(fd)
        dim = header['DIMENSION']
        name = header['NAME']
        nodes = read_nodes(header, fd)
        edges = read_edges(header, fd)
        G = Graph(name=name)
        if nodes:
            for node in xrange(dim):
                G.add_node(Primnode(data=nodes[node]))
        else:
            for node in xrange(dim):
                G.add_node(Primnode())

        if edges:
            for edge in edges:
                G.add_edge(Edge(start=G.get_nodes()[int(edge[0])],
                                end=G.get_nodes()[int(edge[1])],
                                cost=edge[2]
                                )
                           )
        GK = Graph(name=name)
        if nodes:
            for node in xrange(dim):
                GK.add_node(Unionfind(data=nodes[node]))
        else:
            for node in xrange(dim):
                GK.add_node(Unionfind())

        if edges:
            for edge in edges:
                GK.add_edge(Edge(start=GK.get_nodes()[int(edge[0])],
                                 end=GK.get_nodes()[int(edge[1])],
                                 cost=edge[2]
                                 )
                            )

    input1 = raw_input("1.rsl ou 2.hk:")
    input1 = str.lower(input1)

    if input1 == "rsl" or input1 == "1":

        input1_rsl = int(raw_input("Entrer le numero du noeud:"))
        input2_rsl = raw_input("1.prim ou 2.kruskal:")

        if str.lower(input2_rsl) == "kruskal":
            r = Rsl(GK, choice='kruskal', root=GK.nodes[input1_rsl])
            print "\n\ncout:"+str(r[1])
            print "\n\n Graph"
            plot_graph2(r[0], GK)
        elif str.lower(input2_rsl) == "prim":
            r = Rsl(G, choice='prim', root=G.nodes[input1_rsl])
            print "\n\n cout:"+str(r[1])
            print "\n\n Graph"
            plot_graph2(r[0], G)
        else:
            print "vous navez pas respecter les choix le programe se termine"

    elif input1 == "hk" or input1 == "2":
        position = int(raw_input("Entrer le numero du noeud:"))
        choice = raw_input("1.prim ou 2.kruskal:")
        step = float(raw_input("Entrer le pas:"))
        itera = int(raw_input("Entrer le nombre diterations:"))

        if str.lower(choice) == "kruskal":
            onetree = Hkcycle(GK, position, step, itera, choice)
            cycle = Cycle_creation(onetree, GK)
            print "\n\n cout du cycle:"+str(cycle.get_cost())
            print "\n\n Graph du cycle"
            plot_graph2(cycle, GK)
            cycle_postop = Post_op(cycle, GK)
            if cycle_postop.get_cost() < cycle.get_cost():
                print "\n\n cout du cycle:"+str(cycle_postop.get_cost())
                print "\n\n Graph du cycle"
                plot_graph2(cycle_postop, GK)

        elif str.lower(choice) == "prim":
            onetree = Hkcycle(G, position, step, itera, choice)
            cycle = Cycle_creation(onetree, G)
            print "\n\n cout du cycle:"+str(cycle.get_cost())
            print "\n\n Graph du cycle"
            plot_graph2(cycle, G)
            cycle_postop = Post_op(cycle, G)
            if cycle_postop.get_cost() < cycle.get_cost():
                print "\n\n cout du cycle postop:"+str(cycle_postop.get_cost())
                print "\n\n Graph du cycle apres optimisation"
                plot_graph2(cycle_postop, G)
        else:
            print "vous navez pas respecter les choix le programe se termine"
    else:
        print "vous navez pas respecter les choix le programe se termine"
