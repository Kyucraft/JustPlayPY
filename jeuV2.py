from _class_ import *
from def_armes_classe import *

class_correct = False 
class_dic = {'archer': archer,
            'archer lourd': archer_Lourd,
            'berserker':berserker,
            'chevalier':chevalier,
            'cavalier':chevalier}

def check_class(class_type):
    check = True
    try:
        travel = class_dic[class_type]
    except KeyError:
        print("Classe Inconnu")
        check = False
    return check


nom_j1 = input("Nom Joueur 1:")
nom_j2 = input("Nom joueur 2:")
while nom_j2 == nom_j1:
    nom_j2 = input("Nom joueur 2:")

while class_correct == False:
    class_type1 = input("Classe Joueur 1:")
    class_type2 = input("Classe Joueur 2:")
    if check_class(class_type1) == True and check_class(class_type2) == True:
        class_correct = True 


j1 = player(nom_j1, class_dic[class_type1],18,18)
j2 = player(nom_j2, class_dic[class_type2], 22, 22)
LARGEUR = 500
HAUTEUR = 500
mazp = Map(500, 500, 20)
jeu = Game(500, 500, mazp, j1, j2)
jeu.creation(LARGEUR, HAUTEUR)