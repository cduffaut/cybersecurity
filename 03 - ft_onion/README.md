# construire l'image
docker build -t <ID> .  

# lancer le container
docker run -p 80:80 -p 4242:4242 -d --name <NAME_CONTAINER> <ID>

# >>> Tester le projet <<<

# [1] Accéder à la page .onion:

# Commande pour entrer dans le conteneur:
docker exec -it <ID> bash

# Afficher l’adresse .onion :
cat /var/lib/tor/hidden_service/hostname

# [2] Tester l'accès SSH:

# 1. générer une clé ssh
ssh-keygen -t rsa -b 2048

# 2. Copier la clé publique dans le répertoire contenant le Dockerfile

cp ~/.ssh/id_rsa.pub /path/to/your/docker/build/context/

# 3. Lancer le conteneur
docker build -t onion_test .

docker run -p 80:80 -p 4242:4242 -d --name container_ft_onion onion_test

# 4. Tester la Connexion SSH
ssh -i ~/.ssh/id_rsa -p 4242 root@localhost

# [3] tester NGINX
http://localhost

# --------------------------------------------

# lister les containers actifs 
docker ps

# stoper container
docker stop [CONTAINER_ID_OR_NAME]

# supprimer le container
docker rm [CONTAINER_ID_OR_NAME]

# lister toutes les images Docker présentes sur la machine
docker images

# lister tous les conteneurs Docker
docker ps -a

# pour supprimer une image Docker
docker rmi IMAGE_ID

# Supprimer tous les conteneurs
docker rm $(docker ps -a -q)

# forcer la suppression de toutes les images
docker rmi -f $(docker images -q)