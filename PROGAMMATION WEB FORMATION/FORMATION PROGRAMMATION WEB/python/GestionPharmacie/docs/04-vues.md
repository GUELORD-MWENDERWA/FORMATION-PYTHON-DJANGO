# 04 — Les vues : la fonction Python derriere chaque page

## Le principe

Une vue est une simple **fonction Python** qui recoit une requete
(`request`) et doit renvoyer une reponse. Dans `products/views.py`,
chaque page du site a la sienne :

```python
def home(request):
    return render(request, 'home.html')

def produits_liste(request):
    return render(request, 'produits/liste.html')

def factures_detail(request, pk):
    return render(request, 'factures/detail.html')
```

`request` est fourni automatiquement par Django a chaque appel : c'est
un objet qui contient tout ce que le navigateur a envoye (methode
GET/POST, donnees de formulaire, utilisateur connecte, cookies...).
`pk` (pour `factures_detail`) vient de l'URL elle-meme, capture par
`<int:pk>` dans `products/urls.py` (voir [03](03-urls-et-routage.md)).

## `render()` : la fonction la plus utilisee ici

```python
from django.shortcuts import render

def produits_liste(request):
    return render(request, 'produits/liste.html')
```

`render(request, template, context=None)` fait deux choses en une
ligne : elle va chercher le fichier template indique (voir
[05](05-templates.md)), l'execute avec les donnees fournies dans
`context` (un dictionnaire), puis renvoie le HTML resultant sous forme
d'une reponse HTTP prete a etre affichee par le navigateur.

## L'etat actuel : des vues "muettes"

Toutes les vues du projet ont aujourd'hui la meme forme minimale :
elles affichent un template, sans lui transmettre aucune donnee. Le
commentaire en tete de `products/views.py` le resume :

```python
# Vues de simple affichage pour le moment : chaque vue ne fait
# qu'afficher son template (aucune donnee de la base pour l'instant,
# ca viendra avec l'integration Django).
```

Concretement, les chiffres visibles sur le tableau de bord (128
produits references, 24 ventes du jour...) ou la liste de produits
sont ecrits **en dur dans le HTML** (voir `products/templates/home.html`),
pas calcules par la vue. C'est normal a ce stade : construire d'abord
tout le "squelette" (routage + affichage) avant de le brancher a de
vraies donnees. La suite logique -- passer des donnees a `render()` via
`context` une fois que `models.py` contiendra de vrais modeles -- est
detaillee dans [07](07-etat-actuel-et-suite.md).

A quoi ressemblera une vue une fois branchee a la base de donnees
(exemple, pas encore dans le code) :

```python
def produits_liste(request):
    produits = Produit.objects.all()          # va chercher les lignes en base
    return render(request, 'produits/liste.html', {
        'produits': produits,                  # transmis au template
    })
```

## Une vue par page, un motif tres repetitif

Le fichier `views.py` suit toujours le meme schema : liste + formulaire
pour chaque module (produits, ventes, clients, fournisseurs), une
seule vue pour les pages uniques (statistiques, notifications,
parametres, connexion). Faire remarquer ce motif aux eleves aide a
lire vite un fichier de vues inconnu, meme tres long.

## A retenir

- Une vue = une fonction Python qui prend `request` (+ eventuellement
  des arguments captures dans l'URL) et renvoie une reponse.
- `render(request, template, context)` est le raccourci le plus
  courant : il combine chargement du template + injection des donnees
  + generation de la reponse HTML.
- Ici, `context` n'est encore jamais utilise : les vues ne font
  qu'afficher un template statique. C'est la limite actuelle du
  projet, pas une erreur.

## A essayer

Modifiez temporairement `home()` pour passer une variable :

```python
def home(request):
    return render(request, 'home.html', {'message': 'Bonjour depuis la vue !'})
```

puis ajoutez `{{ message }}` n'importe ou dans `home.html` et
rechargez la page. C'est la demonstration la plus directe du lien
vue -> template avant d'aborder les vrais modeles.
