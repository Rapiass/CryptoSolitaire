class Carte:
    def __init__(self, numero, symbole):
        self.numero = numero
        self.symbole = symbole

    def __repr__(self):
        return f"{self.numero} de {self.symbole}"

    def est_joker(self):
        return self.numero == 53 or self.numero == 54