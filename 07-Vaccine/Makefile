#DVWA: Application multi-vulnérabilités
#Utilise MySQL comme backend de base de données
#Sqlite-injection: Utilise SQLite comme dt_base
all:
	-docker run -it -d -p 8080:80 vulnerables/web-dvwa
	-docker run -d -p 8000:80 gitlab.cylab.be:8081/cylab/play/sqlite-injection

#Démontrer et tester les vulnérabilités liées à l'injection SQL, en particulier avec MySQL comme base de données
#fait référence à l'application DVWA qui est configurée pour s'exécuter dans un conteneur Docker mappé au port 8080 de l'hôte
get:
	@echo token=$(TOKEN)
	python3 vaccine.py http://localhost:8080/vulnerabilities/sqli/index.php

#fait référence à l'application sqlite-injection qui est configurée pour s'exécuter dans 
#un conteneur Docker mappé au port 8000 de l'hôte
post:
	python3 vaccine.py -X post http://localhost:8000

# Test du programme avec le méthode POST (-X post)
#altoromutual.com=site web fictif simulant un site bancaire conçue pour 
#contenir diverses vulnérabilités de sécurité courantes, y compris des vulnérabilités d'injection SQL
#dt_base MySQL
test:
	python3 vaccine.py  -X post http://altoromutual.com/login.jsp

clean:
	docker system prune

# -z pour verifier si la chaine est "vide"
fclean:
	docker system prune -f
	CONTAINERS=$$(docker ps -a -q); \
	if [ ! -z "$$CONTAINERS" ]; then \
		docker stop $$CONTAINERS; \
		docker rm $$CONTAINERS; \
	fi

.PHONY: fclean, clean, post, get, test