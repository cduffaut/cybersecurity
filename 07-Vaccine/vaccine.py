import sys
import argparse
import os
import requests

from program import main_program

# - - - - - - [ Parsing Part ] - - - - - - # 

def my_path(arg):
	if os.path.exists(arg):
		print (f'\033[1;32;40m\n💡 The path {arg} does exist...\033[0;37;40m\n')
		return (arg)
	raise Exception('\033[1;31;40m\nInvalid path for the file.\n\033[0mPlease respect the format:\033[1;31;40m ./vaccine [-oX] URL\033[0m')	

def my_request(arg):
	arg = arg.lower()
	if arg == 'get' or arg == 'post':
		print (f'\033[1;32;40m\n💡 The request {arg} is valid...\033[0;37;40m\n')
		return arg
	raise Exception('\033[1;31;40m\nInvalid Type of Request.\n\033[0mPlease respect the format:\033[1;31;40m ./vaccine [-oX] URL\033[0m')

def my_url(arg):
	try:
		response = requests.head(arg)
		if response.status_code < 400:
			print(f'\033[1;32;40m\n💡 The URL {arg} is valid...\033[0;37;40m\n')
			return arg
	except requests.RequestException:
		pass
	raise Exception('\033[1;31;40m\nLast argument should be an URL.\n\033[0mPlease respect the format:\033[1;31;40m ./vaccine [-oX] URL\033[0m')

def main():
	sys.tracebacklimit = 0 # empécher les tracesbacks d'apparaitre
	
	if len( sys.argv) == 1:
		raise Exception('\033[1;31;40m\nURL is missing.\n\033[0mPlease respect the format:\033[1;31;40m ./vaccine [-oX] URL\033[0m')
	
	args = sys.argv[1:]
	url = args[-1]
	my_url(url)

	if len(args) > 5:
		print ('\033[1;31;40m\nInvalid number of arguments.\n\033[0mPlease respect the format:\033[1;31;40m ./vaccine [-oX] URL\033[0m')		

	X = False
	o = False
	request = None
	path = None

	for i, arg in enumerate(args):
		if arg == '-o':
			o = True
			if X:
				raise Exception('\033[1;31;40m\noption -o should be before the -X option.\n\033[0mPlease respect the format:\033[1;31;40m ./vaccine [-oX] URL\033[0m')
			if i + 1 < len(args) - 1 and args[i + 1] != '-X': # un chemin a été donné
				path = my_path(args[i + 1])
			else:
				if not os.path.exists('default_archive.txt'):
					file = open('default_archive.txt', "w") # Création du dossier par défaut
					file.close()
				path = 'default_archive.txt'
			print ('\033[1;32;40m\n💡 -o option has been activated...\033[0;37;40m\n')

		elif arg == '-X':
			X = True
			if i + 1 < len(args) - 1: # un type de requête a été donné
				if args[i + 1] == '-o':
					raise Exception('\033[1;31;40m\noption -o should be before the -X option.\n\033[0mPlease respect the format:\033[1;31;40m ./vaccine [-oX] URL\033[0m')
				else:
					request = my_request(args[i + 1])
			else:
				request = 'get'
			print ('\033[1;32;40m\n💡 -X option has been activated...\033[0;37;40m\n')

		elif i == 0 and i < (len(args) - 1) and arg not in ['-o', '-X']:
			raise Exception('\033[1;31;40m\nThe first argument is not accepted.\n\033[0mPlease respect the format:\033[1;31;40m ./vaccine [-oX] URL\033[0m')

		elif i < (len(args) - 1) and args[i + 1] not in ['-o', '-X'] and args[i - 1] not in ['-o', '-X']:  # vérifier qu'il n'y ai pas d'args en trop
			raise Exception('\033[1;31;40m\nAt least one argument is not accepted.\n\033[0mPlease respect the format:\033[1;31;40m ./vaccine [-oX] URL\033[0m')

	if request is None:
		request = "get"
	if path is None:
		path = "default_archive.txt"
	# récupérer les informations de l'injection	
	try:
		main_program(url, path, request)
	except Exception as e:
		print (f'\033[1;31;40m\nAn error occur during the injections tests: \033[0m{e}\n')
	return

if __name__ == '__main__':
	main()