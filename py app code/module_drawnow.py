import math # utile pour le test
import time # utile pour le test

import matplotlib.pyplot as plt # Librairie graphique
import drawnow # Librairie pour rafraichir une figure matplotlib

T_ylabel = 'Temperature [°C]' # Titre des ordonnees
xlabel = 'Temps' # Titre des abscisses
C_ylabel = 'Commande [0-100%]'
mon_style= 'r-' # Style de la courbe
nb_points = 30 # Nombre de points sur le graphique

"""run = True # Gestion de la boucle principale"""

# Gestion de l'evenement "fermeture de la fenetre"
def handle_close(evt):
    global run
    run = False
    print('Fermeture figure!')
    plt.close(fig)

fig = plt.figure() # Creation de la figure
fig.canvas.mpl_connect('close_event', handle_close)

dataT = [] # Listes des donnees
dataTconsigne = []
dataC = []

plt.ion() # Mode interactif
#cnt = 0 # Compteur du nombre de points

def makeFig(): # Fonction pour tracer le graphique
    plt.subplot(211)
    plt.ylim(0,300)
    plt.grid(True)
    plt.ylabel(T_ylabel)
    plt.plot(dataT, mon_style)
    plt.plot(dataTconsigne,"b-")
    plt.subplot(212)
    plt.ylim(0,100)
    plt.grid(True)
    plt.ylabel(C_ylabel)
    plt.plot(dataC, mon_style)

    """
while run:
    try:
        cnt=cnt+1
        temperature = 20*math.sin(2*math.pi*cnt/10.0)+30 # Simulation temperature mesuree
        commandeChauffage = 50*math.cos(2*math.pi*cnt/10.0)+50 # Simulation commande chauffage
        dataT.append([temperature]) # Ajout de la valeur à la liste dataT
        dataC.append([commandeChauffage])
        drawnow.drawnow(makeFig) # Rafraichissement de la figure matplotlib

        if(cnt>nb_points):
            dataT.pop(0) # Si plus de nb_points, enlever la première valeur de la liste dataT dataC.pop(0)

    except ValueError:# Inutile ici mais permettra de gerer des erreurs de transmission
                # (pour eviter les valeurs qui ne pourraient être converties en float)
        print("erreur")

    time.sleep(1) # Cadence de la boucle principale (=1[s])  utile pour le test
    """
