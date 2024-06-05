Lancer le makefile: make run

Lancer le programme:
python3.9 stockholm.py -h or -help
python3.9 stockholm.py -v or -version
python3.9 stockholm.py -r or -reverse <key> (you can find the key in the key_file)
python3.9 stockholm.py -s or -silent

Verifier les changements:
cd ~/infection

######

Ransomware:
Par définition, un ransomware est un type de logiciel malveillant que les cybercriminels utilisent 
pour gagner de l’argent. 
Ils s’en servent pour bloquer l’accès à des données ou à des systèmes jusqu’à ce que leur propriétaire 
paie la somme demandée.

liste des fichiers touchés par Wannacry:

source: https://gist.github.com/xpn/facb5692980c14df272b16a4ee6a29d5
source: https://www.bleepingcomputer.com/news/security/wannacry-wana-decryptor-wanacrypt0r-info-and-technical-nose-dive/

ℹ️ The key with which the files are encrypted will be at least 16 characters long.
Fernet génère automatiquement des clés de 32 octets, ce qui produit des chaînes de 44 caractères.
Cela respecte toujours la consigne d'avoir au moins 16 caractères.

🧪 Algorithme choisit:
he fernet module of the cryptography package has inbuilt functions for the generation of the key, encryption of plaintext into ciphertext,
and decryption of ciphertext into plaintext using the encrypt and decrypt methods respectively.
The fernet module guarantees that data encrypted using it cannot be further manipulated or read without the key. 