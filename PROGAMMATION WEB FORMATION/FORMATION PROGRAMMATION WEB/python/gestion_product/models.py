"""
Ce fichier montre la base de la POO pour débutants.

Une classe est un plan.
Un objet est une "copie" créée à partir de ce plan.

Exemple simple :

class Product:
    def __init__(self, name, unit_price, quantity):
        self.name = name

Ici, self représente l'objet en cours.
"""


class Product:
    def __init__(self, name, unit_price, quantity):
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity

    def prix_total(self):
        return self.unit_price * self.quantity

    def ligne_tableau(self, numero):
        return (
            f"* {numero:<5} * {self.name:<15} * {self.unit_price:<15.2f} * "
            f"{self.quantity:<10} * {self.prix_total():<10.2f} *"
        )

