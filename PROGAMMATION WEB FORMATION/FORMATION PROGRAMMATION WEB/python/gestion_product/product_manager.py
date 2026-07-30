from pathlib import Path
from models import Product

"""
Ce fichier gère la liste des produits.

On peut expliquer :
- def sert à créer une fonction
- self représente l'objet actuel
- __init__ initialise les valeurs de l'objet
- open() permet de lire et d'écrire dans un fichier texte
"""


class ProductManager:
    def __init__(self, file_name="products.txt"):
        self.file_path = Path(__file__).with_name(file_name)
        self.products = self.load_products()

    def load_products(self):
        produits = []

        if not self.file_path.exists():
            return produits

        with self.file_path.open("r", encoding="utf-8") as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                if ligne == "":
                    continue

                nom, prix, quantite = ligne.split("|")
                produit = Product(nom, float(prix), int(quantite))
                produits.append(produit)

        return produits

    def save_products(self):
        with self.file_path.open("w", encoding="utf-8") as fichier:
            for produit in self.products:
                fichier.write(f"{produit.name}|{produit.unit_price}|{produit.quantity}\n")

    def add_product(self, name, unit_price, quantity):
        produit = Product(name, unit_price, quantity)
        self.products.append(produit)
        self.save_products()
        return produit

    def is_empty(self):
        return len(self.products) == 0

    def total_general(self):
        total = 0
        for produit in self.products:
            total = total + produit.prix_total()
        return total

    def display_table(self):
        largeur = 71
        texte = ["*" * largeur]
        texte.append(
            f"* {'N°':<5} * {'Produit':<15} * {'Prix Unitaire':<15} * {'Quantité':<10} * {'Prix Total':<10} *"
        )
        texte.append("*" * largeur)

        for i, produit in enumerate(self.products, start=1):
            texte.append(produit.ligne_tableau(i))

        texte.append("*" * largeur)
        return "\n".join(texte)
