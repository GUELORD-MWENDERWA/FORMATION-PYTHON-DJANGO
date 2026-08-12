# 03 — CRUD Produits (formulaires + vues)

Fichiers concernes : [`products/forms.py`](../products/forms.py),
[`products/views.py`](../products/views.py),
[`products/urls.py`](../products/urls.py),
[`produits/liste.html`](../products/templates/produits/liste.html),
[`produits/form.html`](../products/templates/produits/form.html),
[`partials/products_table.html`](../products/templates/partials/products_table.html)

## Objectif du module

C'est le module le plus important du cours : il pose le **patron
CRUD** (Create/Read/Update/Delete) qu'on repete ensuite a l'identique
pour Clients (module 05) et Fournisseurs (module 05). Une fois
compris ici, les deux suivants seront rapides.

## Etape 1 — Le formulaire (`forms.py`)

```python
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            'nom', 'categorie', 'fournisseur', 'prix', 'prix_achat',
            'stock', 'seuil_alerte', 'lot', 'date_peremption', 'actif',
            'image', 'description',
        ]
        widgets = {
            'date_peremption': forms.DateInput(attrs={'type': 'date'}),
        }
```

Un `ModelForm` genere automatiquement un champ de formulaire pour
chaque champ de modele liste dans `fields`, avec la bonne validation
(un `DecimalField` du modele refuse une lettre, un champ `blank=False`
devient `required=True`, etc.). C'est nettement moins de code que
d'ecrire chaque `<input>` et sa validation a la main — et c'est
exactement ce qu'on avait deja en HTML statique dans
`produits/form.html`, il ne restait qu'a le brancher.

## Etape 2 — La vue (`views.py`)

Une seule fonction gere **a la fois** la creation et la modification :

```python
def produits_form(request, pk=None):
    produit = get_object_or_404(Produit, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit enregistre.")
            return redirect('produits_liste')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produits/form.html', {'form': form, 'produit': produit})
```

Le principe a bien comprendre : `instance=produit`. Si `produit` est
`None` (creation), le formulaire cree un nouvel enregistrement. S'il
pointe vers un produit existant (modification, `pk` fourni dans
l'URL), le meme `ModelForm` pre-remplit ses champs avec les valeurs
actuelles et modifie cet enregistrement au lieu d'en creer un nouveau.
C'est pour ca que le HTML d'origine disait deja *"Sert aussi bien pour
la creation que pour l'edition"* : ce module rend cette phrase vraie.

Notez aussi `request.FILES` : necessaire des qu'un formulaire contient
un champ fichier (`image`), en plus de `request.POST` et de
`enctype="multipart/form-data"` sur la balise `<form>`.

La suppression est une vue a part, volontairement minimale :

```python
@require_POST
def produits_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    produit.delete()
    messages.success(request, "Produit supprime.")
    return redirect('produits_liste')
```

`@require_POST` refuse toute requete GET sur cette URL : on ne
supprime jamais une ressource via un simple lien cliquable (un
crawler ou un pre-chargement de page pourrait le declencher par
accident), seulement via un `<form method="post">`.

## Etape 3 — Les URLs

```python
path('produits/ajouter/', views.produits_form, name='produits_form'),
path('produits/<int:pk>/modifier/', views.produits_form, name='produits_edit'),
path('produits/<int:pk>/supprimer/', views.produits_delete, name='produits_delete'),
```

Deux URLs differentes (`produits_form` et `produits_edit`) pointent
vers **la meme vue** : c'est le parametre `pk` dans l'URL qui fait la
difference (present ou absent).

## Etape 4 — La liste et la boucle `{% for %}`

`produits/liste.html` n'a pas change : il inclut deja
`partials/products_table.html`. C'est ce partial qui passe de lignes
HTML codees en dur a une boucle sur les vraies donnees :

```django
{% for produit in produits %}
  <div class="products-row">
    ...
    <span>{{ produit.nom }}</span>
    ...
    <span class="cell-label">Categorie:</span>{{ produit.categorie.nom|default:"—" }}
    ...
  {% empty %}
  <p>Aucun produit pour le moment.</p>
{% endfor %}
```

Le tag `{% empty %}` affiche un message de repli si le queryset est
vide — pratique la toute premiere fois qu'on teste la page avant
d'avoir charge la fixture de demonstration.

La vue fournit `produits` avec une petite optimisation a expliquer :

```python
produits = Produit.objects.select_related('categorie').annotate(
    total_ventes=Sum('lignes_vente__quantite')
)
```

- `select_related('categorie')` : va chercher la categorie de chaque
  produit **dans la meme requete SQL** (une jointure), au lieu d'une
  requete separee a chaque fois que le template lit
  `produit.categorie.nom` dans la boucle. Sans ca, afficher 100
  produits ferait 101 requetes SQL au lieu d'une seule.
- `.annotate(total_ventes=Sum(...))` : calcule, cote base de donnees,
  le nombre total d'unites vendues de chaque produit (colonne
  "Ventes" du tableau), en agregeant toutes les `LigneVente` liees.

## Etape 5 — Modifier / supprimer depuis le tableau

Chaque ligne du tableau recoit un lien "modifier" et un petit
formulaire de suppression avec confirmation JavaScript :

```django
<form method="post" action="{% url 'produits_delete' produit.pk %}"
      onsubmit="return confirm('Supprimer {{ produit.nom|escapejs }} ?');">
  {% csrf_token %}
  <button type="submit" class="danger">...</button>
</form>
```

`{% csrf_token %}` est obligatoire dans tout `<form method="post">`
Django : sans lui, la requete est rejetee (protection contre les
attaques CSRF). `|escapejs` echappe le nom du produit pour qu'il
puisse s'inserer sans risque dans l'attribut JavaScript `onsubmit`.

## Testez

1. `/produits/` doit afficher les 6 produits de la fixture, avec
   leurs vraies categories, stocks et une pastille rouge/orange sur
   les produits en rupture ou stock faible.
2. Cliquez "Ajouter un produit", remplissez le formulaire, validez :
   vous devez etre redirige vers la liste avec un message vert de
   confirmation, et le nouveau produit doit apparaitre.
3. Cliquez l'icone crayon sur une ligne : le formulaire doit
   s'ouvrir pre-rempli avec les valeurs actuelles.
4. Cliquez l'icone poubelle : une confirmation doit apparaitre avant
   suppression.
5. Essayez de soumettre le formulaire sans nom : l'erreur doit
   s'afficher sous le champ concerne, sans perdre les autres valeurs
   deja saisies.

Passez au [module 04](04-stock.md).
