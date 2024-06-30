#!/usr/bin/python3

class Archive:
    #Init le fichier d'archive
    def __init__(self, filename):
        #Initialise une chaîne vide pour stocker les messages de log
        self.data = ""
        self.filename = filename
    
    def log(self, str, color="", section="", not_print=""):
        from utils import Colors
        #Méthode pour ajouter un message au log et l'afficher avec une couleur optionnelle
        if color:
            #afficher pas plus de 500chars
            print(color + str[:500] + Colors.RESET)
        elif not_print:
            self.data = self.data + str + '\n'
            return
        else:
            print(str[:500])
        #Ajoute le message au log interne
        self.data = self.data + str + '\n'

	#Méthode pour écrire les logs dans le fichier spécifié
    def to_file(self):
        with open(self.filename, "w") as f:
            f.write(self.data)