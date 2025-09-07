# Solitaire Cipher – Chiffrement et déchiffrement

## Description
Ce projet est une application Python permettant de **coder et décoder des messages** à l’aide de la **méthode de chiffrement Solitaire** inventée par Bruce Schneier.  

L’application dispose d’une interface graphique simple et intuitive, et prend en charge plusieurs modes d’entrée :  

- **Message direct** : saisie du texte à chiffrer ou déchiffrer.  
- **Fichier texte (.txt)** : lecture et écriture de fichiers pour le chiffrement ou le déchiffrement.  

Le projet permet également de gérer le **paquet de cartes** utilisé pour générer le flux de clés :  

- **Paquet aléatoire** : généré à chaque chiffrement ou sur demande.  
- **Paquet existant / personnalisé** : pour déchiffrer un message avec le même paquet utilisé pour le chiffrement.  

---

## Fonctionnalités principales
- Chiffrement et déchiffrement de texte ou de fichiers `.txt`.  
- Sélection du type de paquet : aléatoire ou existant.  
- Interface graphique en **Tkinter**.  
- Gestion des messages longs et de fichiers multiples.  
- Possibilité de garder le même paquet pour coder et décoder plusieurs messages.  

---

## Technologies utilisées
- **Python 3**  
- **Tkinter** pour l’interface graphique  
- **Classes personnalisées** (`JeuDeCartes`, `Carte`) pour la gestion du paquet et la génération des clés  
- Gestion des fichiers texte pour lecture et écriture  

---

## Structure du projet


SolitaireCipher/
│── gui.py # Interface graphique principale
│── solitaire.py # Logique du chiffrement/déchiffrement
│── cartes.py # Classe JeuDeCartes et Carte
│── exemples/ # Exemples de fichiers texte
│── README.md # Documentation
│── requirements.txt # Dépendances