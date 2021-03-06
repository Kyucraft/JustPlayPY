import time
import random
import tkinter as tk
from tkinter import *
class Player:
    tablo_player = []
    color = []
    def __init__(self,nom,classe,x,y): 
        self.classe = ClasseJ
        self._pv = classe._basepv
        self.x = x 
        self.y = y
        self.nom = nom 
        Map.joueur[self.nom] = self.x*10,self.y*10
        Map.prenom.append(self.nom)
        Player.tablo_player.append(self)
        Game.canva.bind_all('<space>',self.check_tour)

    def get_pv(self): 
        return self._pv

    def set_pv(self, val): 
        self._pv += val

    pv = property(get_pv, set_pv)       

    def caillou_verif(self):
        trajex = Game.canva.create_line(Map.joueur[Map.prenom[0]][0]+5,Map.joueur[Map.prenom[0]][1]+5  ,Map.joueur[Map.prenom[1]][0]+5  ,Map.joueur[Map.prenom[1]][1]+5 ,fill="red" )
        traj = list(Game.canva.find_overlapping(Game.canva.coords(trajex)[0],Game.canva.coords(trajex)[1] ,Game.canva.coords(trajex)[2] ,Game.canva.coords(trajex)[3]))

        traj = list(filter(lambda x: (x>=3) and (x<=22),traj))#1 et deux sont les deux joueurs , de 3 23 ce sont lesz obstacles , et de 24 a 124 ce sont les lignes du tableau 
        for i in range(len(traj)):
            obstacl_traj = list(Game.canva.find_overlapping(Map.obstacle_dic[traj[i]-3][0],Map.obstacle_dic[traj[i]-3][1],Map.obstacle_dic[traj[i]-3][0]+10,Map.obstacle_dic[traj[i]-3][1]+10))
            

            if obstacl_traj[-1] > 124:
                Game.canva.delete(list(filter(lambda x: x>124,list(Game.canva.find_all()))))
                return True
        Game.canva.delete(list(filter(lambda x: x>124,list(Game.canva.find_all()))))

        return False


    def check_tour(self,event):
        if Game.tour >= 4:
            Game.classe_game.check_change()
        Player.tablo_player[0].attaquer(Player.tablo_player[1])
        


    def attaquer(self,adv):
        touché_caillou = self.caillou_verif()
        degats = self.classe.appel_classe.arme.appel_arme.get_degats()
        resistance = adv.classe.appel_classe.baseforce
        degats = round(degats/resistance) * 10
            
        if touché_caillou == False:
            adv.set_pv(-degats)
            print(self.nom)
            Game.tour += 4


        advpv = adv.get_pv()
        selfpv = self.get_pv()
            #self.classe_game.implant('attaque')

        if (advpv <= 0) or (selfpv<=0):
            print(f'{Player.tablo_player[0].nom} a gagné')
            Game.fenetre.destroy()
        else:
            Game.classe_game.score()

        

        

class ClasseJ:
    appel_classe = 0
    def __init__(self,basepv,arme,baseforce):
        self._basepv=basepv
        self.arme = arme
        self.baseforce = baseforce
        ClasseJ.appel_classe = self

    def getpv(self):
        return self.basepv

    basepv = property(getpv)


class Arme:
    appel_arme = 0
    def __init__(self,nom,degats,portee):
        self._nom = nom
        self._degats = degats
        self.portee = portee
        Arme.appel_arme = self


    def get_nom(self):  
        return self._nom

    def set_nom(self, val): 
        self._nom = val

    nom=property(get_nom, set_nom)


    def get_degats(self):
        return self._degats

    def set_degats(self,val): 
        self._degats = val

    degats = property(get_degats,set_degats)
    




class Game:
    fenetre = tk.Tk()
    canva = tk.Canvas(fenetre, width=500+10, height=500+10)
    color_tablo=["red", "blue","green","yellow","purple","pink"]
    tour = 0
    classe_game = 0
    i = 0
    score_player_1=Label(fenetre)

    def __init__(self, largeur, hauteur, maap, p1, p2):
        self.largeur = largeur
        self.hauteur = hauteur
        self.maap = maap
        self.p1 = p1
        self.p2 = p2
        Game.classe_game = self 

    def droite(self,event): 
        self.bouger(10,0)


    def gauche(self,event):
        self.bouger(-10,0)


    def haut(self,event):
        self.bouger(0,-10)

    def bas(self,event):
        self.bouger(0,10)

    
    def check_change(self):
        if Game.tour >= 4:
            Game.tour = 0
            Game.i += 1
            Player.tablo_player.append(Player.tablo_player[0])
            Player.tablo_player.pop(0)  
            Map.trouv.append(Map.trouv[0])
            Map.trouv.pop(0)
            Map.prenom.append(Map.prenom[0])
            Map.prenom.pop(0)


        if Game.i%2 == 0:
            Game.fenetre.configure(bg=Game.color_tablo[Player.color[0]])
        else : 
            Game.fenetre.configure(bg=Game.color_tablo[Player.color[1]])

    def bouger(self,dx,dy):

        self.check_change()
        self.score()
        Game.canva.pack()
        
        #collision border

        Map.joueur[Map.prenom[0]]=Map.joueur[Map.prenom[0]][0] + dx ,Map.joueur[Map.prenom[0]][1] + dy
        if (Map.joueur[Map.prenom[0]][0] > 500) or (Map.joueur[Map.prenom[0]][1] > 500) or (Map.joueur[Map.prenom[0]][0]< 0) or (Map.joueur[Map.prenom[0]][1]< 0):
            Map.joueur[Map.prenom[0]]=Map.joueur[Map.prenom[0]][0] - dx ,Map.joueur[Map.prenom[0]][1] - dy
        else:
            Game.canva.move(Map.trouv[0],dx,dy)
        
        caillou_collision_player = list(Game.canva.find_overlapping(Map.joueur[Map.prenom[0]][0]+4,Map.joueur[Map.prenom[0]][1]+4 ,Map.joueur[Map.prenom[0]][0]+6 ,Map.joueur[Map.prenom[0]][1]+6))
        caillou_collision_player = list(filter(lambda x: (x>2) and (x<23),caillou_collision_player))
        if caillou_collision_player != []:
            Map.joueur[Map.prenom[0]]=Map.joueur[Map.prenom[0]][0] - dx ,Map.joueur[Map.prenom[0]][1] - dy
            Game.canva.move(Map.trouv[0],-dx,-dy)
        
        Game.tour+=1
                

        
    def creation(self, largeur, hauteur):
        Game.fenetre.geometry('%sx%s'%(self.largeur+50,self.hauteur+50))
        Game.canva.pack()

        for key in Map.joueur:#si dans joueur il y a un str alor le faire en bleue car c est un joueur
        
            Map.trouv.append(Game.canva.create_rectangle(Map.joueur[key][0],Map.joueur[key][1],Map.joueur[key][0]+10,Map.joueur[key][1]+10,fill=Game.color_tablo[Player.color[i]]))
            i+=1

        for i in range(len(Map.obstacle_dic)):
            Game.canva.create_rectangle(Map.obstacle_dic[i][0],Map.obstacle_dic[i][1],Map.obstacle_dic[i][0]+10,Map.obstacle_dic[i][1]+10,fill="black")

        for i in range(round(self.largeur/10)+1):
            Game.canva.create_line(i*10 ,0  ,i*10  ,self.largeur+10 , fill="grey")#colonnes

        for i in range(round(self.largeur/10)+1):
            Game.canva.create_line(0 , i*10 , self.largeur +10, i*10 , fill="grey")#lignes     

        Game.fenetre.configure(bg=Game.color_tablo[Player.color[0]])
        Game.score_player_1.configure(bg='green') 
        Game.score_player_1.pack()
        Bouton_Quitter=Button(Game.fenetre, text ='Quitter', command = Game.fenetre.destroy)#boutton pour quitter le jeu
        Bouton_Quitter.pack()


        Game.canva.bind_all('d', self.droite)#fleches directionnelles pour les events
        Game.canva.bind_all('q', self.gauche)
        Game.canva.bind_all('z', self.haut)
        Game.canva.bind_all('s', self.bas)
        Game.canva.bind_all('<space>',)
        
        Game.fenetre.mainloop()

    def score(self):
        
        player_12 = StringVar()

        player_12.set('En train de Jouer -->' +str(Player.tablo_player[0].nom)+' : '+str(Player.tablo_player[0].pv)+'\t'+'\t'+'Joue dans : ' +str(3 -Game.tour)+' '+str(Player.tablo_player[1].nom)+' : '+str(Player.tablo_player[1].pv))
        if 3 - Game.tour < 0:
            player_12.set('En train de Jouer -->' +str(Player.tablo_player[0].nom)+' : '+str(Player.tablo_player[0].pv)+'\t'+'\t'+'Joue dans : ' +str(0)+' '+str(Player.tablo_player[1].nom)+' : '+str(Player.tablo_player[1].pv))
        Game.score_player_1.configure(textvariable = player_12 )

        


class Map:

    trouv = []
    joueur = {}
    prenom = []
    obstacle_dic= {}

    def __init__(self,x,y,ob):
        self.x = x
        self.y = y
        self.ob = ob
        self.créer_obstacl(self.ob)


    def créer_obstacl(self,obstacle):
        '''
        obstacle:int
        '''
        for i in range(obstacle):
            Map.obstacle_dic[i] = random.randint(0,round(self.x/10))  *10 , random.randint(0, round(self.y/10)) *10
