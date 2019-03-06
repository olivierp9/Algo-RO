import numpy as np


def read_header(fd):
    "Parse a .tsp file and return a dictionary with header data."

    converters = {'NAME': str, 'TYPE': str, 'COMMENT': str, 'DIMENSION': int,
                  'EDGE_WEIGHT_TYPE': str, 'EDGE_WEIGHT_FORMAT': str,
                  'EDGE_DATA_FORMAT': str, 'NODE_COORD_TYPE': str,
                  'DISPLAY_DATA_TYPE': str}
    sections = converters.keys()
    header = {}

    # Initialize header.
    for section in sections:
        header[section] = None

    fd.seek(0)
    for line in fd:
        data = line.split(':')
        firstword = data[0].strip()
        if firstword in sections:
            header[firstword] = converters[firstword](data[1].strip())

    return header


def read_nodes(header, fd):
    """
    Parse a .tsp file and return a dictionary of nodes, of the form
    {id:(x,y)}. If node coordinates are not given, an empty dictionary is
    returned. The actual number of nodes is in header['DIMENSION'].
    """

    nodes = {}

    node_coord_type = header['NODE_COORD_TYPE']
    display_data_type = header['DISPLAY_DATA_TYPE']
    if node_coord_type not in ['TWOD_COORDS', 'THREED_COORDS'] and \
            display_data_type not in ['COORDS_DISPLAY', 'TWOD_DISPLAY']:

                # Node coordinates are not given.
                return nodes

    dim = header['DIMENSION']
    fd.seek(0)
    k = 0
    display_data_section = False
    node_coord_section = False

    for line in fd:
        if line.strip() == "DISPLAY_DATA_SECTION":
            display_data_section = True
            continue
        elif line.strip() == "NODE_COORD_SECTION":
            node_coord_section = True
            continue

        if display_data_section:
            data = line.strip().split()
            nodes[int(data[0]) - 1] = tuple(map(float, data[1:]))
            k += 1
            if k >= dim:
                break
            continue

        elif node_coord_section:
            data = line.strip().split()
            nodes[int(data[0]) - 1] = tuple(map(float, data[1:]))
            k += 1
            if k >= dim:
                break
            continue

    return nodes


def read_edges(header, fd):
    "Parse a .tsp file and return the collection of edges as a Python set."

    edges = set()
    edge_weight_format = header['EDGE_WEIGHT_FORMAT']
    known_edge_weight_formats = ['FULL_MATRIX', 'UPPER_ROW', 'LOWER_ROW',
                                 'UPPER_DIAG_ROW', 'LOWER_DIAG_ROW',
                                 'UPPER_COL', 'LOWER_COL', 'UPPER_DIAG_COL',
                                 'LOWER_DIAG_COL']
    if edge_weight_format not in known_edge_weight_formats:
        return edges

    dim = header['DIMENSION']

    def n_nodes_to_read(n):
        format = edge_weight_format
        if format == 'FULL_MATRIX':
            return dim
        if format == 'LOWER_DIAG_ROW' or format == 'UPPER_DIAG_COL':
            return n+1
        if format == 'LOWER_DIAG_COL' or format == 'UPPER_DIAG_ROW':
            return dim-n
        if format == 'LOWER_ROW' or format == 'UPPER_COL':
            return n
        if format == 'LOWER_COL' or format == 'UPPER_ROW':
            return dim-n-1

    fd.seek(0)
    edge_weight_section = False
    k = 0
    n_edges = 0
    i = 0
    n_to_read = n_nodes_to_read(k)

    for line in fd:
        if line.strip() == "EDGE_WEIGHT_SECTION":
            edge_weight_section = True
            continue

        if edge_weight_section:
            data = line.strip().split()
            n_data = len(data)

            start = 0

            while n_data > 0:

                # Number of items that we read on this line
                # for the current node.
                n_on_this_line = min(n_to_read, n_data)

                # Read edges.
                for j in range(start, start + n_on_this_line):
                    n_edges += 1
                    if edge_weight_format in ['UPPER_ROW', 'LOWER_COL']:
                        edge = (k, i+k+1, float(data[j]))
                    elif edge_weight_format in ['UPPER_DIAG_ROW', \
                                                'LOWER_DIAG_COL']:
                        edge = (k, i+k, float(data[j]))
                    elif edge_weight_format in ['UPPER_COL', 'LOWER_ROW']:
                        edge = (i+k+1, k, float(data[j]))
                    elif edge_weight_format in ['UPPER_DIAG_COL', \
                                                'LOWER_DIAG_ROW']:
                        edge = (i, k, float(data[j]))
                    elif edge_weight_format == 'FULL_MATRIX':
                        edge = (k, i, float(data[j]))
                    edges.add(edge)
                    i += 1

                # Update number of items remaining to be read.
                n_to_read -= n_on_this_line
                n_data -= n_on_this_line

                if n_to_read <= 0:
                    start += n_on_this_line
                    k += 1
                    i = 0
                    n_to_read = n_nodes_to_read(k)

                if k >= dim:
                    n_data = 0

            if k >= dim:
                break

    return edges


def plot_graph(nodes, edges):
    """
    Plot the graph represented by `nodes` and `edges` using Matplotlib.
    Very basic for now.
    """

    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Plot nodes.
    x = [node[0] for node in nodes.values()]
    y = [node[1] for node in nodes.values()]

    # Plot edges.
    edge_pos = np.asarray([(nodes[e[0]], nodes[e[1]]) for e in edges])
    edge_collection = LineCollection(edge_pos, linewidth=1.5, antialiased=True,
                                     colors=(.8, .8, .8), alpha=.75, zorder=0)
    ax.add_collection(edge_collection)
    ax.scatter(x, y, s=35, c='r', antialiased=True, alpha=.75, zorder=1)
    ax.set_xlim(min(x) - 10, max(x) + 10)
    ax.set_ylim(min(y) - 10, max(y) + 10)

    plt.show()
    return


def plot_graph2(Graph, g_ini=None):
    """
    Plot the graph represented by `nodes` and `edges` using Matplotlib.
    Very basic for now.
    """

    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from random import random
    from copy import deepcopy
    import numpy as np
    from cmdscale import Cmdscale

    G = deepcopy(Graph)
    g_ini = deepcopy(g_ini)
    fig = plt.figure()
    ax = fig.add_subplot(111)  # cree des coordonnes a partir de la matrice
                                # de distance sil pas de coordonnes
    if g_ini is not None and g_ini.nodes[0].get_data() is None:
        tem2 = g_ini.mat_adj
        troup = np.zeros((len(g_ini.nodes), (len(g_ini.nodes))))
        for i in xrange(len(g_ini.nodes)):
            for j in xrange(len(g_ini.nodes)):
                if i != j:
                    if g_ini.edge_exist(g_ini.nodes[i], g_ini.nodes[j]):
                        troup[i][j] = tem2[g_ini.nodes[i]][g_ini.nodes[j]].cost
        temp3 = Cmdscale(troup)
        for i in xrange(len(g_ini.nodes)):
            g_ini.nodes[i].set_data(tuple(temp3[0][i][0:2]))

        for node in g_ini.nodes:
            for nodez in G.nodes:
                if node.get_id() == nodez.get_id():
                    nodez.set_data(node.get_data())

    # Plot nodes.
    if G.nodes[0].get_data() is None:
        for node in G.nodes:
            node.set_data((random()*1000, random()*1000))

    x = [node.get_data()[0] for node in G.nodes]
    y = [node.get_data()[1] for node in G.nodes]

    # Plot edges.
    e_pos = []
    for e in G.edges:
        e_pos.append([e.start.get_data(), e.end.get_data()])
    edge_pos = np.asarray(e_pos)
    edge_collection = LineCollection(edge_pos, linewidth=1.5, antialiased=True,
                                     colors=(.8, .8, .8), alpha=.75, zorder=0)
    ax.add_collection(edge_collection)
    ax.scatter(x, y, s=10, c='r', antialiased=True, alpha=.75, zorder=1)
    ax.set_xlim(min(x) - 10, max(x) + 10)
    ax.set_ylim(min(y) - 10, max(y) + 10)

    plt.show()
    return

if __name__ == "__main__":

    import sys

    finstance = 'ref/dantzig42.tsp'

    with open(finstance, "r") as fd:

        header = read_header(fd)
        print 'Header: ', header
        dim = header['DIMENSION']
        edge_weight_format = header['EDGE_WEIGHT_FORMAT']

        print "Reading nodes"
        nodes = read_nodes(header, fd)
        print nodes

        print "Reading edges"
        edges = read_edges(header, fd)
        edge_list = []
        edge_weight = []
        for k in range(dim):
            edge_list.append([])
            edge_weight.append([])
        for edge in edges:
            if edge_weight_format in ['UPPER_ROW', 'LOWER_COL', \
                    'UPPER_DIAG_ROW', 'LOWER_DIAG_COL']:
                edge_list[edge[0]].append(edge[1])
            else:
                edge_list[edge[1]].append(edge[0])
        
        for edge in edges:
            if edge_weight_format in ['UPPER_ROW', 'LOWER_COL', \
                    'UPPER_DIAG_ROW', 'LOWER_DIAG_COL']:
                edge_weight[edge[0]].append(edge[2])
            else:
                edge_weight[edge[1]].append(edge[2])
                

    if len(nodes) > 0:
        plot_graph(nodes, edges)
