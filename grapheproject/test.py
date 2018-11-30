from numpy.random import random
from math import *
import tkinter as tk

"""______________________________________FUNCTION_______________________________________"""
def place_point (ligne):
    grid = [[0.0] * 2 for _ in range(ligne)]
    for i in range(ligne):
        grid[i][0] = random(1)
        grid[i][1] = random(1)
    return grid


def make_matrice(grid):
    matrice = [[0.0] * len(grid) for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid)):
            if i == j:
                matrice[i][j] = 0
            else:
                matrice[i][j] = get_dist(grid[i], grid[j])
    return matrice


def get_dist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def show_screen(grid, result):
    screen = tk.Tk()
    canva = tk.Canvas(screen, width=800, height=800, background='white')
    for i in range(len(grid)):
        if result[0] != i:
            canva.create_oval(floor(grid[i][0] * 800) - 10, floor(grid[i][1] * 800) - 10,floor(grid[i][0] * 800) + 10,
                          floor(grid[i][1] * 800) + 10, fill="blue")
        else:
            canva.create_oval(floor(grid[i][0] * 800) - 10, floor(grid[i][1] * 800) - 10, floor(grid[i][0] * 800) + 10,
                              floor(grid[i][1] * 800) + 10, fill="red")
        canva.create_text(floor(grid[i][0] * 800), floor(grid[i][1] * 800), text=i, font="Arial 12", fill="white")
    for i in range(1, len(result)):
        canva.create_line(floor(grid[result[i - 1]][0] * 800), floor(grid[result[i - 1]][1] * 800),
                          floor(grid[result[i]][0] * 800), floor(grid[result[i]][1] * 800))

    canva.pack()
    screen.mainloop()


def glouton2 (s, matrice):
    resultat = []
    visites = []

    for i in range(len(matrice)):
        visites.append(False)

    resultat.append(s)
    visites[s] = True

    x = s
    succ = 0

    while not estFini(visites):
        min = 100
        for i in range(len(matrice)):
            if not visites[i] and matrice[x][i] < min > 0:
                min = matrice[x][i]
                succ = i
        resultat.append(succ)
        visites[succ] = True
        x = succ
        succ = 0
    return resultat


def estFini(bool):
    for i in range(len(bool)):
        if not bool[i]:
            return False
    return True

"""______________________________________MAIN_______________________________________"""
grid = place_point(10)
matrice = make_matrice(grid)
result = glouton2(0, matrice)

print(result)
for i in range(len(matrice)):
    for j in range(len(matrice[i])):
        print(matrice[i][j], end=" | ")
    print("\n")

show_screen(grid, result)

