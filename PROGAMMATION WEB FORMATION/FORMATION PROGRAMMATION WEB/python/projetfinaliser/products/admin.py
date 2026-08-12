from django.contrib import admin

from .models import Categorie, Client, Fournisseur, LigneVente, Produit, Vente


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'contact', 'telephone', 'email', 'actif']
    list_filter = ['actif']
    search_fields = ['nom', 'contact', 'email']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'telephone', 'email']
    search_fields = ['nom', 'prenom', 'email', 'telephone']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'fournisseur', 'prix', 'stock', 'seuil_alerte', 'actif']
    list_filter = ['actif', 'categorie', 'fournisseur']
    search_fields = ['nom', 'lot']


class LigneVenteInline(admin.TabularInline):
    model = LigneVente
    extra = 0


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client', 'date', 'statut', 'mode_paiement', 'total']
    list_filter = ['statut', 'mode_paiement']
    inlines = [LigneVenteInline]
