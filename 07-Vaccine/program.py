#!/usr/bin/python3
import argparse
import requests
import re
import os
import difflib

from utils import Colors, get_diff, form_url, get_result, error_exit, error_continue
from archive import Archive
from error import Error
from tester import Tester
from union import Union

"""récupère la valeur de la variable d'environnement nommée TOKEN et l'assigne à la variable token
 utilise la méthode get de l'objet os.environ pour obtenir la valeur de TOKEN sans générer d'erreur 
 si la variable d'environnement n'existe pas. Si TOKEN n'est pas défini dans l'environnement, token sera None."""
token = os.environ.get('TOKEN')
"""crée un dictionnaire Python nommé cookies qui contient deux paires clé-valeur
    "security:low" > les mesures de sécurité minimales sont en place, facilitant ainsi les 
    tests de vulnérabilités"""
cookies = {'PHPSESSID': token, "security": "low"}

class Vaccine:
    #Initialise les paramètres pour les tests d'injection SQL sur une URL donnée
	def __init__(self, url, request):
		self.url = url
		self.method = request
    
		"""obtenir le contenu de la page cible:
		self.request est utilisée pour envoyer une requête HTTP GET à l'URL
		cible et récupérer le contenu de la page web"""

		#recupère le contenu de l'URL via la méthode GET
		txt = self.request()
		#Appel de la méthode get_form pour extraire le formulaire de la page cible
		form = self.get_form(txt)
		#recupère l'url sur lequel on va faire notre injection
		self.request_url = self.get_request_url(form)
		#obtenir les noms des champs du formulaire
		field = self.get_field_names(form)
		#Un formulaire de login contient au moins deux champs : un pour le nom d'utilisateur et un pour le mot de passe. Cependant, il peut y avoir des formulaires avec des champs supplémentaires (comme un champ de token, de captcha, etc.)
		#Cette condition est donc une précaution pour gérer les formulaires plus complexes.
		if len(field) >= 2:
			self.username_field_name = field[0]
			self.password_field_name = field[1]
		else:
			self.username_field_name = field[0]
			self.password_field_name = None

	"""Méthode spéciale : En Python, les méthodes spéciales sont des méthodes qui 
	commencent et se terminent par des doubles underscores (__). 
	Elles sont appelées automatiquement par Python dans certaines situations.
	__str__ : Cette méthode est appelée par la fonction str() et par print() 
	pour obtenir une représentation sous forme de chaîne de caractères de l'objet. 
	Elle est utilisée pour définir comment 
	l'objet doit être affiché sous forme de texte.

	La méthode __str__ de la classe Vaccine retourne une chaîne contenant les métadonnées de l'objet, 
	telles que l'URL, la méthode HTTP, et les champs du formulaire. 
	C'est utile pour avoir un aperçu rapide des propriétés de l'objet lorsqu'il est imprimé.

	Quand la fonction print() ou str() est appelée sur un objet, Python appelle 
	automatiquement la méthode __str__ de cet objet 
	pour obtenir sa représentation sous forme de chaîne.

	Lorsque print(vaccine) est exécuté, 
	Python appelle automatiquement vaccine.__str__() pour obtenir la chaîne à afficher."""

	def __str__(self):
		return f'''{Colors.GREEN}------ Data saved from the injection 🧪 ------{Colors.RESET}\n 
{Colors.CYAN}[URL]{Colors.RESET} {self.url}
{Colors.CYAN}[request-url]{Colors.RESET} {self.request_url}
{Colors.CYAN}[method]{Colors.RESET} {self.method}
{Colors.CYAN}[username-field]{Colors.RESET} {self.username_field_name}
{Colors.CYAN}[password-field]{Colors.RESET} {self.password_field_name}'''

	def get_form(self, txt):
        #Utilise une expression régulière pour trouver tous les formulaires dans le contenu de la page.
		forms = re.findall(r'(<form(.|\s)*?</form>)', txt)

		#Vérifie s'il n'y a pas de formulaire trouvé et affiche un message d'erreur si c'est le cas
		if not forms:
			error_exit("form block does not exist")
        #Initialise une liste pour stocker les formulaires filtrés
		filtered_froms = []
		for form in forms:
			method_match = re.search(r'method="(.*?)"', form[0])
			if not method_match:
				continue
			if method_match.group(1).lower() != self.method:
				continue
			filtered_froms.append(form[0])
        #Vérifie s'il n'y a pas de formulaire correspondant à la méthode HTTP 
		#et affiche un message d'erreur si c'est le cas
		if not filtered_froms:
			error_exit("method does not match")
		if len(filtered_froms) > 1:
			error_exit("multiple fields exist, cannot determin")
		return filtered_froms[0]

	#func pour extraire les noms des champs du formulaire
	def get_field_names(self, form):
		#Utilise une expression régulière pour trouver tous les champs d'entrée 
		#dans le formulaire et retourne leurs noms.
		return re.findall(r'<input[^>]+name="(.*?)"', form)

	"""
	La méthode get_request_url sert à déterminer l'URL de la requête à partir du formulaire exacte vers laquelle
	envoyer les données du formulaire. Quand un utilisateur soumet un formulaire sur une page web, les données sont généralement envoyées à une URL spécifique mentionnée dans l'attribut action de la balise <form>.
	Cette méthode récupère cette URL"""
	def get_request_url(self, form):
		#trouver toutes les occurrences de l'attribut action dans les balises <form> du HTML fourni
		actions = re.findall(r'<form[^>]+action="(.*?)"', form)
		if not actions:
			return self.url
		#Le code ne peut pas gérer plusieurs actions et considère cela comme une erreur
		if len(actions) > 1:
			error_exit("Error\nToo many actions found, can\'t process correctly this form")
		return form_url(self.url, actions[0])

	#func pour envoyer une requête GET à l'URL cible et obtenir le contenu de la page.
	def request(self, retry_count=2):
		#limite le nombre de retry pour les cookies pour ne pas aller dans une boucle inf
		if retry_count <= 0:
			error_exit("Error\nMax retries exceeded for the cookies.")
		try:
			#Envoie une requête GET à l'URL cible avec les cookies spécifiés
			response = requests.get(self.url, cookies=cookies)
			#Si une erreur de connexion se produit
		except requests.exceptions.ConnectionError:
			error_exit(f"Error\nConnection refused: {self.url}.")
		except Exception as e:
			error_exit(e)
		if response.status_code == 302:
			#Si le code de statut de la réponse est 302, affiche un message d'erreur indiquant qu'aucun cookie 
			#n'a été trouvé et renvoie la requête
			error_exit("Error\nNo cookie has been founded.")
			return self.request(retry_count - 1)

		if response.status_code != 200:
			error_exit(f"{self.url} - {response}")
		#Le contenu text qui sera renvoyé: HTML d'une page web, Données d'une API REST, Messages d'erreur ou de statut
		return response.text

    #Soumet un formulaire avec les données d'injection SQL.
	def submit(self, username, password="password"):
        #méthode submit: soumet les informations d'authentification au formulaire
		#Si le champ de mot de passe existe, 
		#Crée un dictionnaire payload avec les noms d'utilisateur et de mot de passe
		if self.password_field_name:
			payload = {
				self.username_field_name: username,
				self.password_field_name: password
			}
		else:
            #crée un dictionnaire payload avec le nom d'utilisateur et un champ "Submit"
			payload = {
				self.username_field_name: username,
				"Submit" : "Submit"
				"""Lorsque le formulaire ne contient pas de champ de mot de passe, il peut représenter des 
				actions comme une recherche, une soumission simple ou d'autres interactions. Dans ce cas, 
				l'inclusion du bouton de soumission ("Submit": "Submit") peut être nécessaire 
				pour indiquer au serveur que le formulaire a été soumis"""
			}

		if self.method == "get":
            #Si la méthode HTTP est GET, envoie une requête GET avec les paramètres payload...
			res = requests.get(self.request_url, params=payload, cookies=cookies)
		elif self.method == "post":
			res = requests.post(self.request_url, data=payload, cookies=cookies)
		return res

	def vaccine(self):
		try:
			"""Essaye d'effectuer une injection SQL avec le caractère #. Crée une instance de Tester et Error, 
			obtient le nombre de colonnes et effectue une union SQL"""
			injection_tester = Tester(self.submit, "#")
			e = Error(injection_tester)
			column_counts = e.error()
			u = Union(injection_tester, column_counts)
			u.union()
		except Error.ErrorException or Union.UnionException as e:
			"""permet de continuer le programme même après avoir rencontré une erreur,
			ce qui est important dans un contexte de tests où plusieurs tentatives 
			d'injection peuvent être nécessaires."""
			error_continue(e)
		try:
			injection_tester = Tester(self.submit, "--")
			e = Error(injection_tester)
			column_counts = e.error()
			u2 = Union(injection_tester, column_counts)
			u2.union()
		except Error.ErrorException or Union.UnionException as e:
			error_continue(e)

def main_program(url, path, request):
	#variable globale final_archive qui sera utilisée pour enregistrer les logs tout au long du programme
	global final_archive
	#initialisation l'objet Archive avec le nom de fichier passé en argument
	#Cet objet gère l'écriture des logs dans un fichier
	final_archive = Archive(path)

	#Crée une instance de la classe Vaccine en passant l'URL cible, le type de requête et une option pour l'entrée utilisateur. 
	#La classe Vaccine contient la logique principale pour tester les injections SQL
	vaccine = Vaccine(url, request)

	#Appel de la méthode vaccine de l'instance Vaccine
	#C'est ici que les tests d'injection SQL sont effectuées
	final_archive.log("Starting SQL Injection Test", section="INFO")
	vaccine.vaccine()

	#Imprime les informations de l'objet Vaccine, 
	#Comme l'URL cible, les champs de formulaire détectés, etc
	final_archive.log("SQL Injection Test Completed!\n", section="INFO")
	print(vaccine)
	final_archive.log(f'''------ Data saved from the injection 🧪 ------\n 
[URL] {vaccine.url}
[request-url] {vaccine.request_url}
[method] {vaccine.method}
[username-field] {vaccine.username_field_name}
[password-field] {vaccine.password_field_name}''', not_print="NOP")
	#Appel de la méthode to_file de l'objet Archive pour sauvegarder les logs dans le fichier spécifié
	final_archive.to_file()
