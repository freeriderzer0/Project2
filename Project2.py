import tkinter
from tkinter.ttk import Combobox
from matplotlib import pyplot as plt
import numpy as np
from Map import map
from Dij import Dijkstra
from Astar import A_star
from RRT import RRT
from tkinter import *
from PIL import ImageTk, Image

size = -1


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Поиск пути")
        self.lbl1 = Label(self.window, text="Размер ячейки (м):").grid(column=0, row=0)
        self.lbl2 = Label(self.window, text="Алгоритм поиска:").grid(column=0, row=1)
        self.lbl3 = Label(self.window, text="Старт:").grid(column=2, row=1)
        self.lblsx = Label(self.window, text=" X ")
        self.lblsx.grid(column=3, row=1)
        self.lblsy = Label(self.window, text=" Y ")
        self.lblsy.grid(column=4, row=1)
        self.lbl4 = Label(self.window, text="Цель:").grid(column=5, row=1)
        self.lbltx = Label(self.window, text=" X ")
        self.lbltx.grid(column=6, row=1)
        self.lblty = Label(self.window, text=" Y ")
        self.lblty.grid(column=7, row=1)
        self.combo = Combobox(self.window, width=10)
        self.combo['values'] = ('Dijkstra', 'A*', 'RRT')
        self.combo.current(1)
        self.combo.grid(column=1, row=1)
        self.txt = Entry(self.window, width=10)
        self.txt.grid(column=1, row=0)
        self.btn = Button(self.window, text="Карта", command=self.clicked_map).grid(column=2, row=0)
        self.btn1 = Button(self.window, text="Поиск", command=self.clicked_d).grid(column=8, row=1)
        self.btn2 = Button(self.window, text="!ЧТОБЫ ЗАКРЫТЬ ПРОГУ, ЖМИТЕ СЮДА!", command=self.window.quit).grid(column=9, row=0)

        self.photo = tkinter.PhotoImage(height=1, width=1)
        self.canvas = tkinter.Canvas(self.window, height=500, width=700)
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(row=2, column=9)
        self.canvas.bind("<Button-1>", self.start)
        self.canvas.bind("<Button-3>", self.stop)
        self.window.mainloop()

    def start(self, event):
        global sx, sy
        sx = int((event.x - 104)/(450/len(np.load('MapFile.npy')[0])))
        sy = int((event.y - 58)/(369/len(np.load('MapFile.npy'))))
        print(event.x, event.y)
        self.lblsx.configure(text=sx)
        self.lblsy.configure(text=sy)
        m[sy][sx] += 2
        plt.imshow(m, interpolation='nearest')
        plt.savefig('map1.png')
        self.imag = ImageTk.PhotoImage(Image.open("map1.png"))
        self.c_imag = self.canvas.create_image(0, 0, anchor='nw', image=self.imag)
        self.canvas.grid(row=2, column=9)

    def stop(self, event):
        global tx, ty
        tx = int((event.x - 104) / (450 / len(np.load('MapFile.npy')[0])))
        ty = int((event.y - 58) / (369 / len(np.load('MapFile.npy'))))
        self.lbltx.configure(text=tx)
        self.lblty.configure(text=ty)
        m[ty][tx] += 1.3
        plt.imshow(m, interpolation='nearest')
        plt.savefig('map1.png')
        self.imag = ImageTk.PhotoImage(Image.open("map1.png"))
        self.c_imag = self.canvas.create_image(0, 0, anchor='nw', image=self.imag)
        self.canvas.grid(row=2, column=9)

    def clicked_d(self):
        if self.combo.get() == 'Dijkstra':
            Dijkstra(np.load('MapFile.npy'), (sy, sx), (ty, tx))
            self.imag = ImageTk.PhotoImage(Image.open("dij.png"))
            self.c_imag = self.canvas.create_image(0, 0, anchor='nw', image=self.imag)
            self.canvas.grid(row=2, column=9)
        if self.combo.get() == 'A*':
            A_star(np.load('MapFile.npy'), (sy, sx), (ty, tx), size)
            self.imag = ImageTk.PhotoImage(Image.open("A.png"))
            self.c_imag = self.canvas.create_image(0, 0, anchor='nw', image=self.imag)
            self.canvas.grid(row=2, column=9)
        if self.combo.get() == 'RRT':
            lines = RRT(np.load('MapFile.npy'), (sy, sx), (ty, tx))
            for i in range(len(lines)):
                self.canvas.create_line(lines[i][0][0]*(450/len(np.load('MapFile.npy')[0]))+104+(450/len(np.load('MapFile.npy')[0]))/2,
                                        lines[i][0][1]*(369/len(np.load('MapFile.npy')))+58+(369/len(np.load('MapFile.npy')))/2,
                                        lines[i][1][0]*(450/len(np.load('MapFile.npy')[0]))+104+(450/len(np.load('MapFile.npy')[0]))/2,
                                        lines[i][1][1]*(369/len(np.load('MapFile.npy')))+58+(369/len(np.load('MapFile.npy')))/2)
            self.canvas.grid(row=2, column=9)

    def clicked_map(self):
        global size
        global m
        if size != float(self.txt.get()):
            size = float(self.txt.get())
            map('examp5', size)
        m = np.load('MapFile.npy')
        self.imag = ImageTk.PhotoImage(Image.open("map.png"))
        self.c_imag = self.canvas.create_image(0, 0, anchor='nw', image=self.imag)
        self.canvas.grid(row=2, column=9)


app = App()




