import math
import numpy as np
import networkx as nx
from random import randint

def obs_on_line(start, stop, arr):
    st = 1000
    step = math.sqrt(2)
    dx = (stop[1] - start[1]) / st
    dy = (stop[0] - start[0]) / st
    x = start[1]
    xs = start[1]
    y = start[0]
    ys = start[0]
    c = []
    for i in range(st):
        x += dx
        y += dy
        xc = int(round(x))
        yc = int(round(y))
        s = math.sqrt((x-xs)**2+(y-ys)**2)
        if arr[yc][xc] == 1 or s >= step:
            break
        c.append((yc,xc))
    return c[-1]

def RRT(m, start, stop):
    dq={}
    arr = m.astype(bool)
    node_idx = list(range(np.sum(~arr)))
    node_pos = list(zip(*np.where(~arr)))
    pos2idx = dict(zip(node_pos, node_idx))
    idx2pos = dict(zip(node_idx, node_pos))
    dist = math.sqrt((start[0]-stop[0])**2 + (start[1]-stop[1])**2)
    g = nx.DiGraph()
    g.add_node(pos2idx[start])
    dq[pos2idx[start]]=0.0
    while dist > math.sqrt(2):
        pointpos = idx2pos[randint(0, len(idx2pos)-1)]
        min = np.inf
        ping = -1
        for i in g.nodes():
            a = math.sqrt((idx2pos[i][0] - pointpos[0])**2 + (idx2pos[i][1] - pointpos[1])**2)
            if a < min:
                min = a
                ping = i

        c = obs_on_line(idx2pos[ping], pointpos, arr)

        g.add_edge(pos2idx[c], ping,
                   weight=round(math.sqrt((idx2pos[ping][0] - c[0]) ** 2 + (idx2pos[ping][1] - c[1]) ** 2),3))

        dq[pos2idx[c]] = dq[ping] + round(math.sqrt((idx2pos[ping][0] - c[0])**2 + (idx2pos[ping][1] - c[1])**2),3)

        dist = math.sqrt((stop[0] - c[0])**2 + (stop[1] - c[1])**2)

    g.add_edge(pos2idx[stop], pos2idx[c],
               weight=round(math.sqrt((stop[0] - c[0]) ** 2 + (stop[1] - c[1]) ** 2),3))

    dq[pos2idx[stop]] = dq[pos2idx[c]] + round(math.sqrt((stop[0] - c[0]) ** 2 + (stop[1] - c[1]) ** 2), 3)

    pa = pos2idx[stop]
    pat = [pos2idx[stop]]
    while pa != pos2idx[start]:
        print(list(g.neighbors(pa)))
        for n in list(g.neighbors(pa)):
            pa = n
            pat.insert(0, n)
            break

    lines = []
    for i in range(len(pat)-1):
        lines.append(((idx2pos[pat[i]][1], idx2pos[pat[i]][0]), (idx2pos[pat[i+1]][1], idx2pos[pat[i+1]][0])))
    print(lines)
    return lines




