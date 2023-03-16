import math
import networkx as nx
from operator import itemgetter
from matplotlib import pyplot as plt
import numpy as np
from Graph import maze_to_graph


def A_star(m, begin, end, cell_size):
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

    openList = []
    closedList = []
    dist = dict(zip(idx2pos.keys(), [[np.inf, np.inf, np.inf]] * (len(idx2pos)-1)))  #ghf
    cspace = {}
    ospace = {}
    dist[pos2idx[start]] = [0,
                            (abs(abs(start[0] - stop[0]) - abs(start[1] - stop[1])) * 10) + (min(abs(start[0] - stop[0]), abs(start[1] - stop[1])) * 14),
                            (abs(abs(start[0] - stop[0]) - abs(start[1] - stop[1])) * 10) + (min(abs(start[0] - stop[0]), abs(start[1] - stop[1])) * 14)]
    openList.append(pos2idx[start])
    ospace[pos2idx[start]] = 0

    while openList != []:
        cn = sorted(dist.items(), key=lambda item: item[1][2])[0][0]
        closedList.append(cn)
        cspace[cn] = [dist[cn][0], dist[cn][2]]
        openList.remove(cn)
        ospace.pop(cn)
        dist.pop(cn)
        if cn == pos2idx[stop]:
            break
        for i in list(g.neighbors(cn)):
            if i in closedList:
                continue
            gi = cspace[cn][0] + g.edges[cn, i]['weight']
            hi = (abs(abs(idx2pos[i][0] - stop[0]) - abs(idx2pos[i][1] - stop[1])) * 10) + (min(abs(idx2pos[i][0] - stop[0]), abs(idx2pos[i][1] - stop[1])) * 14)
            #hi = math.sqrt((idx2pos[i][0] - stop[0])**2 + (idx2pos[i][1] - stop[1])**2)*12
            #hi = math.sqrt((idx2pos[i][0] * cell_size + cell_size/2 - stop[0] * cell_size + cell_size/2)**2 + (idx2pos[i][1] * cell_size + cell_size/2 - stop[1] * cell_size + cell_size/2)**2)*10
            fi = gi + hi
            if i in openList:
                if gi > ospace[i][0]:
                    continue
            dist[i] = [gi, hi, fi]
            openList.append(i)
            ospace[i] = [gi, fi]

    p = pos2idx[stop]
    path = [pos2idx[stop]]
    while p != pos2idx[start]:
        for n in list(set(g.neighbors(p)) & set(closedList)):
            st = cspace[p][0] - g.edges[p, n]['weight']
            if cspace[n][0] == st:
                p = n
                path.insert(0, n)
                break

    for i in range(len(closedList)):
        m[idx2pos[closedList[i]][0]][idx2pos[closedList[i]][1]] += 0.5
    for i in range(len(path)):
        m[idx2pos[path[i]][0]][idx2pos[path[i]][1]] += 1.5
    m[idx2pos[path[0]][0]][idx2pos[path[0]][1]] += 0.5
    m[idx2pos[path[len(path)-1]][0]][idx2pos[path[len(path)-1]][1]] -= 0.2
    plt.imshow(m, interpolation='nearest')
    plt.savefig('A.png')