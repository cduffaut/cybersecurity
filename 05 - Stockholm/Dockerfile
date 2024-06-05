FROM ubuntu:focal

# Définir l'option non interactive pour apt-get dans les commandes RUN
RUN apt update && apt upgrade -y && \
	DEBIAN_FRONTEND=noninteractive apt -y install python3.9 python3-pip libssl-dev

RUN pip3 install cryptography 

# Installer les bibliothèques Python nécessaires
RUN python3.9 -m pip install spacy

# Télécharger les modèles Spacy
RUN python3.9 -m spacy download en_core_web_sm

# Vérifier les installations
RUN python3.9 -m pip list

# Créer un répertoire de travail
WORKDIR /stockholm

# Copier les fichiers du projet dans le conteneur
COPY . /stockholm

# Copier le dossier infection dans le répertoire de travail (ce qui est /root)
COPY infection /root/infection

CMD ["/bin/bash"]