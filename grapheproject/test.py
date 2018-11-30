from numpy.random import random
from math import *
import tkinter as tk

"""______________________________________FUNCTION_______________________________________"""
def place_point (ligne):
    grid = [[0] * 2 for _ in range(ligne)]
    for i in range(ligne):
        grid[i][0] = random(1)
        grid[i][1] = random(1)
    return grid


def make_matrice(grid):
    matrice = [[0] * len(grid) for _ in range(len(grid))]
    print(len(matrice[0]))
    for i in range(len(grid)):
        for j in range(len(grid)):
            if i == j:
                matrice[i][j] = 0
            else:
                matrice[i][j] = get_dist(grid[i], grid[j])
    return matrice


def get_dist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def show_screen(grid):
    screen = tk.Tk()
    canva = tk.Canvas(screen, width=800, height=800, background='white')
    for i in range(len(grid)):
        canva.create_oval(floor(grid[i][0] * 800) - 10, floor(grid[i][1] * 800) - 10,floor(grid[i][0] * 800) + 10,
                          floor(grid[i][1] * 800) + 10, fill="blue")
    canva.pack()
    screen.mainloop()


def glouton(s, matrice):

    resultat = []
    visites = []

    for i in range(len(matrice)):
        visites.append(False)

    visites[s] = True
    x = s
    succ = 0

    while len(resultat) != len(matrice):
        min = matrice[x][0]
        for j in range(0, len(matrice)):
            if min > matrice[x][j] > 0 and visites[j] is False:
                succ = j
        resultat.append(succ)
        x = succ

    return resultat


"""______________________________________MAIN_______________________________________"""
grid = place_point(10)
matrice = make_matrice(grid)
result = glouton(5, matrice)

for i in range(len(result)):
    print(result, end=" ")

show_screen(grid)

