#!/usr/bin/python3

import re
import difflib

class Colors():
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    RESET = '\033[0m'

#Compare deux chaînes de caractères et retourne les différences sous forme de chaîne de caractères
def get_diff(str1, str2):
	"""-difflib.unified_diff- Cette fonction compare les deux chaînes ligne par ligne
	transforme les chaînes de caractères str1 et str2 en listes de lignes. 
	Chaque ligne est un élément de la liste
	n = 0 signifie qu'aucune ligne de contexte supplémentaire ne sera incluse dans la sortie du diff.
	Seulement les lignes qui diffèrent seront affichées.
	Le résultat est stocké dans la variable diff"""
	diff = difflib.unified_diff(str1.splitlines(), str2.splitlines(), n = 0)
	ret = ""
    #"cnt": pour compter les lignes du diff
	cnt = 0
	for d in diff:
		cnt = cnt + 1
        #Ignore les trois premières lignes du diff (généralement des métadonnées)
		if cnt < 4:
			continue
		#Ignore les lignes qui commencent par "-" (lignes présentes uniquement dans str1)
		if d.startswith("-"):
			continue
		ret = ret + d[1:].strip() + '\n'
	return ret

#créer l'URL de renvoi
def form_url(url, add):
	if add == "#":
		return url
	if add.startswith('/'):
		if url.endswith('/'):
			# retire le dernier caractère de l'url
			url = url[:-1]
		return url + add

	baseurl_match = re.search(r'^(https?://[^/]+)', url)
	if not baseurl_match:
		error_exit(f"worng url - {url}")
	baseurl = baseurl_match.group()
	return baseurl + '/' + add

# Nettoie et formate les différences entre deux chaînes de caractères
def get_result(str1, str2, query=""):
	diff = get_diff(str1, str2)
	result = diff.replace("<b>", "")
	result = result.replace("</b>", "")
	result = re.sub('<(.|\n)*?>', '\n', result)
	result = re.sub('\n+', '\n', result)
	formatted_result = ""
	for line in result.split('\n'):
		#Verifie si la ligne n'est pas vide apres suppression des espaces
		if line.strip():
			formatted_result += f"{line.strip()}\n"
	return formatted_result

def error_exit(str):
	print(f"{Colors.RED}Error: {Colors.RESET}{str}")
	exit(1)

def error_continue(str):
	print(f"{Colors.RED}Error: {Colors.RESET}{str}")