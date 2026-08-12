# 01 — Qu'est-ce que Django ? Le schema MVT

## Le probleme que Django resout

Avant Django, dans la formation, on a ecrit des pages HTML/CSS/JS
statiques (dossiers precedents de la formation) puis du Python "pur"
(fonctions, boucles, petits programmes en console). Un site web
utile doit combiner les deux : recevoir une requete du navigateur,
executer du code Python pour decider quoi faire, puis renvoyer du
HTML genere dynamiquement. C'est exactement ce role que joue un
**framework web** comme Django : il fournit toute la mecanique
(serveur de developpement, routage des URLs, moteur de templates,
acces a une base de donnees, etc.) pour qu'on n'ait a ecrire que la
logique propre a NOTRE application.

## Le schema MVT (Model - View - Template)

Django organise le code selon trois roles bien separes. C'est la note
laissee dans `GestionPharmacie/explication.txt` :

```
structure de django :
M V T : avec le M model, V : views, T: template
```

En detail :

| Lettre | Role | Fichier(s) dans ce projet | Contenu actuel |
|---|---|---|---|
| **M**odel | Represente les donnees (une table de base de donnees = une classe Python) | `products/models.py` | vide pour l'instant, voir [07](07-etat-actuel-et-suite.md) |
| **V**iew | Recoit la requete, decide quoi faire, renvoie une reponse | `products/views.py` | une fonction par page, voir [04](04-vues.md) |
| **T**emplate | Le HTML avec un mini-langage pour afficher des donnees | `products/templates/*.html` | une vingtaine de pages, voir [05](05-templates.md) |

C'est une variante du patron **MVC** (Model-View-Controller) que l'on
retrouve dans beaucoup d'autres frameworks (Laravel, Ruby on Rails,
Spring...) ; seul le vocabulaire change un peu : ce que Django appelle
"View" correspond au "Controller" ailleurs, et son "Template"
correspond a la "View" ailleurs. Le principe reste le meme partout :
**ne jamais melanger la logique metier et l'affichage** dans le meme
fichier.

Le trajet d'une requete, dans l'ordre, avec le fichier concerne :

```
Navigateur --GET /produits/--> urls.py --> views.py --> models.py (pas encore utilise)
                                              |
                                              v
                                        templates/*.html --> reponse HTML --> Navigateur
```

C'est exactement l'ordre suivi par les documents [03](03-urls-et-routage.md),
[04](04-vues.md) et [05](05-templates.md).

## Installer Django (ce qui a deja ete fait pour ce projet)

```bash
python -m venv env                 # cree un environnement virtuel
source env/bin/activate            # l'active (Linux/Mac)
pip install django                 # installe Django dedans
django-admin startproject GestionPharmacie   # cree le projet
cd GestionPharmacie
python manage.py startapp products           # cree une application
```

Un environnement virtuel (`env/`) isole les paquets Python installes
pour ce projet du reste de la machine ; c'est pour ca qu'il ne figure
pas dans les fichiers commis sur Git (voir `.gitignore`) et qu'il faut
toujours l'activer avant de lancer une commande `python manage.py ...`.

## Projet vs Application

Deux mots reviennent tout le temps et qu'il faut distinguer :

- Un **projet** (`GestionPharmacie/`, le dossier genere par
  `startproject`) est la configuration globale du site : reglages,
  liste des applications actives, routage principal.
- Une **application** (`products/`, generee par `startapp`) est un
  module reutilisable qui traite UN domaine fonctionnel (ici : la
  gestion de la pharmacie). Un projet peut contenir plusieurs
  applications (par exemple, plus tard : `products`, `facturation`,
  `utilisateurs`...) ; ici il n'y en a qu'une.

Voir [02](02-structure-du-projet.md) pour le detail fichier par
fichier des deux.

## A retenir

- MVT = Model (donnees) / View (logique) / Template (affichage) : ce
  decoupage est LA notion a bien faire passer avant tout le reste.
- "Projet" = configuration globale. "Application" = un module
  fonctionnel a l'interieur du projet.
- Toute commande Django passe par `manage.py` (`python manage.py
  runserver`, `startapp`, `migrate`, etc.), et doit etre lancee avec
  l'environnement virtuel active.

## A essayer

Demandez aux eleves d'ouvrir `GestionPharmacie/explication.txt` et de
reformuler, dans leurs mots, ce que fait chaque lettre M/V/T -- avant
meme d'ouvrir le code. C'est la meilleure verification qu'ils ont
compris le concept avant de le voir applique.
