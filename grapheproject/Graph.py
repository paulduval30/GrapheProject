from numpy.random import random
from math import *
import tkinter as tk

"""Classe qui fait le lien entre la vue et la simulation"""


class Controleur:
    #COnstructeur
    def __init__(self):
        self.algo = Algo(self)
        self.screen = Screen(self.algo)

    # update la frame
    def update_screen(self):
        self.screen.show_screen()
        self.screen.screen.update()

    # set le parcours affiché
    def set_display(self, display):
        self.screen.display = display

    # lance la simulation
    def run(self):
        self.algo.init_calcul()
        self.update_screen()
        self.algo.show_non_tri()
        self.screen.screen.mainloop()


"""Classe qui gère l'affichage"""


class Screen:
    # COnstructeur
    def __init__(self, algo):
        self.algo = algo
        self.screen = tk.Tk()
        self.display = algo.result_glouton
        self.frame = tk.Frame(self.screen)
        self.show_screen()

    # gere l'affichage du contenu de l'ecran
    def show_screen(self):
        self.frame.forget()
        self.frame = tk.Frame(self.screen)
        canva = tk.Canvas(self.frame, width=1000, height=800, background='white')
        if "graph" in self.display:
            rect1 = canva.create_rectangle(50, 700, 150, 700 - 6 * floor(self.algo.somme_glouton / 5 * 100), fill="red")
            rect2 = canva.create_rectangle(200, 700, 300, 700 - 6 * floor(self.algo.somme_decroise / 5 * 100), fill="blue")
            rect1 = canva.create_rectangle(350, 700, 450, 700 - 6 * floor(self.algo.somme_prim  / 5 * 100), fill="green")

            canva.create_line(0,700,500,700)
            canva.create_text(700,700, text="0")

            canva.create_line(0,700 - 6 * floor(self.algo.somme_glouton / 5 * 100),
                                                500, 700 - 6 * floor(self.algo.somme_glouton / 5 * 100))
            canva.create_text(700,700 - 6 * floor(self.algo.somme_glouton / 5 * 100), text=self.algo.somme_glouton, fill="red")
            canva.create_text(900,700 - 6 * floor(self.algo.somme_prim / 5 * 100), text=self.algo.somme_prim, fill="green")

            canva.create_line(0, 700 - 6 * floor(self.algo.somme_decroise / 5 * 100),
                              500, 700 - 6 * floor(self.algo.somme_decroise / 5 * 100))
            canva.create_text(900,700 - 6 * floor(self.algo.somme_decroise / 5 * 100) - 20, text=self.algo.somme_decroise, fill="blue")

        else:
            for i in range(1, len(self.display)):
                canva.create_line(floor(self.algo.grid[self.display[i - 1]][0] * 800),
                                  floor(self.algo.grid[self.display[i - 1]][1] * 800),
                                  floor(self.algo.grid[self.display[i]][0] * 800),
                                  floor(self.algo.grid[self.display[i]][1] * 800), fill="red")
            for i in range(len(self.algo.grid)):
                    canva.create_oval(floor(self.algo.grid[i][0] * 800) - 10, floor(self.algo.grid[i][1] * 800) - 10,
                                      floor(self.algo.grid[i][0] * 800) + 10,
                                      floor(self.algo.grid[i][1] * 800) + 10, fill="blue")

        bouton_glouton = tk.Button(self.frame, text ="Glouton", command=self.algo.show_glouton)
        bouton_prim = tk.Button(self.frame, text ="Prim", command=self.algo.show_prim)
        bouton_decroise = tk.Button(self.frame, text ="Decroise", command=self.algo.show_decroise)
        bouton_non_tri = tk.Button(self.frame, text="Non parcouru", command=self.algo.show_non_tri)
        bouton_graph = tk.Button(self.frame, text="Graph", command=self.algo.show_graph)

        canva_stat = tk.Canvas(self.frame, width=1000, height=50, background='white')
        canva_stat.create_text(100, 10, text="Moyenne glouton : " + str(self.algo.somme_glouton), fill="red")
        canva_stat.create_text(100, 25, text="Moyenne decroise : " + str(self.algo.somme_decroise), fill="blue")
        canva_stat.create_text(100, 40, text="Moyenne prim : " + str(self.algo.somme_prim), fill="green")
        """canva_stat.create_text(self.somme_glouton)
        canva_stat.create_text(self.somme_glouton)"""
        bouton_decroise.pack(side=tk.LEFT)
        bouton_prim.pack(side=tk.LEFT)
        bouton_glouton.pack(side=tk.LEFT)
        bouton_non_tri.pack(side=tk.LEFT)
        bouton_graph.pack(side=tk.LEFT)
        canva_stat.pack(side=tk.TOP)
        canva.pack()

        self.frame.pack()
        self.frame.update()


"""Classe qui gère la simulation"""
class Algo:
    # Constructeur de la classe
    def __init__(self, controleur):
        self.somme_glouton = 0
        self.somme_prim = 0
        self.somme_decroise = 0
        self.place_point(20)
        self.matrice = [[0.0] * len(self.grid) for _ in range(len(self.grid))]
        self.make_matrice()
        self.result = self.pvcprim(0)
        self.result_glouton = self.glouton(0)
        self.result_decroise = self.cheminminimaldecroise()
        self.result_non_tri = self.non_tri()
        self.controleur = controleur

    def place_point(self, ligne):
        self.grid = [[0.0] * 2 for _ in range(ligne)]
        for i in range(ligne):
            self.grid[i][0] = random(1)
            self.grid[i][1] = random(1)

    def make_matrice(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if i == j:
                    self.matrice[i][j] = 0
                else:
                    self.matrice[i][j] = self.get_dist(self.grid[i], self.grid[j])

    def get_dist(self, p1, p2):
        return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    # Méthode permetant de calculer la taille d'un chemin
    def somme_dist(self, chemin):
        somme = 0
        for i in range(0, len(chemin) - 1):
            somme += self.get_dist(self.grid[chemin[i]], self.grid[chemin[i + 1]])
        return somme

    # Méthode pour afficher glouton
    def show_glouton(self):
        self.controleur.set_display(self.result_glouton)
        self.controleur.update_screen()

    # Méthode pour afficher non tri
    def show_non_tri(self):
        self.controleur.set_display(self.result_non_tri)
        self.controleur.update_screen()

    # Méthode pour afficher Prim
    def show_prim(self):
        self.controleur.set_display(self.result)
        self.controleur.update_screen()

    # Méthode pour afficher chemin minimal decroise
    def show_decroise(self):
        self.controleur.set_display(self.result_decroise)
        self.controleur.update_screen()

    def show_graph(self):
        self.controleur.set_display(["graph", " "])
        self.controleur.update_screen()

    # Méthode permetant de générer le chemin avec Glouton
    def glouton (self, s):
        resultat = []
        visites = []

        for i in range(len(self.matrice)):
            visites.append(False)

        resultat.append(s)
        visites[s] = True

        x = s
        succ = 0

        while not estFini(visites):
            min = 100
            for i in range(len(self.matrice)):
                if not visites[i] and self.matrice[x][i] < min > 0:
                    min = self.matrice[x][i]
                    succ = i
            resultat.append(succ)
            visites[succ] = True
            x = succ
            succ = 0
        return resultat

    # Méthode permetant de générer le chemin minimal décroisé
    def cheminminimaldecroise(self):
        decroise = self.result_glouton.copy()
        n = len(decroise)
        ee = []
        for i in range(n):
            ee.append(0)
        while True:
            flag = 0
            for i in range(0, n - 1):
               for j in range(i + 1, n):
                   if intersection(i if i < n - 1 else i % n - 1, j if j < n - 1 else j % n - 1, self.grid, decroise):
                        flag = 1
                        for ii in range(0, n):
                            ee[ii] = decroise[(ii + i) % n]
                        for ii in range(0, n):
                            decroise[ii] = ee[ii]

                        aux = decroise[(j + 1 -i) % n]
                        decroise[(j + 1 - i) % n] = decroise[0]
                        decroise[0] = aux
                        g = j + 2 - i
                        d = n - 1

                        while g < d:
                            aux = decroise[g]
                            decroise[g] = decroise[d]
                            decroise[d] = aux
                            g += 1
                            d -= 1

                        j = n
                        i = n - 1
            if flag == 0:
                break
        return decroise

    # Méthode permetant de générer le chemin avec Prim
    def pvcprim(self, s):
        acm = []

        curent = s

        while len(acm) != len(self.matrice):
            acm.append(curent)
            tmp = self.get_next(acm, curent)
            curent = tmp if tmp != -1 else acm[len(acm) - 2]

        return acm

    # Méthode obtenir le sommet le plus proche d'un sommet courant et qui n'a pas encore été traité
    def get_next(self, acm, curent):
        min = 1000
        next = -1

        for i in range(len(self.matrice[curent])):
            if self.matrice[curent][i] != 0 and self.matrice[curent][i] < min and not i in acm:
                min = self.matrice[curent][i]
                next = i
        return next

    # lance une simulation sur 100 calculs
    def init_calcul(self):
        for i in range(100):
            self.place_point(20)
            self.make_matrice()
            self.result_glouton = self.glouton(0)
            self.result_decroise = self.cheminminimaldecroise()
            self.result = self.pvcprim(0)
            self.somme_glouton += self.somme_dist(self.result_glouton)
            self.somme_decroise += self.somme_dist(self.result_decroise)
            self.somme_prim += self.somme_dist(self.result)
            self.show_non_tri()

        self.somme_decroise = self.somme_decroise / 100
        self.somme_glouton = self.somme_glouton / 100
        self.somme_prim = self.somme_prim / 100

    # tableau contenant tout les liens entre tout les points
    def non_tri(self):
        result = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if( j > i):
                    result.append(i)
                    result.append(j)

        return result



"""_____________________________________OUTIL______________________________________"""

# Méthode savoir si le traitement est fini
def estFini(bool):
    for i in range(len(bool)):
        if not bool[i]:
            return False
    return True

# Méthode pour savoir si deux arrete se croise
def intersection(i, j, grid, result):
    sommet1 = grid[result[i]]
    sommet2 = grid[result[i + 1]]
    sommet3 = grid[result[j]]
    sommet4 = grid[result[j + 1]]
    abx = sommet2[0] - sommet1[0]
    aby = sommet2[1] - sommet1[1]
    acx = sommet3[0] - sommet1[0]
    acy = sommet3[1] - sommet1[1]
    adx = sommet4[0] - sommet1[0]
    ady = sommet4[1] - sommet1[1]
    det1 = abx * acy - aby * acx
    det2 = abx * ady - aby * adx
    cdx = sommet4[0] - sommet3[0]
    cdy = sommet4[1] - sommet3[1]
    cax = -acx
    cay = -acy
    cbx = sommet2[0] - sommet3[0]
    cby = sommet2[1] - sommet3[1]
    det3 = cdx * cay - cdy * cax
    det4 = cdx * cby - cdy * cbx
    return det1 * det2 < 0 and det3 * det4 < 0


"""______________________________________MAIN_______________________________________"""

ctrl = Controleur()
ctrl.run()

















