# GestionPharmacie — projet finalise

Version complete de l'application de gestion de pharmacie : le meme
habillage (sidebar, pages, responsive, theme clair/sombre) que
`../GestionPharmacie/`, mais avec le backend Django entierement
branche (modeles, formulaires, vues CRUD, donnees de demonstration).

## Pour les formateurs / eleves : par ou commencer

Tout le parcours pedagogique, module par module, est dans le dossier
[`docs/`](docs/00-introduction.md). Commencez par
[`docs/00-introduction.md`](docs/00-introduction.md). Pour une carte
du projet et un protocole de test complet a faire tourner avant
chaque cours, voir
[`docs/11-guide-complet-et-protocole-de-test.md`](docs/11-guide-complet-et-protocole-de-test.md).

## Demarrage rapide

```bash
source ../env/bin/activate
python manage.py migrate
python manage.py loaddata demo
python manage.py setup_auth        # groupes Gerant/Vendeur + comptes demo
python manage.py createsuperuser   # optionnel, pour /admin/
python manage.py runserver
```

Puis ouvrez `http://127.0.0.1:8000/` et connectez-vous avec
`gerant` / `pharmacie123` (acces complet) ou `vendeur` / `pharmacie123`
(acces restreint — voir [`docs/10-authentification-et-permissions.md`](docs/10-authentification-et-permissions.md)).

## Perimetre de cette version

Couvert : Produits, Stock, Clients, Fournisseurs, Ventes (avec
formset et decrement de stock), Factures — CRUD complet avec
validation cote serveur sur une vraie base SQLite, ainsi que
l'authentification et les permissions (connexion, deconnexion, roles
Gerant/Vendeur).

Volontairement laisse comme exercice (voir
[`docs/09-aller-plus-loin.md`](docs/09-aller-plus-loin.md)) :
filtres/recherche fonctionnels, tableau de bord dynamique, export PDF,
notifications reelles.
