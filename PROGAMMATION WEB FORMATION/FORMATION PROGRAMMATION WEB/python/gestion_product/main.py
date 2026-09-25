from product_manager import ProductManager
from utils import demander_confirmation, saisir_texte, saisir_nombre_flottant, saisir_nombre_entier

"""
Ce fichier est le point d'entrée du programme.

Le déroulement est simple :
1. on crée un objet ProductManager
2. on demande le nom du produit
3. on demande le prix
4. on demande la quantité
5. on ajoute le produit
6. on affiche le tableau à la fin
"""


def main():
    manager = ProductManager()

    while True:
        nom_produit = saisir_texte("Entrer le nom d'un produit ou saisissez '-1' pour arrêter : ")

        if nom_produit == "-1":
            if manager.is_empty():
                print("Aucun produit n'a été enregistré.")
                reponse = demander_confirmation(
                    "Voulez-vous arrêter (A/a) ou enregistrer un produit (E/e) ? "
                )
                if reponse == "a":
                    break
                continue

            print("\nVoici les produits complétés :")
            print(manager.display_table())
            print(f"Prix total général : {manager.total_general():.2f}")
            break

        prix_unitaire = saisir_nombre_flottant(
            f"Entrer le prix unitaire du produit '{nom_produit}' : "
        )
        quantite = saisir_nombre_entier(
            f"Entrer la quantité du produit '{nom_produit}' : "
        )

        manager.add_product(nom_produit, prix_unitaire, quantite)
        print(f"Le produit '{nom_produit}' a été ajouté avec succès.\n")


if __name__ == "__main__":
    main()

