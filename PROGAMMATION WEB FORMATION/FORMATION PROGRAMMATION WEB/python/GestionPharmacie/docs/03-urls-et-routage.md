# 03 — Les URLs : comment une adresse devient une page

## Le principe

Quand le navigateur demande `http://127.0.0.1:8000/produits/`, Django
doit decider quelle fonction Python va traiter cette requete. C'est le
role du **routage** : une correspondance entre une adresse et une
fonction. Cette correspondance est ecrite dans des fichiers `urls.py`,
sous forme d'une liste `urlpatterns`.

## Deux niveaux, un seul projet

```
Requete "/produits/"
        |
        v
GestionPharmacie/urls.py   (racine, ROOT_URLCONF dans settings.py)
        |  path('', include('products.urls'))
        v
products/urls.py           (routes de l'application)
        |  path('produits/', views.produits_liste, name='produits_liste')
        v
products/views.py : produits_liste(request)
```

### `GestionPharmacie/urls.py` (racine)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
]
```

Seulement deux lignes utiles : `/admin/...` va vers l'interface
d'administration fournie par Django, et **tout le reste** (`''`) est
delegue au fichier de l'application via `include('products.urls')`.
C'est ce mecanisme d'`include()` qui permet de garder les URLs de
chaque application dans son propre dossier, plutot que de tout
entasser dans un seul fichier geant des que le projet grandit.

### `products/urls.py` (application)

Chaque page du site y a sa ligne, par exemple :

```python
path('produits/', views.produits_liste, name='produits_liste'),
path('produits/ajouter/', views.produits_form, name='produits_form'),
...
path('factures/<int:pk>/', views.factures_detail, name='factures_detail'),
```

Trois elements a chaque fois :

1. **Le motif d'URL** (`'produits/'`) : le chemin apres le nom de
   domaine.
2. **La vue** (`views.produits_liste`) : la fonction Python appelee
   quand ce motif correspond (voir [04](04-vues.md)).
3. **Le nom** (`name='produits_liste'`) : un identifiant utilise pour
   generer le lien ailleurs dans le code, SANS jamais recopier l'URL
   en dur.

## `<int:pk>` : capturer une partie de l'URL

```python
path('factures/<int:pk>/', views.factures_detail, name='factures_detail'),
```

`<int:pk>` capture un nombre entier a cet endroit de l'URL et le
transmet a la vue comme argument. `/factures/12/` appelle donc
`factures_detail(request, pk=12)`. C'est ainsi qu'une seule vue peut
gerer la facture n°1, n°2, n°3... sans ecrire une fonction par
facture.

## Ne jamais ecrire une URL en dur : `{% url %}` et `reverse()`

Le `name=` de chaque route sert a generer l'URL correspondante sans
jamais l'ecrire litteralement. Dans un template :

```django
<a href="{% url 'produits_liste' %}">Produits</a>
```

C'est exactement ce que fait `products/templates/partials/sidebar.html`
pour chacun des liens du menu. L'interet : si un jour l'URL
`/produits/` devient `/catalogue/`, il suffit de changer la ligne dans
`products/urls.py` -- tous les liens du site continuent de fonctionner
sans etre touches.

`request.resolver_match.url_name` (utilise dans la meme sidebar pour
surligner le lien de la page active) fonctionne dans l'autre sens : il
donne le `name=` de la route qui vient d'etre resolue pour la requete
en cours.

## A retenir

- Une URL est toujours resolue en deux temps ici : d'abord le fichier
  racine (`GestionPharmacie/urls.py`), qui delegue ensuite a celui de
  l'application (`products/urls.py`).
- Le `name=` de chaque route est ce qui permet de ne jamais ecrire une
  URL en dur, ni dans une vue (`reverse('nom')`) ni dans un template
  (`{% url 'nom' %}`).
- `<int:pk>` (ou `<str:...>`, `<slug:...>`) capture une partie de
  l'URL et la transmet a la vue en argument.

## A essayer

Dans `products/urls.py`, faites renommer temporairement la route
`'produits/'` en `'catalogue/'` (en gardant le meme `name=`). Rechargez
le site : la sidebar continue de pointer au bon endroit sans avoir ete
modifiee, precisement parce qu'elle utilise `{% url 'produits_liste' %}`
et non un lien ecrit en dur. Bon reflexe a faire remarquer : c'est la
preuve concrete de l'interet du `name=`.
