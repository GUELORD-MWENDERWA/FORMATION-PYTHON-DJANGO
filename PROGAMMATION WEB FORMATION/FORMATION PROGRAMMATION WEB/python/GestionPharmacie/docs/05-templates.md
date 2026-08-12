# 05 — Les templates : le langage HTML+Django

## Le principe

Un template est un fichier `.html` "enrichi" : en plus du HTML normal,
il utilise un petit langage propre a Django pour afficher des
variables, repeter du contenu, inclure d'autres fichiers, etc. Django
cherche ces fichiers dans `products/templates/` (grace a `APP_DIRS:
True` dans `settings.py`, voir [02](02-structure-du-projet.md)).

Deux types de balises a bien distinguer des le debut :

| Balise | Role | Exemple dans le projet |
|---|---|---|
| `{{ ... }}` | Affiche la valeur d'une variable | `{{ message }}` |
| `{% ... %}` | Execute une instruction (condition, boucle, heritage...) | `{% if %}`, `{% for %}`, `{% url %}` |

## L'heritage de templates : `{% extends %}` et `{% block %}`

Repeter la structure HTML complete (`<html>`, `<head>`, sidebar...) sur
chacune des vingt pages serait absurde. Django resout ca avec
l'heritage :

`products/templates/base.html` definit le squelette commun (sidebar,
zone de contenu, chargement du CSS/JS) et laisse des "trous" nommes,
les **blocks** :

```django
<title>{% block title %}GestionPharmacie{% endblock %}</title>
...
{% block content %}{% endblock %}
```

Chaque page ne redefinit que ces blocs. Exemple complet,
`products/templates/produits/liste.html` :

```django
{% extends "base.html" %}

{% block title %}Produits - GestionPharmacie{% endblock %}

{% block content %}
  ...
  {% include "partials/products_toolbar.html" %}
  {% include "partials/products_table.html" %}
{% endblock %}
```

`{% extends "base.html" %}` doit toujours etre la toute premiere ligne
du fichier. Le projet a deux gabarits de base : `base.html` (pages
normales, avec sidebar) et `base_auth.html` (page de connexion, sans
sidebar, carte centree) -- voir `products/templates/auth/login.html`.

## `{% include %}` : reutiliser un morceau de HTML

Contrairement a `{% extends %}` (une page HERITE d'un gabarit unique),
`{% include %}` INSERE un fragment de HTML a un endroit precis, autant
de fois que necessaire. Le dossier `products/templates/partials/`
contient les fragments reutilises sur plusieurs pages :

- `sidebar.html` : le menu de navigation, inclus une seule fois dans
  `base.html` -- donc present sur toutes les pages qui en heritent.
- `messages.html` : affiche les messages Django (succes/erreur), lui
  aussi inclus depuis `base.html`.
- `theme_switch.html` : le bouton clair/sombre, inclus dans l'en-tete
  de chaque page de contenu (pas dans `base.html` directement, car
  toutes les pages n'ont pas le meme en-tete).
- `products_toolbar.html` / `products_table.html` : specifiques a la
  page produits, separes en deux fichiers pour rester lisibles.

## Les commentaires de template : un piege classique

Django propose deux syntaxes de commentaire, et une seule accepte
plusieurs lignes :

```django
{# Ceci fonctionne : un commentaire court, sur une seule ligne #}

{% comment %}
  Ceci fonctionne aussi : un commentaire qui peut s'etaler
  sur plusieurs lignes.
{% endcomment %}
```

`{# ... #}` **ne supporte pas les retours a la ligne**. Si on ecrit un
commentaire multi-lignes avec cette syntaxe courte, Django ne le
reconnait plus comme un commentaire et l'affiche tel quel, en texte
brut, sur la page -- un bug deja rencontre et corrige sur ce projet
dans `base.html`. C'est une erreur tres frequente chez les debutants
Django, a signaler explicitement en cours : privilegier `{# #}`
uniquement pour une note courte sur une ligne, et `{% comment %}
{% endcomment %}` des que ca depasse.

## Variables de contexte automatiques : `request`, `messages`

Certaines variables sont disponibles dans TOUS les templates sans que
la vue ait besoin de les transmettre, grace aux `context_processors`
declares dans `settings.py` (voir [02](02-structure-du-projet.md)).
Exemple concret dans `partials/sidebar.html` :

```django
<li class="sidebar-list-item{% if request.resolver_match.url_name == 'home' %} active{% endif %}">
```

`request` est disponible partout grace au context processor
`django.template.context_processors.request` -- c'est ce qui permet de
savoir, depuis n'importe quel template, sur quelle page on se trouve
actuellement (et donc de surligner le bon lien du menu).

## `{% load static %}` et `{% url %}`

Deux "tags" essentiels, presents dans `base.html` :

```django
{% load static %}
...
<link rel="stylesheet" href="{% static 'css/style.css' %}" />
```

`{% load static %}` active le tag `{% static %}` (detail dans
[06](06-fichiers-statiques.md)). `{% url 'nom_de_la_route' %}` genere
un lien a partir du `name=` defini dans `urls.py` (detail dans
[03](03-urls-et-routage.md)) : les deux servent le meme objectif,
ne jamais ecrire un chemin en dur dans le HTML.

## A retenir

- `{% extends %}` = heriter d'UN gabarit (toute la page). `{% include
  %}` = inserer un fragment reutilisable, autant de fois que voulu.
- `{{ variable }}` affiche, `{% tag %}` execute une instruction
  (condition, boucle, heritage, inclusion...).
- `{# #}` = commentaire une seule ligne. `{% comment %}...{%
  endcomment %}` = commentaire multi-lignes. Confondre les deux est
  une source de bug classique, deja rencontree sur ce projet.

## A essayer

Ouvrez `base.html`, `sidebar.html` et `theme_switch.html` en meme
temps et faites suivre visuellement, avec les eleves, le chemin d'un
`{% include %}` : ou est-il ecrit, quel fichier est insere, ou le
resultat apparait-il a l'ecran une fois la page rendue.
