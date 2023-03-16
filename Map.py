import math
import matplotlib.pyplot as plt
import numpy as np


def map(ex, cs):
    file = open(ex + '.txt')  # Сюда необходимо вписать путь к желаемому файлу
    lines = file.readlines()

    position_data = []
    lidar_data = []

    for i in range(len(lines)):
        position_data.append(lines[i].split(';')[0].split(', '))
        lidar_data.append(lines[i].split(';')[1].split(', '))

    for i in range(len(position_data)):
        for j in range(len(position_data[i])):
            position_data[i][j] = float(position_data[i][j])

    for i in range(len(lidar_data)):
        for j in range(len(lidar_data[i])):
            lidar_data[i][j] = float(lidar_data[i][j])
            if lidar_data[i][j] == 5.6 or lidar_data[i][j] < 0.2:
                lidar_data[i][j] = np.nan

    step = 240 / len(lidar_data[0])
    x_global = []
    y_global = []
    for s in range(len(position_data)):
        if s % 5 == 0:
            for i in range(len(lidar_data[s])):
                if not math.isnan(lidar_data[s][i]):
                    x_local = lidar_data[s][i] * math.cos(((120 - (i * step)) * math.pi / 180) + position_data[s][2])
                    y_local = lidar_data[s][i] * math.sin(((120 - (i * step)) * math.pi / 180) + position_data[s][2])
                    x_global.append(x_local + position_data[s][0] + 0.3 * math.cos(position_data[s][2]))
                    y_global.append(y_local + position_data[s][1] + 0.3 * math.sin(position_data[s][2]))

    cell_size = cs
    m = np.zeros((round((max(y_global) - min(y_global)) / cell_size) + 1,
                  round((max(x_global) - min(x_global)) / cell_size) + 1))
    for i in range(len(x_global)):
        m_y = int(abs(y_global[i] - max(y_global)) / cell_size)
        m_x = int((x_global[i] - min(x_global)) / cell_size)
        if ((x_global[i] - min(x_global) - m_x * cell_size + cell_size/2)**2 + (abs(y_global[i] - max(y_global)) - m_y * cell_size + cell_size/2)**2) <= (cell_size):
            m[m_y][m_x] += 1

    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] >= 1:
                m[i][j] = 1
            else:
                m[i][j] = 0

    #m = m[slice(0, int(len(m) * 6 / 7))]
    #m = np.delete(m, (range(int(len(m[0]) * 8 / 9), int(len(m[0])))), 1)
    plt.imshow(m, interpolation='nearest')
    plt.savefig('map.png')
    np.save('MapFile', m)
