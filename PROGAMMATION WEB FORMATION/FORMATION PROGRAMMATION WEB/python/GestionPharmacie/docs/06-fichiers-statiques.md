# 06 — Fichiers statiques : CSS et JavaScript

## Le principe

Les "fichiers statiques" sont tout ce qui n'est pas genere
dynamiquement par Django : CSS, JavaScript, images, polices... Django
a besoin d'un mecanisme dedie pour les servir, different de celui des
templates, car ce sont des fichiers bruts envoyes tels quels au
navigateur (pas de langage de template a l'interieur).

## Ou ils vivent dans ce projet

```
products/static/
├── css/style.css     (~1400 lignes : toute l'apparence du site)
└── js/script.js      (interactions : menu mobile, filtres, theme clair/sombre)
```

Grace a `'django.contrib.staticfiles'` (present dans `INSTALLED_APPS`,
voir [02](02-structure-du-projet.md)), Django trouve automatiquement
ce dossier `static/` a l'interieur de l'application `products`,
exactement comme il trouve `products/templates/`.

## Les utiliser dans un template

Deux etapes, toujours dans cet ordre, visibles en haut de
`products/templates/base.html` :

```django
{% load static %}
...
<link rel="stylesheet" href="{% static 'css/style.css' %}" />
...
<script src="{% static 'js/script.js' %}"></script>
```

1. `{% load static %}` active le tag `{% static %}` pour ce template
   (a mettre tout en haut du fichier, avant tout usage).
2. `{% static 'css/style.css' %}` genere l'URL finale a partir du
   chemin relatif au dossier `static/` de l'application, en tenant
   compte du prefixe `STATIC_URL` defini dans `settings.py` (`static/`
   par defaut, voir [02](02-structure-du-projet.md)).

On n'ecrit jamais `href="/static/css/style.css"` en dur : si
`STATIC_URL` change un jour (deploiement avec un CDN, par exemple),
tous les liens generes par `{% static %}` restent corrects
automatiquement.

## `style.css` : une seule feuille pour tout le site

Plutot qu'un fichier CSS par page, le projet utilise une seule feuille
partagee, chargee une fois dans `base.html` et donc disponible sur
toutes les pages qui en heritent. Elle couvre la sidebar, les cartes de
statistiques, les tableaux, les formulaires, le theme clair/sombre,
et le comportement responsive (sidebar en tiroir sous 1024px).

## `script.js` : des verifications avant chaque branchement d'evenement

Un point de style Javascript notable, a signaler aux eleves : chaque
bloc verifie que l'element existe avant de brancher un ecouteur
d'evenement dessus.

```js
var jsFilter = document.querySelector(".jsFilter");
if (jsFilter) {
  jsFilter.addEventListener("click", function () {
    document.querySelector(".filter-menu").classList.toggle("active");
  });
}
```

La barre de filtres (`.jsFilter`) n'existe que sur la page produits.
Comme `script.js` est charge sur TOUTES les pages (il est inclus dans
`base.html`), sans ce `if (jsFilter)`, le script provoquerait une
erreur JavaScript ("Cannot read properties of null") des qu'il
essaierait d'attacher un evenement a un element absent de la page
courante. C'est un reflexe systematique a prendre des qu'un script
partage manipule des elements qui n'existent pas forcement partout.

## A retenir

- Fichiers statiques (CSS/JS/images) et templates (`.html`) passent
  par deux mecanismes distincts, meme s'ils vivent tous les deux dans
  l'application `products/`.
- `{% load static %}` puis `{% static 'chemin/fichier' %}` : jamais
  d'URL ecrite en dur vers un fichier statique.
- Un script JS partage sur toutes les pages doit toujours verifier
  qu'un element existe (`if (element) { ... }`) avant d'y attacher un
  comportement, car il ne sera pas present sur chaque page.

## A essayer

Ouvrez les outils de developpement du navigateur (onglet Network) en
rechargeant la page d'accueil, et retrouvez la requete vers
`/static/css/style.css` : c'est la preuve visible que
`{% static %}` a bien genere une vraie URL HTTP, servie separement du
HTML de la page.
