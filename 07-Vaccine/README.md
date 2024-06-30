# 🧪 TESTER LE PROJET:
source env/bin/activate

# [1] Lancer les containers
make all

[INFO] si config en amd64:
   docker run --platform linux/amd64 -it -d -p 8080:80 vulnerables/web-dvwa
   docker run --platform linux/amd64 -d -p 8000:80 gitlab.cylab.be:8081/cylab/play/sqlite-injection

# [2] Tester une URL avec la méthode GET par défaut:
a. Accédez à l'URL : http://localhost:8080/setup.php

b. Puis accédez à l'URL : http://localhost:8080/login.php

c. Utilisez les identifiants :
	Nom d'utilisateur: admin
	Mot de passe: password

d. http://localhost:8080/index.php
	get cookie value of `PHPSESSID`
	inspect -> Application tab -> Stockage -> Cookies
	
	Declarer la variable: export TOKEN=YOUR_COOKIE
e. make get

# [3] Tester une URL avec une méthode POST:
make post

# [4] Site additionnel pour tester les injections SQL:
make test

Commande pour excuter le programme : ./vaccine -o [file_name] -X [method] URL

# [5] Arrêter les Dockers
make clean

# [6] Arrêter et supprimer les Dockers
make fclean

# [Information PROGRAM]

- Detection des database : <SQLite> et <MySQL>
- Injections Type <Error> et <Union>

Les traces des opérations et des résultats sont stockés par défaut dans le fichier <default_archive.txt>

Le code teste d'abord la sensibilité de la database à travers une injection <booléene> type : "' or 1=1"

Le programme récupère les informations sensible via une injection type <UNION> :
" UNION SELECT null, null, null, column_name --"