# Définit l’environnement de base sur lequel le conteneur sera construit
# Debian:bullseye-slim est une image minimaliste de Debian
# Elle contient les outils et les bibliothèques nécessaires pour installer d’autres logiciels comme NGINX, SSH et Tor
FROM debian:bullseye-slim

# Met à jour la liste des paquets disponibles
# Et installe les paquets nécessaires : NGINX, SSH et Tor
# RUN execute les commandes d’installation dans le conteneur
RUN apt-get update && \
    apt-get install nginx openssh-server tor -y

# Copie les fichiers de configuration personnalisés dans le conteneur 
# Et s’assure qu’ils sont correctement configurés pour le service caché Tor et l’accès SSH.
COPY nginx.conf /etc/nginx/nginx.conf
COPY sshd_config /etc/ssh/sshd_config
COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css
COPY torrc /etc/tor/torrc

# Créer le répertoire .ssh et configurer les permissions
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh

# Copie la clé publique dans le conteneur
COPY id_rsa.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

# Expose les ports nécessaires pour HTTP et SSH
EXPOSE 80 4242

# Copie et rend exécutable le script de démarrage personnalisé
COPY start_services.sh /start_services.sh
RUN chmod +x /start_services.sh

# Lance le script de démarrage personnalisé
CMD ["/start_services.sh"]