# Utiliser une image de base Ubuntu pour l'architecture amd64
FROM --platform=linux/amd64 ubuntu:22.04

# Installer les dépendances nécessaires pour exécuter des binaires 32 bits
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
        libc6:i386 \
        libncurses5:i386 \
        libstdc++6:i386 \
        gdb \
        strace \
        binutils \
        elfutils \
		git \
        build-essential \
        cmake \
        python3

RUN git clone https://github.com/radareorg/radare2.git && \
    cd radare2 && \
    ./sys/install.sh


# Copier le fichier binaire dans l'image Docker
COPY level1 /level1

# Donner les permissions d'exécution au fichier binaire
RUN chmod +x /level1

# Définir le point d'entrée
CMD ["/bin/bash"]
