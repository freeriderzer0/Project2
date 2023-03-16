from matplotlib import pyplot as plt
import numpy as np
from Graph import maze_to_graph


def Dijkstra(m, begin, end):
    arr = m.astype(bool)
    steps = [(0, 1),  # right
             (-1, 1),  # diagonal up-right
             (-1, 0),  # up
             (-1, -1),  # diagonal up-left
             (0, -1),  # left
             (1, -1),  # diagonal down-left
             (1, 0),  # down
             (1, 1)]  # diagonal down-right

    g, idx2pos, pos2idx = maze_to_graph(arr, steps)

    start = begin
    stop = end

    dist = dict(zip(idx2pos.keys(), [np.inf] * len(idx2pos)))
    dist[pos2idx[start]] = 0
    DQ = {}
    while dist != {}:
        U = sorted(dist.items(), key=lambda item: item[1])[0][0]
        if U not in list(g.nodes()):
            dist.pop(U)
            continue
        DQ[U] = dist[U]
        dist.pop(U)
        for n in list(g.neighbors(U)):
            if n in dist:
                length = DQ[U] + g.edges[U, n]['weight']
                if length < dist[n]:
                    dist[n] = length

    p = pos2idx[stop]
    path = [pos2idx[stop]]
    while p != pos2idx[start]:
        for n in list(g.neighbors(p)):
            st = DQ[p] - g.edges[p, n]['weight']
            if DQ[n] == st:
                p = n
                path.insert(0, n)
                break

    for i in range(len(path)):
        m[idx2pos[path[i]][0]][idx2pos[path[i]][1]] += 1.5
    m[idx2pos[path[0]][0]][idx2pos[path[0]][1]] += 0.5
    m[idx2pos[path[len(path)-1]][0]][idx2pos[path[len(path)-1]][1]] -= 0.2
    plt.imshow(m, interpolation='nearest')
    plt.savefig('dij.png')