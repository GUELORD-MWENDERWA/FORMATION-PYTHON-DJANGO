from datetime import timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Fournisseur(models.Model):
    nom = models.CharField("Nom de l'entreprise", max_length=150)
    contact = models.CharField("Personne de contact", max_length=150, blank=True)
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
    telephone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    notes = models.TextField(
        blank=True,
        help_text="Allergies, traitements en cours...",
    )

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        nom_complet = f"{self.prenom} {self.nom}".strip()
        return nom_complet or f"Client #{self.pk}"


class Produit(models.Model):
    nom = models.CharField(max_length=150)
    categorie = models.ForeignKey(
        Categorie, on_delete=models.PROTECT, related_name='produits',
        null=True, blank=True,
    )
    fournisseur = models.ForeignKey(
        Fournisseur, on_delete=models.SET_NULL, related_name='produits',
        null=True, blank=True,
    )
    prix = models.DecimalField(
        "Prix de vente (€)", max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    prix_achat = models.DecimalField(
        "Prix d'achat (€)", max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)], null=True, blank=True,
    )
    stock = models.PositiveIntegerField("Quantite en stock", default=0)
    seuil_alerte = models.PositiveIntegerField("Seuil d'alerte", default=0)
    lot = models.CharField("Numero de lot", max_length=50, blank=True)
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
        return 0 < self.stock <= self.seuil_alerte

    @property
    def peremption_proche(self):
        if not self.date_peremption:
            return False
        return self.date_peremption <= timezone.localdate() + timedelta(days=30)


class Vente(models.Model):
    class ModePaiement(models.TextChoices):
        ESPECES = 'especes', 'Especes'
        CARTE = 'carte', 'Carte bancaire'
        MOBILE_MONEY = 'mobile_money', 'Mobile money'

    class Statut(models.TextChoices):
        PAYEE = 'payee', 'Payee'
        EN_ATTENTE = 'en_attente', 'En attente'
        IMPAYEE = 'impayee', 'Impayee'
        ANNULEE = 'annulee', 'Annulee'

    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, related_name='ventes',
        null=True, blank=True, help_text="Vide = client de passage",
    )
    date = models.DateTimeField(auto_now_add=True)
    mode_paiement = models.CharField(
        max_length=20, choices=ModePaiement.choices, default=ModePaiement.ESPECES,
    )
    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.PAYEE,
    )
    remise = models.DecimalField(
        "Remise (€)", max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.numero

    @property
    def numero(self):
        return f"#{self.pk}"

    @property
    def numero_facture(self):
        annee = self.date.year if self.date else "----"
        return f"F-{annee}-{self.pk}"

    @property
    def statut_css(self):
        return {
            self.Statut.PAYEE: 'active',
            self.Statut.EN_ATTENTE: 'warning',
            self.Statut.IMPAYEE: 'warning',
            self.Statut.ANNULEE: 'danger',
        }.get(self.statut, 'active')

    @property
    def sous_total(self):
        return sum((ligne.total for ligne in self.lignes.all()), start=0)

    @property
    def total(self):
        return self.sous_total - self.remise

    @property
    def nb_articles(self):
        return sum(ligne.quantite for ligne in self.lignes.all())


class LigneVente(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT, related_name='lignes_vente')
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(
        "Prix unitaire au moment de la vente (€)", max_digits=10, decimal_places=2,
    )

    def __str__(self):
        return f"{self.quantite} x {self.produit}"

    @property
    def total(self):
        return self.quantite * self.prix_unitaire
