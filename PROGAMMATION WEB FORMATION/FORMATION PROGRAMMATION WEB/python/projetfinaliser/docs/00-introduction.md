# 00 — Introduction et plan du cours

## Les deux dossiers du projet

- **`GestionPharmacie/`** : le point de depart. L'habillage complet
  (sidebar, pages, formulaires, responsive, theme clair/sombre) existe
  deja en HTML/CSS/JS, mais les vues Django ne font qu'afficher des
  templates statiques (`return render(request, 'produits/liste.html')`,
  sans aucune donnee de base). C'est le projet a donner aux eleves
  comme squelette de depart.
- **`projetfinaliser/`** : la meme application, mais avec tout le
  backend Django ecrit par-dessus (modeles, migrations, formulaires,
  vues CRUD, donnees de demo). C'est le corrige de reference. Ce
  dossier `docs/` explique, module par module, **comment on passe de
  l'un a l'autre**.

Vous pouvez soit faire suivre ces documents aux eleves en parallele de
leur propre `GestionPharmacie/`, soit les utiliser vous-meme comme
trame de cours puis leur distribuer `projetfinaliser/` comme corrige
une fois l'exercice termine.

## Pourquoi cet ordre

Chaque module ajoute une couche complete et testable avant de passer
au suivant, dans l'ordre ou un developpeur Django construit
naturellement une application :

1. [01 — Modeles et migrations](01-modeles.md)
2. [02 — Admin et donnees de demonstration](02-admin-et-donnees-demo.md)
3. [03 — CRUD Produits (formulaires + vues)](03-produits-crud.md)
4. [04 — Stock (reutiliser un modele existant)](04-stock.md)
5. [05 — Clients et Fournisseurs (repeter le patron CRUD)](05-clients-fournisseurs.md)
6. [06 — Ventes : formulaires imbriques (formsets)](06-ventes-et-formsets.md)
7. [07 — Factures (vue lecture seule d'une vente)](07-factures.md)
8. [08 — Messages et erreurs de formulaire](08-messages-et-erreurs.md)
9. [09 — Pour aller plus loin (exercices)](09-aller-plus-loin.md)
10. [10 — Authentification et permissions](10-authentification-et-permissions.md)

Chaque fichier se termine par une section **"Testez"** avec des
commandes ou des manipulations concretes a faire dans le navigateur
avant de passer a la suite. Ne sautez pas une etape sans avoir vu
l'application fonctionner : c'est le fil conducteur de tout le cours.

## Pre-requis techniques

- Python 3.12+, Django 6.1 (deja installe dans `env/` a la racine du
  projet, partage entre tous les dossiers `python/*`).
- `Pillow` pour la gestion des photos de produits (`pip install
  Pillow`) — deja installe si vous suivez ce cours a partir de cette
  meme machine.
- Aucune connaissance de base de donnees SQL n'est necessaire : l'ORM
  Django (les modeles) s'en charge.

## Demarrage rapide (verifier que projetfinaliser tourne)

```bash
cd projetfinaliser
source ../env/bin/activate          # environnement virtuel partage
python manage.py migrate            # cree la base SQLite locale
python manage.py loaddata demo      # charge les donnees d'exemple
python manage.py setup_auth         # cree les groupes Gerant/Vendeur + comptes demo
python manage.py runserver
```

Ouvrez `http://127.0.0.1:8000/`. Vous devez atterrir sur la page de
connexion : identifiez-vous avec `gerant` / `pharmacie123` (acces
complet) ou `vendeur` / `pharmacie123` (acces restreint, voir
[module 10](10-authentification-et-permissions.md)). Vous devez voir
le tableau de bord, puis pouvoir naviguer vers Produits / Stock /
Ventes / Clients / Fournisseurs / Factures et y voir de vraies donnees
(pas les lignes figees du mockup d'origine).

## Le bug corrige dans GestionPharmacie avant de commencer

Avant de construire ce backend, un bug de template a ete corrige dans
`GestionPharmacie/products/templates/base.html` : trois commentaires
`{# ... #}` s'etalaient sur plusieurs lignes. Or la syntaxe courte de
commentaire Django `{# ... #}` **ne supporte pas les retours a la
ligne** (contrairement a `{% comment %}...{% endcomment %}`) : le
moteur de template ne reconnaissait plus ces blocs comme des
commentaires et les affichait tels quels, en texte brut, sur chaque
page. C'est ce qui produisait le texte parasite visible a l'ecran.
Retenez cette regle, elle revient souvent chez les debutants Django :

```django
{# Ceci fonctionne : un commentaire court, sur une seule ligne #}

{% comment %}
  Ceci fonctionne aussi : un commentaire qui peut s'etaler
  sur plusieurs lignes.
{% endcomment %}

{# Ceci NE fonctionne PAS : Django ne reconnait pas le bloc
   comme un commentaire des qu'il y a un saut de ligne avant #} <!-- casse -->
```
