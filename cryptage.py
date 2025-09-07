import string

def coder(message, jeu):
    """Code un message en utilisant un flux de clés de la même longueur, en ignorant les lettres accentuées et spéciales."""
    alphabet = string.ascii_uppercase
    nb_lettres = sum(1 for lettre in message.upper() if lettre in alphabet)
    flux_de_cle = jeu.generer_cle(nb_lettres)
    print("Flux de clé utilisé : ", flux_de_cle)

    message_code = []
    index_cle = 0

    for lettre in message:
        if lettre.upper() in alphabet:
            decalage = ord(flux_de_cle[index_cle]) - ord('A')
            coded_lettre = chr(((ord(lettre.upper()) - ord('A') + decalage) % 26) + ord('A'))
            message_code.append(coded_lettre)
            index_cle += 1
        else:
            message_code.append(lettre)

    return ''.join(message_code)

def decoder(message_code, jeu):
    """Décode un message en utilisant le flux de clés généré par le jeu de cartes"""
    nb_lettres = sum(1 for lettre in message_code if lettre.isalpha())
    flux_de_cle = jeu.generer_cle(nb_lettres)
    print("Flux de clé utilisé : ", flux_de_cle)
    
    message_decode = []
    index_cle = 0

    for lettre in message_code:
        if lettre.isalpha():
            decalage = ord(flux_de_cle[index_cle]) - ord('A')
            decoded_lettre = chr(((ord(lettre.upper()) - ord('A') - decalage) % 26) + ord('A'))  
            message_decode.append(decoded_lettre)
            index_cle += 1
        else:
            message_decode.append(lettre)

    return ''.join(message_decode)
