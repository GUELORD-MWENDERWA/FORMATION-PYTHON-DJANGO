from django.db import models

# Create your models here.
class Categorie(models.Model):
   nom = models.CharField(max_length=100, unique=True)

   class Meta:
      verbose_name = "categorie"
      verbose_name_plural = "categories"
      ordering = ['nom']

   def __str__(self):
      return self.nom   


class Fournisseur(models.Model):
   nom = models.CharField("Nom de l'entreprise", max_length=150)
   contact = models.CharField("Personne de contact",max_length=150,blank=True)
   telephone = models.CharField(max_length=30, blank=True)
   email = models.EmailField(blank=True)
   adresse = models.CharField(max_length=255, blank=True)
   notes = models.TextField(blank=True)
   actif = models.BooleanField(default=True)

   class Meta:
      ordering = ['nom']

   def __str__(self):
      return self.nom   


class Client(models.Model):
   nom = models.CharField(max_length=100)
   prenom = models.CharField(max_length=100, blank=True)
   telephone = models.CharField(max_length=30,blank=True)
   email = models.EmailField(blank=True)
   date_naissance =models.DateField(null=True, blank=True)
   adresse = models.CharField(max_length=255,blank=True)
   note = models.TextField(blank=True,help_text="Allergies, traitements en cours...")

   class Meta:
      ordering = ['nom','prenom']

   def __str__(self):
      nom_complet = f"{self.nom} {self.prenom}".strip()
      return nom_complet or f"Client #{self.pk}"


class Produit(models.Model):
   pass   