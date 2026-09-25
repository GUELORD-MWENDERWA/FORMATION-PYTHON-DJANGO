from django.test import TestCase
# Create your tests here.
class User():
   def __init__(self, nom, email):
      self.nom = nom
      self.email = email

   def get_nom(self):
      return self.nom   

   def get_email(self):
      return self.email

   def update_email(self, new_email):
      self.email = new_email


personne = User("Guelord", "xK5d9@example.com")   
personne2 = User("Mwendwa", "j7NtW@example.com")


print(personne.get_nom())
print(personne.get_email())
personne.update_email("newemail@example.com")
print(personne.get_email())

personne2.update_email("newemail2@example.com")
print(personne2.get_email())


class Produit():
   def __init__(self, nom, description, prix, quantite):
      self.nom = nom
      self.description = description
      self.prix = prix
      self.quantite = quantite

   def get_nom(self):
      return self.nom   

   def get_description(self):
      return self.description

   def get_prix(self):
      return self.prix

   def get_quantite(self):
      return self.quantite

   def update_quantite(self, new_quantite):
      self.quantite = new_quantite

   def total_value(self):
      return self.prix * self.quantite   

