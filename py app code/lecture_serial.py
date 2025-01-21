import serial # Librairie gerant la communication serie -> module pyserial

nucleo_port = 'COM7' # Preciser ici le port serie. Ex.: "COM4"
nucleo_baudrate = 9600 # La frequence de la communication serie (baudrate)
nucleo_timeout = 3 # Delai d'attente maximale

cnt = 0

nucleoData = serial.Serial(nucleo_port, nucleo_baudrate, timeout=nucleo_timeout) # Initialisation de la communication
nucleoData.reset_input_buffer() # Reinitialisation du buffer de reception


while 1:
    while(nucleoData.inWaiting()==0): # On attend de recevoir des donnees.
        pass    # C'est Bloquant


    nucleoString = nucleoData.readline () # Recuperation du contenu de la ligne (fin de ligne: \n)
    string = nucleoString.split()

    cnt = cnt+1

    try:
        # On decoupe la chaine de caractères (separateur: espace)
        temps = float(string[0].decode()) / 10.0 # Conversion de la chaine de caractere en nombre
        temperature = float(string[1].decode())/10.0
        commandeChauffage = float(string[2].decode())/10.0
        print(temps, temperature, commandeChauffage)

        # Gestion des erreurs de transmission (pour eviter les valeurs qui ne pourraient être converties en float)
    except ValueError:
        print("Not a float: ", string)

    if cnt > 10:
        print("Fin")
        nucleoData.reset_input_buffer() # On vide le buffer de reception
        nucleoData.close() # on libere le port serie
        break
