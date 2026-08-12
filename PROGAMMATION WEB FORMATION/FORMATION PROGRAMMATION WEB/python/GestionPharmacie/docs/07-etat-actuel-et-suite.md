# 07 — Ou en est le projet, et quelle est la suite

## Ce qui existe reellement aujourd'hui

- Un projet Django complet et fonctionnel (`manage.py runserver`
  demarre sans erreur, `python manage.py check` ne remonte aucun
  probleme).
- Une application `products` avec **toutes les routes** definies
  (seize URLs dans `products/urls.py`, voir [03](03-urls-et-routage.md)).
- Une vue par page, qui affiche un template **sans donnee dynamique**
  (voir [04](04-vues.md)) : tous les chiffres, listes et lignes de
  tableau visibles a l'ecran sont ecrits en dur dans le HTML.
- Un ensemble complet de templates (une vingtaine de pages) avec
  heritage, fragments reutilisables, responsive et theme clair/sombre
  deja en place (voir [05](05-templates.md)).
- Le CSS et le JS finalises pour l'ensemble de ces pages (voir
  [06](06-fichiers-statiques.md)).

## Ce qui n'existe PAS encore (a bien clarifier aupres des eleves)

Le message du dernier commit du projet ("ajout du projet finalise avec
auth et permissions") concerne en realite le dossier `projetfinaliser/`
ajoute a cote (voir plus bas), **pas** `GestionPharmacie/`. Dans
`GestionPharmacie/` lui-meme, a ce jour :

- **Pas de modeles** : `products/models.py` est vide. Aucune donnee
  n'est stockee ni lue depuis `db.sqlite3` (le fichier existe, mais
  aucune table applicative n'y a ete creee).
- **Pas d'administration** : `products/admin.py` est vide car il n'y a
  encore rien a y enregistrer.
- **Pas de formulaires connectes** : les balises `<form>` du HTML
  (ex. `produits/form.html`) n'ont ni `method`, ni `action`, ni
  `{% csrf_token %}` -- elles ne soumettent encore rien.
- **Pas d'authentification reelle** : la page `/connexion/` affiche
  un formulaire de connexion, mais `views.login()` se contente d'un
  `render()`, sans verifier ni email ni mot de passe. N'importe qui
  peut deja acceder a toutes les pages sans se connecter.
- **Pas de permissions** : consequence directe du point precedent,
  puisqu'il n'y a pas encore d'utilisateurs distincts.

Ce n'est pas une erreur ni un oubli : c'est un choix pedagogique
deliberer. Construire d'abord tout le squelette visuel et le routage
(le "frontend habille") avant de brancher le backend permet de
travailler chaque brique separement, avec un resultat visible a chaque
etape.

## La suite logique, dans l'ordre naturel de construction Django

1. **Modeles** (`products/models.py`) : definir les classes
   (`Produit`, `Client`, `Fournisseur`, `Vente`, `Facture`...) puis
   generer et appliquer les migrations (`makemigrations`, `migrate`).
2. **Admin** (`products/admin.py`) : enregistrer ces modeles pour
   pouvoir creer des donnees de test sans ecrire de formulaire.
3. **Vues connectees a la base** : remplacer les `render(request,
   'template.html')` par des vues qui interrogent les modeles
   (`Produit.objects.all()`) et transmettent le resultat au template
   via `context`.
4. **Formulaires Django** (`forms.py`, nouveau fichier) : remplacer
   les `<form>` HTML muets par de vrais `ModelForm`, avec validation et
   sauvegarde en base.
5. **Authentification** : utiliser `django.contrib.auth` (deja dans
   `INSTALLED_APPS`) pour une vraie connexion, puis `@login_required`
   sur les vues sensibles.
6. **Permissions** : groupes et droits Django pour distinguer par
   exemple un role "Gerant" (acces complet) d'un role "Vendeur" (acces
   restreint).

## Le corrige de reference : `projetfinaliser/`

A cote de `GestionPharmacie/`, le dossier `projetfinaliser/` contient
**exactement les six etapes ci-dessus deja realisees**, avec son propre
jeu de documents dans `projetfinaliser/docs/` (`01-modeles.md` a
`10-authentification-et-permissions.md`) qui explique, module par
module, comment on construit ce backend par-dessus le meme habillage
visuel. Une fois que les eleves maitrisent bien l'etat decrit dans ce
dossier-ci (`GestionPharmacie/docs/`), c'est la suite naturelle du
cours -- soit comme trame pour continuer a coder ensemble, soit comme
corrige a distribuer apres coup.

## A retenir

- Le projet "s'arrete", volontairement, juste avant le backend :
  routage + affichage complets, donnees et logique metier absentes.
- Ne jamais laisser croire que l'authentification ou les permissions
  existent deja dans `GestionPharmacie/` : le formulaire de connexion
  est un habillage visuel, pas une fonctionnalite.
- La suite est deja ecrite, module par module, dans
  `projetfinaliser/docs/` : ce document sert de pont entre les deux.
