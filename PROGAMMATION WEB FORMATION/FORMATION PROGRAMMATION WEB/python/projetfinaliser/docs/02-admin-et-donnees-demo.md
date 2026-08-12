# 02 — Admin et donnees de demonstration

Fichiers concernes : [`products/admin.py`](../products/admin.py),
[`products/fixtures/demo.json`](../products/fixtures/demo.json)

## Objectif du module

Avant d'ecrire le moindre formulaire HTML, on veut pouvoir verifier
que les modeles du module 01 fonctionnent, et avoir des donnees a
afficher pendant qu'on construit les pages. Django fournit un
back-office d'administration gratuit ; on l'active en quelques lignes.

## Enregistrer les modeles dans l'admin

```python
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'fournisseur', 'prix', 'stock', 'seuil_alerte', 'actif']
    list_filter = ['actif', 'categorie', 'fournisseur']
    search_fields = ['nom', 'lot']
```

- `list_display` : les colonnes affichees dans la liste de l'admin.
- `list_filter` : ajoute des filtres a droite (tres utile pour
  verifier rapidement "quels produits sont en rupture ?" une fois
  `stock` visible).
- `search_fields` : active la barre de recherche en haut de la liste.

Pour les ventes, on va plus loin avec un **inline** :

```python
class LigneVenteInline(admin.TabularInline):
    model = LigneVente
    extra = 0

@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client', 'date', 'statut', 'mode_paiement', 'total']
    inlines = [LigneVenteInline]
```

Un `TabularInline` permet de modifier les lignes d'une vente
directement sur la page de la vente, sans changer de page — pratique
pour corriger une vente de test sans repasser par le formulaire du
site.

## Creer un compte administrateur

```bash
python manage.py createsuperuser
```

Puis ouvrez `http://127.0.0.1:8000/admin/` et connectez-vous. C'est le
moyen le plus rapide de verifier que les modeles se comportent
correctement avant meme d'avoir ecrit une seule vue.

## Les donnees de demonstration (fixtures)

Plutot que de re-saisir des produits/clients a la main a chaque fois
que la base est remise a zero (tres frequent en cours), on fige un
jeu de donnees dans `products/fixtures/demo.json` : categories,
fournisseurs, produits (avec un produit en rupture, un stock faible,
une peremption proche — pour tester les trois etats visuellement des
le module 04), clients, et quelques ventes deja passees.

```bash
python manage.py loaddata demo
```

Le format d'une fixture Django est une liste d'objets
`{"model": "app.modele", "pk": ..., "fields": {...}}`. Point notable
pour les eleves curieux : les cles etrangeres se referencent
simplement par leur `pk` (ex. `"categorie": 1`), et l'ordre des objets
dans le fichier doit respecter les dependances (les `Categorie`
avant les `Produit` qui les referencent, les `Produit` et `Client`
avant les `Vente`, etc.).

## Testez

```bash
python manage.py migrate
python manage.py loaddata demo
python manage.py createsuperuser
python manage.py runserver
```

Ouvrez `/admin/` : vous devez voir 4 categories, 3 fournisseurs, 6
produits, 4 clients et 5 ventes (chacune avec ses lignes visibles en
inline en cliquant dessus). Passez au [module 03](03-produits-crud.md).
