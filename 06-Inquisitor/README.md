🚨 Avant de lancer le programme: Donner accès Docker 🐳

1️⃣ Copier-Coller:
vi ~/Library/Group\ Containers/group.com.docker/settings.json

2️⃣ Aller au niveau de: "filesharingDirectories" 

📍 Ajouter une ',' a la fin de la dernière ligne du block,
📍 Puis retour à la ligne 
📍 Et ajouter "chemin/absolu/vers/dossier/projet/server" >> cd >> pwd + chemin vers le dossier "server"

3️⃣ 🚀 LANCER LE PROGRAMME
make build

4️⃣ 🔌 Se connecter via FileZilla:
lien: http://localhost:5800/
Host: ftp_server
Username: ftpuser
Password: ftppass
Port: 21
Cliquer sur "Quickconnect"

5️⃣ 🖥️ Récupérer la ligne de commande pour lancer le programme:
make run

6️⃣ 🥷🏻 Se placer dans le bash pour executer le programme:
make inquisitor

# 💤 Éteindre les Docker
make clean

# 💻 Récupérer les ips / MACs adresses des Docker
make info

# 📺 Se placer dans le bash du Docker ftp_server:
make server

# 📺 Se placer dans le bash du Docker ftp_client
make client

🛑 Si Erreur:
chmod 777 ./server
chmod 777 ./client

# 📑 Justifications projet et vocabulaire:

# def MAC:
Dans un réseau local (LAN) ou autre, l'adresse MAC (pour Media Access Control) constitue l'identifiant matériel unique d'un ordinateur.

# def IPV4
Une adresse IPv4 est une adresse IP dans la version 4 du protocole IP (IPv4)
Les adresses IPv4 sont des valeurs numériques codées sur 32 bits. Elles se composent de quatre nombres chacun compris entre 0 et 255 et séparés par un point.

# Rappel Docker
Un volume dans Docker est un mécanisme pour stocker des données de manière persistante, indépendamment du cycle de vie du conteneur. Les volumes permettent de partager des données entre le conteneur et l'hôte (la machine sur laquelle Docker s'exécute).

# Comment cela se passe pour l'aspect LINUX du projet
Image de base Python qui est basée sur Linux.
Instalation d'une dépendance spécifique à Linux.

# Socket Raw:
Un RAW socket est un socket dans lequel les champs des 
en-tetes des paquets envoyes sont remplis a la main. 
On accede donc a un niveau de programmation reseau assez bas 
puisqu'on atteint directement les couches de TCP/IP. 
Cela va nous permettre de forger des paquets comme bon nous semble.

# Utilisation de libpcap
Scapy utilise libpcap en arrière-plan pour la capture des paquets.

