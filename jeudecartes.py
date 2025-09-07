import random
from carte import Carte

class JeuDeCartes:
    def __init__(self, option="aleatoire", paquet_personnalise=None):
        self.option = option
        self.paquet_personnalise = paquet_personnalise
        self.cartes = self.creer_paquet()
    
    def creer_paquet(self):
        """Crée un paquet de cartes (52 cartes + 2 jokers), selon l'option choisie"""
        symboles = ['Trèfle', 'Carreau', 'Coeur', 'Pique']
        
        if self.option == "personnalise" and self.paquet_personnalise:
            # Si l'option est personnalisée, on construit le paquet avec les cartes données par l'utilisateur
            paquet = [Carte(numero, symbole) for numero, symbole in self.paquet_personnalise]
            
            # Si les jokers ne sont pas dans le paquet personnalisé, on les ajoute à la fin
            if not any(carte.numero == 53 for carte in paquet):  # Pas de joker noir
                paquet.append(Carte(53, 'Joker Noir'))
            if not any(carte.numero == 54 for carte in paquet):  # Pas de joker rouge
                paquet.append(Carte(54, 'Joker Rouge'))
        
        else:
            # Sinon, on crée un paquet standard avec 52 cartes et 2 jokers
            paquet = [Carte(i + 1, symbole) for symbole in symboles for i in range(13)]
            paquet.append(Carte(53, 'Joker Noir'))  # Ajouter le joker noir
            paquet.append(Carte(54, 'Joker Rouge'))  # Ajouter le joker rouge
        
        if self.option == "aleatoire":
            # Mélange le paquet si l'option est aléatoire
            random.shuffle(paquet)

        return paquet

    def valider_paquet(self):
        """Vérifie que le paquet est valide (cartes uniques, numéros et symboles valides)"""
        symboles_valides = ['Trèfle', 'Carreau', 'Coeur', 'Pique', 'Joker Noir', 'Joker Rouge']
        numeros_valides = set(range(1, 14))  # Numéros valides pour les cartes normales (1 à 13)
        if len(self.cartes) != 54:
            return False, "Le paquet doit contenir exactement 54 cartes." 
        # Vérifier que les cartes sont uniques
        cartes_uniques = set((carte.numero, carte.symbole) for carte in self.cartes)
        if len(cartes_uniques) != len(self.cartes):
            return False, "Le paquet contient des cartes en double."

        # Vérifier que les numéros et symboles sont valides
        for carte in self.cartes:
            if carte.numero == 53:  # Joker Noir
                if carte.symbole != 'Joker Noir':
                    return False, f"Le symbole de la carte {carte} est invalide pour un Joker Noir."
            elif carte.numero == 54:  # Joker Rouge
                if carte.symbole != 'Joker Rouge':
                    return False, f"Le symbole de la carte {carte} est invalide pour un Joker Rouge."
            elif carte.numero < 1 or carte.numero > 13:  # Numéros invalides (en dehors de 1 à 13)
                return False, f"Le numéro de la carte {carte} est invalide. Il doit être entre 1 et 13."
            elif carte.symbole not in ['Trèfle', 'Carreau', 'Coeur', 'Pique']:  # Vérification des symboles valides
                return False, f"Le symbole de la carte {carte} est invalide."

        return True, "Le paquet est valide."

    
    def copier_paquet(self):
        """Crée une copie du paquet de cartes actuel."""
        nouveau_paquet = [Carte(carte.numero, carte.symbole) for carte in self.cartes]
        copie = JeuDeCartes(option=self.option)
        copie.cartes = nouveau_paquet
        return copie
        
    def parser_depuis_chaine(chaine):
        """Transforme une chaîne de type '5 de Trèfle, 7 de Pique, ...' en liste de tuples (numéro, symbole)"""
        cartes_str = chaine.split(', ')
        paquet = []
        for carte_str in cartes_str:
            numero_str, symbole = carte_str.split(' de ')
            numero = int(numero_str)
            paquet.append((numero, symbole))
        return paquet
    
    def afficher(self, message=""):
        """Affiche les cartes d'un paquet"""
        if message:
            print(f"{message}:\n")

        # Formate chaque carte pour l'affichage
        cartes_str = [str(carte) for carte in self.cartes]
        
        # Affiche nombre fixe de cartes par ligne
        cartes_par_ligne = 5  

        # Trouver la longueur maximale des cartes pour aligner le texte
        max_len = max(len(carte) for carte in cartes_str)

        # Formater les cartes avec la longueur maximale
        for i in range(0, len(cartes_str), cartes_par_ligne):
            # Utilisation de .ljust(max_len) pour garantir un alignement uniforme
            print(" | ".join(carte.ljust(max_len) for carte in cartes_str[i:i+cartes_par_ligne]))

        # Afficher un message de fin ou un total de cartes
        print(f"\nTotal des cartes: {len(self.cartes)}")



    def couper_simple(self):
        """Effectue la coupe simple en fonction de la dernière carte"""
        last_card = self.cartes[-1]

        # Vérifie si la dernière carte est un joker et lui attribue la valeur 53
        if last_card.est_joker():  # Assure-toi que la méthode est_joker() existe dans ta classe Carte
            last_card_value = 53
        else:
            last_card_value = last_card.numero

        # Calcule la position de coupe en fonction de la dernière carte (joker = 53)
        cut_position = (last_card_value - 1) % 52

        # Effectue la coupe
        cut_part = self.cartes[:cut_position]
        self.cartes = self.cartes[cut_position:-1] + cut_part + [self.cartes[-1]]

        self.afficher("Après coupe simple")


    def couper_double(self):
        """Effectue la coupe double en fonction des jokers"""
        # Récupérer les indices des deux jokers
        joker_indices = sorted([i for i, carte in enumerate(self.cartes) if carte.numero in (53, 54)])
    
        # Découper le paquet en trois parties selon les indices triés
        top_part = self.cartes[:joker_indices[0]]
        middle_part = self.cartes[joker_indices[0] + 1:joker_indices[1]]
        bottom_part = self.cartes[joker_indices[1] + 1:]
    
        # Reformulation du paquet selon la coupe
        self.cartes = bottom_part + middle_part + top_part + [self.cartes[joker_indices[0]], self.cartes[joker_indices[1]]]
    
        self.afficher("Après coupe double")


    def deplacer_joker_noir(self):
        """Déplace le joker noir d'une position"""
        idx_joker_noir = next(i for i, carte in enumerate(self.cartes) if carte.numero == 53)
        if idx_joker_noir == len(self.cartes) - 1:
            self.cartes.insert(1, self.cartes.pop())
        else:
            self.cartes[idx_joker_noir], self.cartes[idx_joker_noir + 1] = self.cartes[idx_joker_noir + 1], self.cartes[idx_joker_noir]

        self.afficher("Après déplacement du joker noir")

    def deplacer_joker_rouge(self):
        """Déplace le joker rouge de deux positions"""
        idx_joker_rouge = next(i for i, carte in enumerate(self.cartes) if carte.numero == 54)
        if idx_joker_rouge == len(self.cartes) - 1:
            self.cartes.insert(2, self.cartes.pop())
        elif idx_joker_rouge == len(self.cartes) - 2:
            self.cartes.insert(1, self.cartes.pop())
        else:
            self.cartes[idx_joker_rouge], self.cartes[idx_joker_rouge + 2] = self.cartes[idx_joker_rouge + 2], self.cartes[idx_joker_rouge]

        self.afficher("Après déplacement du joker rouge")

    def generer_cle(self, longueur):
        """Génère un flux de clés de la longueur demandée"""
        flux = []
        while len(flux) < longueur:  # Générer exactement 'longueur' lettres
            self.deplacer_joker_noir()  # 1. Déplacer le joker noir
            self.deplacer_joker_rouge()  # 2. Déplacer le joker rouge
            self.couper_double()  # 3. Effectuer la coupe double
            self.couper_simple()  # 4. Effectuer la coupe simple
    
            # 5. Lire la première carte et générer la lettre
            numero_carte = self.cartes[0].numero
            if numero_carte in (53, 54):  # Si c'est un joker, on l'ignore et on recommence la boucle
                continue
    
            # Convertir le numéro en lettre (alignement avec l'alphabet)
            lettre = chr(((numero_carte - 1) % 26) + ord('A'))
            flux.append(lettre)
        
        return ''.join(flux)  # Retourner sous forme de chaîne de caractères

