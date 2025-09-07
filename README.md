# Solitaire Cipher – Chiffrement et déchiffrement

## Description
Ce projet est une application Python permettant de **coder et décoder des messages** à l’aide de la **méthode de chiffrement Solitaire** inventée par Bruce Schneier.  

L’application dispose d’une interface graphique en PyQt6, et permet de :

- saisir un message directement ou de sélectionner un fichier .txt à chiffrer ;

- déchiffrer un fichier .crypt avec le paquet associé (.paquet) ;

- choisir le type de paquet de cartes : classique, aléatoire ou personnalisé.


## Fonctionnalités principales

- Chiffrement et déchiffrement de texte ou fichiers .txt / .crypt.

- Gestion des paquets de cartes : classique, aléatoire ou personnalisé.

- Interface graphique PyQt6 avec boutons intuitifs et zones de texte pour coder/décoder.

- Copie et exportation du paquet pour réutilisation future.

- Gestion des fichiers .txt et .crypt pour sauvegarder les messages.
---

## Technologies utilisées
- **Python 3**  
- **PyQt6** pour l’interface graphique  
- **Classes personnalisées** ; JeuDeCartes, Carte 
- Gestion des fichiers texte (.txt, .crypt) 

---

## Structure du projet


SolitaireCipher/
│── application.py

│── carte.py

│── cryptage.py

│── jeudecartes.py

│── style.qss

│── oui.txt #exemple de message prêt à être encodé

│── README.md # Documentation

## Installation et utilisation
### 1 - Cloner le dépôt :
git clone https://github.com/TonPseudo/SolitaireCipher.git
cd SolitaireCipher

### 2 - Installer les dépendances :
pip install PyQt6 pyperclip

### 3 - Lancer l’application :
python application.py

### Utilisation :

- Choisir un message ou un fichier à chiffrer/déchiffrer.

- Sélectionner le type de paquet : classique, aléatoire ou personnalisé.

- Copier ou sauvegarder le message/chiffrement.

- Pour déchiffrer un fichier .crypt, sélectionner également le fichier .paquet associé.
