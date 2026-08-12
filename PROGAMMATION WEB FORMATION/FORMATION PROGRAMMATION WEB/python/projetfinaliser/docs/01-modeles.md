# 01 — Modeles et migrations

Fichier concerne : [`products/models.py`](../products/models.py)

## Objectif du module

Avant ce module, `products/models.py` etait vide (`# Create your
models here.`). On y definit les 6 modeles qui representent les
donnees manipulees par l'application, en s'appuyant sur les champs
deja presents dans les formulaires HTML statiques (`produits/form.html`,
`clients/form.html`, etc.) : le HTML nous dit deja quels champs
existent, il ne reste qu'a les traduire en `models.Field`.

## Les 6 modeles et pourquoi ils existent

| Modele | Represente | Lien avec le frontend existant |
|---|---|---|
| `Categorie` | Une categorie de produit (Medicaments, Hygiene...) | Le `<select name="categorie">` de `produits/form.html` |
| `Fournisseur` | Un grossiste / fournisseur | `fournisseurs/liste.html` + `fournisseurs/form.html` |
| `Produit` | Un article vendu en pharmacie | `produits/liste.html`, `stock/liste.html` |
| `Client` | Un client de la pharmacie | `clients/liste.html` + `clients/form.html` |
| `Vente` | Une transaction de vente (le "panier" encaisse) | `ventes/form.html` (point de vente) |
| `LigneVente` | Une ligne produit dans une vente (quantite, prix) | Les lignes du panier / de la facture |

## Points a expliquer en classe

### 1. Les `ForeignKey` et leur `on_delete`

```python
categorie = models.ForeignKey(
    Categorie, on_delete=models.PROTECT, related_name='produits',
    null=True, blank=True,
)
fournisseur = models.ForeignKey(
    Fournisseur, on_delete=models.SET_NULL, related_name='produits',
    null=True, blank=True,
)
```

- `on_delete=models.PROTECT` sur `categorie` : on refuse de supprimer
  une categorie tant que des produits l'utilisent (empeche une erreur
  de manipulation cote admin).
- `on_delete=models.SET_NULL` sur `fournisseur` : si un fournisseur
  disparait, on garde le produit mais on vide juste le lien (moins
  strict, car un produit peut exister sans fournisseur connu).
- `related_name='produits'` permet d'ecrire `categorie.produits.all()`
  depuis l'autre bout de la relation — utile plus tard pour compter
  les ventes par produit (module 06).

### 2. Les `@property` : des champs "calcules"

```python
@property
def en_rupture(self):
    return self.stock == 0

@property
def stock_faible(self):
    return 0 < self.stock <= self.seuil_alerte
```

Une `@property` se comporte comme un champ (`produit.en_rupture`,
sans parentheses) mais est calculee a la volee au lieu d'etre stockee
en base. C'est le bon outil des qu'une valeur peut se deduire d'autres
champs : pas besoin de la recalculer et la sauvegarder a chaque
vente, elle est toujours a jour. On les retrouve massivement dans
`Vente` (`sous_total`, `total`, `nb_articles`, `numero_facture`) —
voir le module 06.

### 3. `TextChoices` pour les listes deroulantes

```python
class Statut(models.TextChoices):
    PAYEE = 'payee', 'Payee'
    EN_ATTENTE = 'en_attente', 'En attente'
    IMPAYEE = 'impayee', 'Impayee'
    ANNULEE = 'annulee', 'Annulee'

statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.PAYEE)
```

`TextChoices` remplace les `<option>` codes en dur dans le HTML
d'origine (`ventes/form.html` avait un `<select>` avec des options
statiques). Cote Django, ca donne gratuitement :
- une validation ("statut" ne peut pas contenir n'importe quelle
  chaine),
- un widget `<select>` genere automatiquement dans les formulaires,
- une methode `vente.get_statut_display()` qui renvoie le libelle
  humain ("En attente") a partir de la valeur stockee ("en_attente").

### 4. Pourquoi `LigneVente` est un modele a part

Une vente contient plusieurs produits, chacun avec sa propre quantite
et son propre prix (le prix au moment de la vente, pas le prix actuel
du produit — un produit peut changer de prix apres coup, la facture
doit rester figee). C'est une relation many-to-many **avec des
donnees supplementaires** (quantite, prix_unitaire), donc on ne peut
pas utiliser un simple `ManyToManyField` : il faut un modele
intermediaire explicite, `LigneVente`, relie a `Vente` par
`related_name='lignes'` (d'ou `vente.lignes.all()` partout dans le
code).

## Commandes a executer

```bash
python manage.py makemigrations products
python manage.py migrate
```

`makemigrations` lit `models.py` et genere un fichier Python dans
`products/migrations/` qui decrit les changements de schema SQL a
appliquer. `migrate` execute reellement ces changements sur
`db.sqlite3`. Cette separation en deux etapes permet de relire (et
committer dans git) le plan de migration avant de l'appliquer.

## Testez

```bash
python manage.py shell
```
```python
from products.models import Categorie, Produit
c = Categorie.objects.create(nom="Medicaments")
p = Produit.objects.create(nom="Test", categorie=c, prix=5, stock=10, seuil_alerte=3)
p.en_rupture      # False
p.stock_faible    # False
print(p)          # Test (via __str__)
```

Si ces quatre lignes s'executent sans erreur, les modeles et les
migrations sont corrects. Passez au [module 02](02-admin-et-donnees-demo.md).
