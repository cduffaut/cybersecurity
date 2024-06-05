#!/bin/bash

# Créer le répertoire pour SSH
mkdir -p /run/sshd
chmod 755 /run/sshd

# Configurer les permissions des fichiers et répertoires SSH
chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys

# Créez le répertoire pour le service caché Tor
mkdir -p /var/lib/tor/hidden_service/
chmod 700 /var/lib/tor/hidden_service/

# Démarrer le serveur SSH
# & permet de démarrer le service 
# En parallèle avec les autres services
/usr/sbin/sshd -D &

# Démarrer le service Tor
tor &

# Attendre quelques secondes pour s'assurer que Tor a le temps de démarrer et créer le service caché
sleep 10

# Afficher l'URL du service caché Tor
# Vérifier si le fichier hostname a été créé et afficher l'URL du service caché Tor
if [[ -f /var/lib/tor/hidden_service/hostname ]]; then
    echo "🕵️ Tor hidden service URL: $(cat /var/lib/tor/hidden_service/hostname)"
else
    echo "Erreur: le fichier hostname n'a pas été créé par Tor."
fi

# Daemon off assure que NGINX reste au premier plan 
# Et continue de fonctionner
nginx -g 'daemon off;' &

# Garder le conteneur en cours d'exécution
tail -f /dev/null