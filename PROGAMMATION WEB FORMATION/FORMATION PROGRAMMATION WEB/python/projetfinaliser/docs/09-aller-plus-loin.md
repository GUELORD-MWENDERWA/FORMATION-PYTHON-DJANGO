# 09 — Pour aller plus loin (exercices)

Ce module cloture le cours principal (01 a 08). Ce qui suit n'est pas
corrige dans `projetfinaliser/` : c'est une liste d'exercices a donner
aux eleves une fois le CRUD de base assimile, du plus simple au plus
ambitieux. Chaque exercice s'appuie sur des patrons deja vus dans les
modules precedents.

## Facile — consolider ce qui existe deja

- **Pagination** : `/produits/` et les autres listes chargent tous les
  enregistrements d'un coup. Utiliser `django.core.paginator.Paginator`
  dans les vues `*_liste` et ajouter des boutons "page suivante /
  precedente" dans les templates.
- **Tests automatises** : `products/tests.py` est vide. Ecrire des
  `TestCase` qui verifient, par exemple, qu'une vente avec une
  quantite superieure au stock est bien rejetee (module 06), ou qu'un
  produit supprime disparait de `/produits/`.
- **Bouton "Ajuster le stock"** (`/stock/`) : actuellement decoratif.
  Creer une vue + un petit formulaire (nouvelle quantite + raison de
  l'ajustement) qui modifie `produit.stock` directement, sans passer
  par une vente.

## Intermediaire — fonctionnalites volontairement laissees de cote

L'authentification et les permissions, qui figuraient ici, sont
maintenant traitees pour de vrai au [module 10](10-authentification-et-permissions.md) —
ce n'est plus un exercice. Il reste ces deux points, volontairement
non retenus pour la version de base :

- **Filtres et recherche fonctionnels** : les barres de recherche et
  le panneau de filtres (categorie / statut) presents sur plusieurs
  pages sont purement visuels. Les rendre actifs cote serveur, en
  lisant `request.GET.get('q')` dans les vues `*_liste` et en filtrant
  le queryset (`Produit.objects.filter(nom__icontains=q)`).
- **Tableau de bord dynamique** : `home.html` affiche des statistiques
  et des ventes recentes figees dans le HTML. Les calculer depuis la
  base (nombre de ventes du jour, chiffre d'affaires du mois via
  `Sum`, produits en rupture via les `@property` du module 04...) et
  les passer en contexte a la vue `home`.

## Avance — nouvelles briques

- **Menu deroulant sur la vue grille des produits** : en vue grille
  (bouton "Vue grille" sur `/produits/`), le bouton "..." de chaque
  carte renvoie directement vers la modification (voir module 03). En
  faire un vrai menu deroulant (modifier / supprimer / voir), avec un
  peu de JavaScript pour l'ouverture/fermeture — bon exercice de
  manipulation du DOM une fois le CRUD acquis.
- **Export PDF d'une facture** : le bouton "Telecharger en PDF" de
  `/factures/<id>/` est desactive. Une bibliotheque comme `weasyprint`
  ou `xhtml2pdf` peut generer un PDF a partir du meme template HTML
  deja utilise pour l'affichage.
- **Notifications reelles** : `/notifications/` est statique.
  Generer une notification (ou au moins une requete calculee a la
  volee) a chaque produit qui entre en rupture ou en stock faible,
  en reutilisant les `@property` du module 04.
- **API avec Django REST Framework** : exposer les modeles du module
  01 via une API JSON (`/api/produits/`, etc.) — utile si un futur
  module du cours introduit une application mobile ou un frontend
  JavaScript separe.

## Comment aborder ces exercices en classe

Pour chacun, faites re-suivre aux eleves la meme methode que les
modules 01-08 : d'abord la question "quel modele/champ ai-je deja, et
lequel me manque ?", puis formulaire, puis vue, puis template — dans
cet ordre, presque systematiquement. C'est le patron general de tout
developpement Django, pas seulement de ce projet.
