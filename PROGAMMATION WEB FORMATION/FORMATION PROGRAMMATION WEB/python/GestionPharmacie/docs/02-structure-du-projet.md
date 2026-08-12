# 02 — Anatomie du projet : tous les fichiers, un par un

Vue d'ensemble du dossier `GestionPharmacie/` (fichiers de code
uniquement, sans les caches `__pycache__/`) :

```
GestionPharmacie/                  <- racine du depot pour ce projet
├── manage.py                      <- point d'entree de toutes les commandes Django
├── db.sqlite3                     <- la base de donnees (fichier unique, SQLite)
├── .gitignore                     <- fichiers/dossiers a ne pas commiter (env/, __pycache__/...)
│
├── GestionPharmacie/               <- dossier de CONFIGURATION du projet
│   ├── __init__.py                <- rend ce dossier importable comme un module Python
│   ├── settings.py                <- tous les reglages du projet
│   ├── urls.py                    <- URLs racine (voir 03)
│   ├── wsgi.py / asgi.py          <- points d'entree pour un serveur de production
│   └── explication.txt            <- note de cours sur le schema MVT
│
└── products/                      <- l'APPLICATION "products"
    ├── __init__.py
    ├── apps.py                    <- declaration de l'application
    ├── admin.py                   <- enregistrement des modeles pour /admin/
    ├── models.py                  <- les donnees (vide pour l'instant, voir 07)
    ├── views.py                   <- une fonction par page (voir 04)
    ├── urls.py                    <- URLs de l'application (voir 03)
    ├── tests.py                   <- tests automatises
    ├── migrations/                <- historique des changements de modeles
    ├── static/
    │   ├── css/style.css          <- toute l'apparence du site (~1400 lignes)
    │   └── js/script.js           <- interactions (menu mobile, filtres, theme...)
    └── templates/                 <- tout le HTML (voir 05)
        ├── base.html              <- gabarit commun (sidebar + zone de contenu)
        ├── base_auth.html         <- gabarit pour la page de connexion
        ├── home.html, auth/, produits/, stock/, ventes/, clients/,
        │   fournisseurs/, factures/, statistiques/, notifications/,
        │   parametres/            <- une page (ou un groupe de pages) par module
        └── partials/               <- morceaux de HTML reutilises entre plusieurs pages
```

## `manage.py`

Genere automatiquement, on n'y touche quasiment jamais. C'est la porte
d'entree de toutes les commandes : `runserver` (lance le serveur de
developpement), `startapp` (cree une nouvelle application),
`makemigrations` / `migrate` (gestion de la base de donnees), `test`
(lance les tests), etc. Toutes s'ecrivent `python manage.py <commande>`.

## `GestionPharmacie/settings.py`

Le fichier de reglages du projet entier. Les sections importantes a ce
stade (voir les commentaires ajoutes directement dans le fichier) :

- `INSTALLED_APPS` : la liste des applications actives, y compris
  `'products'` -- sans cette ligne, Django ignorerait completement
  notre application (ses templates, ses futurs modeles...).
- `MIDDLEWARE` : une chaine de traitements appliques a chaque requete
  (securite, sessions, authentification, messages...).
- `TEMPLATES` : ou et comment Django cherche les fichiers `.html`
  (voir [05](05-templates.md)).
- `DATABASES` : quelle base de donnees utiliser -- ici SQLite, un
  simple fichier (`db.sqlite3`), pratique pour apprendre sans installer
  de serveur de base de donnees.
- `STATIC_URL` : le prefixe d'URL pour le CSS/JS (voir
  [06](06-fichiers-statiques.md)).

## `GestionPharmacie/urls.py` vs `products/urls.py`

Il y a bien DEUX fichiers `urls.py` dans le projet, et c'est normal :
le premier (dans le dossier de configuration) est la racine, le second
(dans l'application) contient les routes propres a `products`. Detail
complet dans [03](03-urls-et-routage.md).

## `products/apps.py`, `admin.py`, `models.py`, `tests.py`

Ces quatre fichiers sont generes automatiquement par `startapp` et
restent, a ce stade du cours, proches de leur contenu d'origine :

- `apps.py` declare l'application aupres de Django (nom, config).
- `admin.py` sert a enregistrer les modeles pour qu'ils apparaissent
  sur `/admin/` -- vide car `models.py` ne definit encore aucun
  modele.
- `models.py` est la ou vivront les futures classes representant les
  produits, ventes, clients... (le **M** de MVT). Voir
  [07](07-etat-actuel-et-suite.md) pour ce que ca donnera.
- `tests.py` est la ou ecrire les tests automatises du projet.

Chacun contient desormais un commentaire expliquant a quoi il servira
concretement pour CE projet (pharmacie) des que le backend sera
construit : ouvrez-les avec les eleves, c'est plus parlant que de
lire la doc Django generique.

## `products/migrations/`

Un dossier qui contiendra l'historique des changements apportes aux
modeles (un fichier Python genere par `makemigrations` a chaque
modification de `models.py`). Il ne contient pour l'instant que
`__init__.py`, car aucun modele n'existe encore.

## A retenir

- Deux dossiers de configuration a ne pas confondre :
  `GestionPharmacie/` (le projet, reglages globaux) et `products/`
  (une application, un domaine fonctionnel).
- Chaque fichier genere par `startapp`/`startproject` a un role fixe
  et previsible : une fois qu'on connait le nom, on sait a quoi il
  sert dans N'IMPORTE QUEL projet Django, pas seulement celui-ci.

## A essayer

Faites ouvrir les deux dossiers `GestionPharmacie/` (config) et
`products/` (app) cote a cote dans l'explorateur de fichiers de
l'IDE, et demandez aux eleves de retrouver, sans aide, dans lequel des
deux se trouve chacun des elements du tableau du document
[01](01-introduction-django.md#le-schema-mvt-model---view---template).
