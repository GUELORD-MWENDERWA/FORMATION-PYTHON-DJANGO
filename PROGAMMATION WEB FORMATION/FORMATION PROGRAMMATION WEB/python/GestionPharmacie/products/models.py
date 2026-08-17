from datetime import timedelta

from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone

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
   nom = models.CharField(max_length=150)
   categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name='produits', 
                                 blank=True, null=True) 
   fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, related_name='produits',
                                   blank=True, null=True)
   prix = models.DecimalField("Prix de vente (€)", max_digits=10, decimal_places=2, 
                              validators=[MaxValueValidator(0)])
   prix_achat = models.DecimalField("Prix d'achat en (€)", max_digits=10, decimal_places=2,
                                     validators=[MaxValueValidator(0)], null=True, blank=True)
   stock =models.PositiveIntegerField("Quantinte en stock", default=0)
   seuil_alerte = models.PositiveIntegerField("Seuil alerte", default=0)
   lot = models.CharField("Numerro de lot", max_length=50, blank=True)
   date_peremption = models.DateField(null=True, blank=True)
   actif = models.BooleanField(default=True)
   image = models.ImageField(upload_to='produits/', blank=True, null=True)
   description = models.TextField(blank=True)

   class Meta:
      ordering = ['nom']

   def __str__(self):
      return self.nom   
   @property
   def en_rupture(self):
      return self.stock == 0

   @property
   def stock_faible(self):
       return  0 < self.stock <= self.seuil_alerte

   @property
   def peremption_proche(self):
      if not self.date_peremption:
         return False
      return self.date_peremption <= timezone.localdate() + timedelta(days=30)


class Vente(models.Model):
   class ModePaiement(models.TextChoices):
      ESPECES = 'especes','Especes'
      CARTE ='carte','Carte bancaire'
      MOBILE_MONEY = 'mobile_money', 'Mobile money'

   class Statut(models.TextChoices):
      PAYEE = 'payee', 'Payee'
      EN_ENTENTE = 'en_entente', 'En antente'
      IMPAYEE = 'impayee', 'Impayee'
      ANNULERR = 'annulee', 'Annulee'
   client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='ventes',
                              null=True, blank=True, help_text='vide = client de passage')
   date = models.DateTimeField(auto_now_add=True)
   mode_paiement = models.CharField(max_length=20, choices=ModePaiement.choices,
                                     default=ModePaiement.ESPECES)
   statut = models.CharField(max_length=20, choices=Statut.choices, 
                             default=Statut.IMPAYEE)
   remise = models.DecimalField("Remise en (€)", max_digits=10, 
                                decimal_places=2, default=0)

   class Meta:
      ordering = ['-date']

   def __str__(self):
      pass 