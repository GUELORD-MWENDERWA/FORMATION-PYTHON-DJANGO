# 00 — Sommaire et mode d'emploi

Ces documents expliquent, fichier par fichier, ce que contient le
dossier `GestionPharmacie/` **tel qu'il est aujourd'hui** : la partie
Django construite pendant la formation, du tout premier `django-admin
startproject` jusqu'a l'etat actuel (routage + vues + templates,
encore sans base de donnees reelle). Ils sont ecrits pour vous
(formateur) afin de pouvoir reexpliquer chaque brique aux eleves sans
avoir a tout redecouvrir sur le moment.

## A ne pas confondre avec `projetfinaliser/`

Le projet contient deux dossiers Django cote a cote, a la racine de
`python/` :

- **`GestionPharmacie/`** (celui documente ici) : le projet des
  eleves, tel qu'on l'a construit en cours. C'est celui-ci qui est
  "arrete" au stade actuel.
- **`projetfinaliser/`** : une version corrigee/avancee de la meme
  application, avec un backend complet (modeles, formulaires,
  authentification...). Son propre dossier `projetfinaliser/docs/`
  explique comment on construit ce backend, module par module. Ne
  melangez pas les deux jeux de documentation : celui-ci (dans
  `GestionPharmacie/docs/`) s'arrete volontairement avant le backend,
  pour rester au niveau exact ou en sont les eleves.

## Plan de ces documents

1. [01 — Qu'est-ce que Django ? Le schema MVT](01-introduction-django.md)
2. [02 — Anatomie du projet : tous les fichiers, un par un](02-structure-du-projet.md)
3. [03 — Les URLs : comment une adresse devient une page](03-urls-et-routage.md)
4. [04 — Les vues : la fonction Python derriere chaque page](04-vues.md)
5. [05 — Les templates : le langage HTML+Django](05-templates.md)
6. [06 — Fichiers statiques : CSS et JavaScript](06-fichiers-statiques.md)
7. [07 — Ou en est le projet, et quelle est la suite](07-etat-actuel-et-suite.md)

## Comment utiliser ces documents en cours

Chaque fichier reprend une seule brique de Django, avec :

- une explication du **concept** avant de regarder le code (pourquoi
  ce fichier existe, quel probleme il resout) ;
- le code **reellement present** dans le projet, commente ligne par
  ligne quand c'est utile ;
- une section **"A retenir"** avec les 2-3 points essentiels a faire
  passer aux eleves ;
- quand c'est pertinent, une section **"A essayer"** avec une
  manipulation concrete a faire devant eux (lancer le serveur,
  modifier une ligne, observer le resultat).

L'ordre suit exactement celui dans lequel Django traite une requete :
une URL arrive (03), elle declenche une vue (04), la vue rend un
template (05) qui peut charger des fichiers statiques (06). Le
document 02 sert de carte generale avant de plonger dans le detail, et
le document 01 pose le vocabulaire (MVT) utilise partout ensuite.

## Faire tourner le projet

```bash
cd GestionPharmacie
source ../env/bin/activate      # environnement virtuel partage (voir 01)
python manage.py runserver
```

Puis ouvrir `http://127.0.0.1:8000/`. Aucune connexion n'est demandee
pour l'instant : la page d'accueil s'affiche directement (voir
[07](07-etat-actuel-et-suite.md) pour la raison).
