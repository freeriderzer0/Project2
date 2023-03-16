import math
import numpy as np
import networkx as nx


def maze_to_graph(is_wall, allowed_steps):
    node_idx = list(range(np.sum(~is_wall)))
    node_pos = list(zip(*np.where(~is_wall)))
    pos2idx = dict(zip(node_pos, node_idx))

    g = nx.DiGraph()
    for (i, j) in node_pos:
        for (delta_i, delta_j) in allowed_steps:  
            if (i + delta_i, j + delta_j) in pos2idx:  
                g.add_edge(pos2idx[(i, j)], pos2idx[(i + delta_i, j + delta_j)],
                           weight=int((round((math.sqrt(abs(delta_i) + abs(delta_j))), 1)) * 10))

    idx2pos = dict(zip(node_idx, node_pos))
    return g, idx2pos, pos2idx
