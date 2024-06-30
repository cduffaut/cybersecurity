#!/usr/bin/python3

class Tester:
    def __init__(self, submit, payload):
        self.submit = submit
        self.delimiter = "'"
        self.payload = payload
        #Stockent les réponses initiales pour la comparaison
        #stocke la réponse du serveur lorsque le formulaire est soumis sans aucun payload
        self.original_text = self.submit("").text
        #stocke la réponse du serveur lorsque le formulaire est soumis avec un payload contenant une tentative d'injection SQL simple
        self.normal_text = self.submit("' or 1=1" + self.payload).text