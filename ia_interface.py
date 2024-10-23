import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import copy
from numpy import *
import copy
import time
from tkinter import messagebox

class tree:
    def __init__(self, data,parent):
        self.data = data
        self.parent = parent




def estEtatFinal(t):
    tf = [["1", "2", "3"], ["8", "", "4"], ["7", "6", "5"]]
    for i in range(3):
        for j in range(3):
            if t[i][j] != tf[i][j]:
                return False
    return True


def position(x, t):
    for i in range(3):
        for j in range(3):
            if t[i][j] == x:
                return i, j


def transitions(x, t):
    l, c = position(x, t)
    d = {"haut": -1, "gauche": -1, "bas": -1, "droite": -1}
    
    if l > 0:
        d["haut"] = t[l - 1][c]
    if l < 2 and l > 0:  # Empêche le mouvement de la dernière ligne à la première
        d["bas"] = t[l + 1][c]
    if c > 0:
        d["gauche"] = t[l][c - 1]
    if c < 2:
        d["droite"] = t[l][c + 1]
    
    return d



def position_case_vide(t):
    for i in range(3):
        for j in range(3):
            if t[i][j] == "":
                return i, j


def permuter(t, c1, c2):
    x1, y1 = position(c1, t)
    x2, y2 = position(c2, t)
    t[x1][y1], t[x2][y2] = t[x2][y2], t[x1][y1]
    return t


def afficher_taquin(t):
    print("____________________________")
    for i in range(3):
        for j in range(3):
            if t[i][j]=='':
                print('0', end=" ")
            else:
                print(t[i][j], end=" ")
            
        print()


def afficher_taquin_list(liste):
    for t in liste:
        afficher_taquin(t)


def nb_neuds(t):
    l, c = position("", t)
    if l == 1 and c == 1:
        return 4
    elif (l == 0 or l == 2) and (c == 0 or c == 2):
        return 2
    else:
        return 3


def comparer(t, t1):
    for i in range(3):
        for j in range(3):
            if t[i][j] != t1[i][j]:
                return False
    return True


def recherche(t, ch,interface):
    for i in range(3):
        for j in range(3):
            while "\n" in t[i][j]:
                t[i][j] = t[i][j].replace("\n", "")
    if estEtatFinal(t):
        return t,0,0
    head= tree(t,None)
    trees=[]
    trees.append(head)
    freeNodes = [t]
    closedNodes = []
    goalNode = []
    success = False
    z = 1
    nb_visite = 0
    nb_generer = 0
    i=0
    while freeNodes and not success:
        
        firstNode = freeNodes[0]
        freeNodes = freeNodes[1:]
        firsttree=trees[i]
        i+=1
        closedNodes.append(firstNode)
        nb_visite += 1
        generatedStates = []

        d = transitions('',firstNode)
        for valeur in d.values():
            if valeur != -1:
                t_permut = permuter(copy.deepcopy(firstNode), "", valeur)
                trees.append(tree(t_permut,firsttree) )
                generatedStates.append(t_permut)
                nb_generer += 1

        generatedStates = [
            s for s in generatedStates if s not in freeNodes and s not in closedNodes
        ]

        for s in generatedStates:
            if estEtatFinal(s):
                success = True
                goalNode = s
        if ch == "DFS":
            freeNodes2 = generatedStates
            freeNodes2.extend(freeNodes)
            freeNodes = freeNodes2
        else:
            freeNodes2 = freeNodes
            freeNodes2.extend(generatedStates)
            freeNodes = freeNodes2

        z += 1
        # Update the interface with the current state of the puzzle
        # Update the interface to refresh the display
        # Add a small delay for visualization
        #time.sleep(1)
        afficher_taquin(firstNode)
    a=trees[-1]
    print(trees)
    while a.parent!=None:
        time.sleep(1)




        
        interface.init_taquin2(a.data)
        interface.update()
        print(a.data)
        a=a.parent
    return goalNode, nb_visite, nb_generer
"""def recherche(t, ch, interface):
        for i in range(3):
            for j in range(3):
                while "\n" in t[i][j]:
                    t[i][j] = t[i][j].replace("\n", "")
        if estEtatFinal(t):
            return t, 0, 0
        freeNodes = [t]
        closedNodes = []
        goalNode = []
        success = False
        z = 1
        nb_visite = 0
        nb_generer = 0
        while freeNodes and not success:
            firstNode = freeNodes[0]
            freeNodes = freeNodes[1:]
            closedNodes.append(firstNode)
            nb_visite += 1
            generatedStates = []

            d = transitions('',firstNode)
            for valeur in d.values():
                if valeur != -1:
                    t_permut = permuter(copy.deepcopy(firstNode), "", valeur)
                    generatedStates.append(t_permut)
                    nb_generer += 1

            generatedStates = [
                s for s in generatedStates if s not in freeNodes and s not in closedNodes
            ]

            for s in generatedStates:
                if estEtatFinal(s):
                    success = True
                    goalNode = s
                    break
            if ch == "DFS":
                freeNodes.extend(generatedStates)
            else:
                freeNodes = generatedStates + freeNodes

            z += 1
            # Update the interface with the current state of the puzzle
            interface.init_taquin2(firstNode)
            # Update the interface to refresh the display
            interface.update()
            # Add a small delay for visualization
            time.sleep(0.5)

        return goalNode, nb_visite, nb_generer"""


def rechercheDFSL(t, interface, L=3):
    for i in range(3):
        for j in range(3):
            while "\n" in t[i][j]:
                t[i][j] = t[i][j].replace("\n", "")
    if estEtatFinal(t):
        return t, 0, 0
    
    nb_visite = 0
    nb_generer = 0
    while True:
        freeNodes = [(t, 0)]  
        closedNodes = []
        goalNode = []
        success = False

        while freeNodes and not success:
            firstNode, depth = freeNodes[0]
            freeNodes = freeNodes[1:]
            if depth <= L:  
                closedNodes.append(firstNode)
                nb_visite += 1
                generatedStates = []
                d = transitions('',firstNode)
                for valeur in d.values():
                    if valeur != -1:
                        t_permut = permuter(copy.deepcopy(firstNode), "", valeur)
                        generatedStates.append((t_permut, depth + 1))  
                        nb_generer += 1

                generatedStates = [
                    s for s in generatedStates if s not in freeNodes and s not in closedNodes
                ]

                for s, d in generatedStates:
                    if estEtatFinal(s):
                        success = True
                        goalNode = s
                        break

                freeNodes.extend(generatedStates)
            else:
                break  
            # Update the interface with the current state of the puzzle
            interface.init_taquin2(firstNode)
            # Update the interface to refresh the display
            interface.update()
            # Add a small delay for visualization
            time.sleep(0.5)   

        if success:
            
            return goalNode, nb_visite, nb_generer
        else:
            L += 1  
            print("Augmentation de la profondeur limite à", L)


import copy

def heuristique(etat):
    # Heuristique pour A* - nombre de jetons mal placés
    count = 0
    for i in range(3):
        for j in range(3):
            if etat[i][j] != '' and etat[i][j] != str(3 * i + j + 1):
                count += 1
    return count

def rechercheA(t, interface):
    for i in range(3):
        for j in range(3):
            while "\n" in t[i][j]:
                t[i][j] = t[i][j].replace("\n", "")
    if estEtatFinal(t):
        return t,0,0
    freeNodes = [t]
    closedNodes = []
    goalNode = []
    success = False
    z = 1
    nb_visite = 0
    nb_generer = 0
    while freeNodes and not success:

        
        min_cost = float('inf')
        min_node_index = -1
        for i, node in enumerate(freeNodes):
            cost = z + heuristique(node)
            if cost < min_cost:
                min_cost = cost
                min_node_index = i
        
        firstNode = freeNodes.pop(min_node_index)
        closedNodes.append(firstNode)
        nb_visite += 1
        interface.init_taquin2(firstNode)
        interface.update()
        time.sleep(1) 
        generatedStates = []

        d = transitions('',firstNode)
        for valeur in d.values():
            if valeur != -1:
                t_permut = permuter(copy.deepcopy(firstNode), "", valeur)
                generatedStates.append(t_permut)
                nb_generer += 1

        generatedStates = [
            s for s in generatedStates if s not in freeNodes and s not in closedNodes
        ]

        for s in generatedStates:
            if estEtatFinal(s):
                success = True
                goalNode = s
        
        freeNodes = generatedStates + freeNodes

        z += 1

    return goalNode, nb_visite, nb_generer

"""def h(etat):
    # Heuristique pour A* - nombre de jetons mal placés
    count = 0
    for i in range(3):
        for j in range(3):
            if i < len(etat) and j < len(etat[i]) and etat[i][j] != '' and etat[i][j].isdigit() and int(etat[i][j]) != 3 * i + j + 1:
                count += 1
    return count


def heuristique(etat):
    # Heuristique pour A* - nombre de jetons mal placés
    count = 0
    for i in range(3):
        for j in range(3):
            if etat[i][j] != '' and etat[i][j] != str(3 * i + j + 1):
                count += 1
    return count

def rechercheA(etat_depart, interface):
    closedNodes = []
    freeNodes = [(heuristique(etat_depart), etat_depart)]
    goalNode = None  # Initialiser goalNode à None
    success = False
    nb_visite = 0
    nb_generer = 0

    while freeNodes:
        _, currentNode = freeNodes.pop(0)
        closedNodes.append(currentNode)
        nb_visite += 1
        interface.init_taquin2(currentNode)
        interface.update()
        time.sleep(0.5) 

        if estEtatFinal(currentNode):
            success = True
            goalNode = currentNode
            break

        generatedStates = transitions(currentNode)
        nb_generer += len(generatedStates) 
        for state in generatedStates:
            if state not in closedNodes:
                freeNodes.append((heuristique(state), state))
                freeNodes.sort(key=lambda x: x[0])

    return goalNode, nb_visite, nb_generer"""


def pasInit(taquin):
        for i in range(3):
            for j in range(3):
                if taquin[i][j] != "":
                    return False
        return True

class TaquinInterface(tk.Tk):
    def __init__(self):
        
        super().__init__()
        
        self.title("Interface du Jeu du Taquin")
        self.geometry("800x600")
        self.configure(background="white")
        self.initUI()

    def initUI(self):
        self.labels = []
        for i in range(3):
            row = []
            for j in range(3):
                background_color = (
                    "#334EAC" if i == 0 else ("#7096D1" if i == 1 else "#D0E3FF")
                )
                label = tk.Label(
                    self,
                    text="\n" * 2,
                    width=13,
                    anchor="center",
                    borderwidth=1,
                    relief="solid",
                    foreground="white",
                    background=background_color,
                    font=("Arial", 12),highlightbackground="white"
                )
                
                label.grid(
                    row=i + 1, column=j + 1, padx=0, pady=0
                )  
                row.append(label)
            self.labels.append(row)

        
        self.style = ttk.Style()
        self.style.configure(
            "My.TButton",
            borderwidth=1,
            relief="solid",
            foreground="black",
            background="white",
        )

        # Bouton d'initialisation
        
        
        self.init_button = tk.Button(self, text="Init", command=self.init_taquin,bg="#334EAC",fg="white", font=("Arial", 10, "bold"), width=10)
        self.init_button.grid(row=2, column=6, padx=5, pady=5, rowspan=1)

        # Boutons pour les algorithmes
        self.algo_labels = ["DFS", "DFSL", "BFS", "A*"]
        self.algo_buttons = []
        for i, algo in enumerate(self.algo_labels):
            button = tk.Button(
                self, text=algo, command=lambda algo=algo: self.run_algorithm(algo),bg="#334EAC",fg="white", font=("Arial", 10, "bold"), width=10
            )
            button.grid(row=6, column=i + 1, padx=5, pady=5)
            self.algo_buttons.append(button)

        # Cadres pour les informations
        self.info_frames = {}
        info_labels = ["Nb visités", "Nb générés", "Temps \n d’exécution"]
        max_label_length = max(len(label) for label in info_labels)

        x = 0
        for label in info_labels:

            frame = tk.Frame(self, borderwidth=1, relief="solid",bg="#334EAC")
            frame.grid(row=7 + x, column=0, padx=5, pady=5, sticky="nsew")
            self.info_frames[label] = frame

            frame.grid_columnconfigure(0, minsize=max_label_length)

            tk.Label(frame, text=label, bg="#334EAC", fg="white", font=("Arial", 10, "bold"), width=10).grid(row=0, column=0, sticky="nsew")


            # Création des champs vides et de leurs cadres
            for i in range(4):
                empty_frame = tk.Frame(self, borderwidth=1, relief="solid",bg="white")
                empty_frame.grid(row=7 + x, column=i + 1, padx=5, pady=5, sticky="nsew")

                empty_label = tk.Label(
                    empty_frame, text="", width=5, anchor="center", background="white"
                )
                empty_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

            x += 1

    def init_taquin(self):
        # initialisation du taquin avec le taquin initial
        self.taquin = [["1", "2", "3"], ["8", "6", ""], ["7", "5", "4"]]

        # affichage du taquin initial
        for i in range(3):
            for j in range(3):
                if self.taquin[i][j] == "":
                    self.labels[i][j].config(text="\n" * 2)
                else:
                    self.labels[i][j].config(text="\n" + str(self.taquin[i][j]) + "\n")

    def init_taquin2(self, taquin_test):
        
        # Affichage du taquin initial
        for i in range(3):
            for j in range(3):
                if taquin_test[i][j] == "":
                    self.labels[i][j].config(text="\n" * 2)
                else:
                    self.labels[i][j].config(text="\n" + str(taquin_test[i][j]) + "\n")

    def run_algorithm(self, algo):
        taquin = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(self.labels[i][j].cget("text"))
            taquin.append(row)
        
        for i in range(3):
            for j in range(3):
                while "\n" in taquin[i][j]:
                    taquin[i][j] = taquin[i][j].replace("\n", "")
        if pasInit(taquin):
            messagebox.showwarning("Alerte", "Veuillez initialiser le Taquin !")
            return

        if algo == "DFS":
            start_time = time.time()
            result, nb_visites, nb_genere = recherche(taquin, "DFS",self)
            end_time = time.time()
            temps_execution = end_time - start_time
            temps_execution = round(temps_execution, 5)
            info_values = [nb_visites, nb_genere, temps_execution]
            j = 0
            for x in range(3):
                empty_frame = tk.Frame(self, borderwidth=1, relief="solid",bg="white")
                empty_frame.grid(row=7 + x, column=1, padx=5, pady=5, sticky="nsew")
                empty_label = tk.Label(
                    empty_frame,
                    text=str(info_values[j]),
                    width=10,
                    anchor="center",
                    background="white",
                )
                empty_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                j += 1

        elif algo == "BFS":
            start_time = time.time()
            result, nb_visites, nb_genere = recherche(taquin, "BFS", self)
            end_time = time.time()
            temps_execution = end_time - start_time
            temps_execution = end_time - start_time
            temps_execution = round(temps_execution, 5)
            info_values = [nb_visites, nb_genere, temps_execution]
            j = 0
            for x in range(3):
                empty_frame = tk.Frame(self, borderwidth=1, relief="solid",bg="white")
                empty_frame.grid(row=7 + x, column=3, padx=5, pady=5, sticky="nsew")
                empty_label = ttk.Label(
                    empty_frame,
                    text=str(info_values[j]),
                    width=10,
                    anchor="center",
                    background="white",
                )
                empty_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                j += 1
        elif algo == "DFSL":
            start_time = time.time()
            result, nb_visites, nb_genere = rechercheDFSL(taquin,self,  L=3)
            end_time = time.time()
            temps_execution = end_time - start_time
            temps_execution = end_time - start_time
            temps_execution = round(temps_execution, 5)
            info_values = [nb_visites, nb_genere, temps_execution]
            j = 0
            for x in range(3):
                empty_frame = tk.Frame(self, borderwidth=1, relief="solid",bg="white")
                empty_frame.grid(row=7 + x, column=2, padx=5, pady=5, sticky="nsew")
                empty_label = tk.Label(
                    empty_frame,
                    text=str(info_values[j]),
                    width=10,
                    anchor="center",
                    background="white",
                )
                empty_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                j += 1
        else:
            start_time = time.time()
            result, nb_visites, nb_genere = rechercheA(taquin,self)
            end_time = time.time()
            temps_execution = end_time - start_time
            temps_execution = end_time - start_time
            temps_execution = round(temps_execution, 5)
            info_values = [nb_visites, nb_genere, temps_execution]
            j = 0
            for x in range(3):
                empty_frame = tk.Frame(self, borderwidth=1, relief="solid",bg="white")
                empty_frame.grid(row=7 + x, column=4, padx=5, pady=5, sticky="nsew")
                empty_label = tk.Label(
                    empty_frame,
                    text=str(info_values[j]),
                    width=10,
                    anchor="center",
                    background="white",
                )
                empty_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                j += 1
            

        # Afficher le résultat dans les étiquettes d'informations
        if result:
            self.init_taquin2(result)
            
        else:
            print("Aucun résultat trouvé.")

    

app = TaquinInterface()
app.mainloop()
