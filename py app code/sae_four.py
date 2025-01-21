import serial # Librairie gerant la communication serie -> module pyserial
from module_drawnow import *

nucleo_port = 'COM3' # Preciser ici le port serie. Ex.: "COM4"
nucleo_baudrate = 9600 # La frequence de la communication serie (baudrate)
nucleo_timeout = 3 # Delai d'attente maximale

nucleoData = serial.Serial(nucleo_port, nucleo_baudrate, timeout=nucleo_timeout) # Initialisation de la communication
nucleoData.reset_input_buffer() # Reinitialisation du buffer de reception

def read_valeur():
    with open("Z:\data.txt",'w') as data:
        run = True
        cnt = 0
        while run:
            while(nucleoData.inWaiting()==0): # On attend de recevoir des donnees.
                pass    # C'est Bloquant


            nucleoString = nucleoData.readline () # Recuperation du contenu de la ligne (fin de ligne: \n)
            string = nucleoString.split()
            print


            cnt = cnt+1

            try:
                """
                        Ecriture dans un fichier texte
                """
                # On decoupe la chaine de caractères (separateur: espace)
                temps = float(string[0].decode()) # Conversion de la chaine de caractere en nombre
                Temp_Consigne = float(string[1].decode())/10.0
                Temperature_TC = float(string[2].decode())/10.0
                commande = float(string[3].decode())
                valeurs = "{0:5.1f} {1:5.1f} {2:5.1f} {3:5.1f} \n".format(temps,Temp_Consigne,Temperature_TC, commande)
                data.write(valeurs)

                """
                    Tracage de la courbe
                """

                dataT.append([Temperature_TC]) # Ajout de la valeur à la liste dataT
                dataTconsigne.append([Temp_Consigne])
                dataC.append([commande])
                drawnow.drawnow(makeFig) # Rafraichissement de la figure matplotlib

                # Gestion des erreurs de transmission (pour eviter les valeurs qui ne pourraient être converties en float)
            except ValueError:
                print("Not a float: ", string)

            if cnt > 1000:
                dataT.pop(0) # Si plus de nb_points, enlever la première valeur de la liste dataT dataC.pop(0)
                nucleoData.reset_input_buffer() # On vide le buffer de reception
                nucleoData.close() # on libere le port serie

                run = False
                break

        time.sleep(1)

if __name__ == '__main__':
    read_valeur()
    print("Valeur Lu et tracer")
    print(dataC)

