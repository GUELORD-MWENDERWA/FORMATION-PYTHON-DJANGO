"""
Ce fichier contient des fonctions simples pour la saisie.

Pour créer une fonction, on utilise def.

Exemple :

def saisir_texte(message):
    return input(message)

message est le paramètre.
"""


def saisir_texte(message):
    while True:
        valeur = input(message).strip()
        if valeur != "":
            return valeur
        print("La valeur ne doit pas être vide.")


def saisir_nombre_flottant(message):
    while True:
        try:
            valeur = float(input(message).strip())
            if valeur < 0:
                print("Le prix ne peut pas être négatif.")
                continue
            return valeur
        except ValueError:
            print("Veuillez entrer un nombre valide.")


def saisir_nombre_entier(message):
    while True:
        try:
            valeur = int(input(message).strip())
            if valeur < 0:
                print("La quantité ne peut pas être négative.")
                continue
            return valeur
        except ValueError:
            print("Veuillez entrer un entier valide.")


def demander_confirmation(message):
    while True:
        reponse = input(message).strip().lower()
        if reponse == "a" or reponse == "e":
            return reponse
        print("Réponse invalide. Tapez 'A/a' pour arrêter ou 'E/e' pour enregistrer.")


"""
def saisir_name(message):
    
    while True: 
        
        print(message)
        product = input().strip()
        if product == "":
            print("le nom ne doit pas etre vide")
        else:
            return product


name_produit = saisir_name("entrer le nom d'un produit")
name_user  = saisir_name("entrer le nom de l(utilisateur)")

print(f"l'utilisateur {name_user} a enregister le produit {name_produit }")
"""

