# 11 — Guide complet et protocole de test

Ce module ne construit rien de nouveau : c'est une vue d'ensemble a
garder ouverte pendant que vous enseignez, plus un protocole de test
de bout en bout a faire tourner (a) avant chaque cours, pour verifier
que la demo n'est pas cassee, et (b) a donner aux eleves comme
"criteres d'acceptation" une fois qu'ils ont reconstruit leur propre
version dans `GestionPharmacie/`.

Les modules [01](01-modeles.md) a [10](10-authentification-et-permissions.md)
restent la reference pour *comprendre* chaque brique. Celui-ci sert a
*verifier* que tout l'ensemble fonctionne ensemble.

## 1. Carte du projet

### Les 6 modeles et leurs relations

```
Categorie ──┐
            │ (PROTECT)
Fournisseur ─┼──> Produit ──┐
            │ (SET_NULL)    │ (PROTECT, via LigneVente)
            │               │
Client ─────┴──(SET_NULL)──> Vente ──1:N──> LigneVente
```

- Une **Vente** a plusieurs **LigneVente** (`vente.lignes.all()`) ;
  chaque ligne fige un `produit` et son `prix_unitaire` au moment de
  la vente (le prix du `Produit` peut changer plus tard sans jamais
  modifier une facture deja emise).
- Supprimer une `Categorie` est bloque tant qu'un `Produit` l'utilise
  (`on_delete=PROTECT`). Supprimer un `Fournisseur` ou un `Client`
  n'efface rien : le lien est juste mis a `null` (`SET_NULL`).
- Supprimer un `Produit` deja vendu est bloque (`PROTECT` sur
  `LigneVente.produit`) : l'historique des ventes ne peut jamais
  perdre sa reference produit.

### Table des URLs, vues et permissions

| URL | Vue | Nom (`{% url %}`) | Qui peut y acceder |
|---|---|---|---|
| `/` | `home` | `home` | Tout compte connecte |
| `/produits/` | `produits_liste` | `produits_liste` | Tout compte connecte |
| `/produits/ajouter/`, `/produits/<pk>/modifier/` | `produits_form` | `produits_form`, `produits_edit` | Tout compte connecte |
| `/produits/<pk>/supprimer/` (POST) | `produits_delete` | `produits_delete` | Permission `products.delete_produit` (Gerant seulement) |
| `/stock/` | `stock_liste` | `stock_liste` | Tout compte connecte |
| `/clients/` + form | `clients_liste`, `clients_form` | ... | Tout compte connecte |
| `/clients/<pk>/supprimer/` (POST) | `clients_delete` | `clients_delete` | Permission `products.delete_client` (Gerant seulement) |
| `/fournisseurs/...` (liste, form, delete) | `fournisseurs_*` | ... | **Gerant uniquement** (`@gerant_required`) |
| `/ventes/`, `/ventes/nouvelle/` | `ventes_liste`, `ventes_form` | ... | Tout compte connecte |
| `/factures/`, `/factures/<pk>/` | `factures_liste`, `factures_detail` | ... | Tout compte connecte |
| `/statistiques/`, `/notifications/` | `statistiques`, `notifications` | ... | Tout compte connecte (pages statiques, voir [module 09](09-aller-plus-loin.md)) |
| `/parametres/` | `parametres` | `parametres` | **Gerant uniquement** |
| `/connexion/`, `/deconnexion/` | `login`, `logout_view` | `login`, `logout` | Public |
| `/admin/` | admin Django | — | Compte `is_staff` (Gerant) pour les modeles `products` ; `is_superuser` pour tout voir, y compris Groupes/Utilisateurs |

### Matrice des permissions (groupe `Vendeur` vs `Gerant`)

Definie dans [`setup_auth.py`](../products/management/commands/setup_auth.py) :

| Action | Vendeur | Gerant |
|---|---|---|
| Voir/ajouter/modifier Produits, Clients, Ventes | Oui | Oui |
| Supprimer Produits, Clients | **Non (403)** | Oui |
| Voir/gerer Fournisseurs | **Non (redirection + message)** | Oui |
| Acceder a `/parametres/` | **Non** | Oui |
| Acceder a `/admin/` | Non (`is_staff=False`) | Oui (modeles `products` seulement, pas Groupes/Utilisateurs) |

## 2. Demarrage propre (a faire avant chaque cours)

Repartir d'une base saine, comme si vous cloniez le projet pour la
premiere fois :

```bash
cd projetfinaliser
rm -f db.sqlite3                     # jamais versionne (voir .gitignore)
source ../env/bin/activate
python manage.py migrate
python manage.py loaddata demo
python manage.py setup_auth
python manage.py runserver
```

`db.sqlite3` et `media/` sont dans `.gitignore` : les supprimer ne
touche a rien de versionne, et les regenerer avec les 3 commandes
ci-dessus prend quelques secondes.

### Verification rapide en une commande

```bash
python manage.py check && python manage.py showmigrations
```

Doit afficher `System check identified no issues (0 silenced)` et
toutes les migrations cochees `[X]`. Si une migration n'est pas
cochee, `migrate` n'a pas ete relance apres un changement de
`models.py`.

## 3. Les donnees de demo (`products/fixtures/demo.json`)

`loaddata demo` cree volontairement des cas particuliers pour pouvoir
demontrer chaque etat sans rien creer a la main :

| Produit | Stock | Seuil alerte | Etat demontre |
|---|---|---|---|
| Paracetamol 500mg | 0 | 15 | `en_rupture = True` |
| Gel hydroalcoolique | 4 | 10 | `stock_faible = True` |
| Tensiometre digital | 2 | 5 | `stock_faible = True` |
| Amoxicilline 500mg | 18 | 15 | `peremption_proche = True` (date < 30 jours) |
| Doliprane 1000mg / Creme hydratante | stock confortable | — | Cas "normal" |

5 ventes de demo couvrent les 3 modes de paiement (especes, carte,
mobile money), 3 statuts (`payee`, `en_attente`, `annulee`) et un cas
"client de passage" (vente `F-2026-3`, sans `client` associe — verifie
que `{{ vente.client|default:"Client de passage" }}` s'affiche bien
dans les templates plutot qu'une erreur).

## 4. Protocole de test complet

A faire dans l'ordre, dans le navigateur, juste apres le demarrage
propre (section 2). Chaque etape doit reussir avant de passer a la
suivante — c'est le meme reflexe que la section "Testez" de chaque
module, mais pour l'application entiere.

### A. Sans etre connecte

1. Ouvrez `/produits/` (ou n'importe quelle URL protegee) : vous devez
   etre redirige vers `/connexion/?next=/produits/`.
2. Sur `/connexion/`, entrez un mauvais mot de passe : message d'erreur
   "Nom d'utilisateur ou mot de passe incorrect.", vous restez sur la
   page.

### B. Connecte en `vendeur` / `pharmacie123`

3. Apres connexion, vous atterrissez sur `/` (grace au `?next=`, sinon
   sur `home`). La sidebar affiche Accueil, Produits, Stock, Ventes,
   Clients, Factures, Statistiques, Notifications — **mais pas**
   Fournisseurs ni Parametres.
4. `/produits/` : les 6 produits de demo s'affichent, y compris
   Paracetamol 500mg marque en rupture. Le bouton "Ajouter" fonctionne
   et cree un produit. Le bouton "Supprimer" **n'apparait sur aucune
   ligne**.
5. Tapez directement `/fournisseurs/` dans la barre d'adresse : vous
   etes renvoye a l'accueil avec le message "Cette page est reservee
   aux gerants." Meme resultat pour `/parametres/`.
6. Toujours en `vendeur`, forcez un `POST` vers
   `/produits/1/supprimer/` (par exemple via les outils developpeur du
   navigateur, ou `curl`, voir section 5) : reponse **403**, pas une
   redirection — la personne est bien connectee, elle n'a simplement
   pas la permission.
7. `/ventes/nouvelle/` : choisissez un produit, une quantite
   **superieure a son stock** (ex. 999 x Paracetamol) : le formulaire
   est rejete avec le message "Stock insuffisant pour ... (0
   disponible(s))." (voir [module 06](06-ventes-et-formsets.md)).
   Recommencez avec une quantite valide sur un produit en stock (ex. 3
   x Creme hydratante) : la vente est creee, vous etes redirige vers
   `/factures/<id>/`, et `/produits/` montre le stock diminue
   d'exactement 3.
8. Deconnectez-vous (`/deconnexion/`) : retour a `/connexion/` avec un
   message de confirmation.

### C. Connecte en `gerant` / `pharmacie123`

9. La sidebar affiche desormais Fournisseurs et Parametres. `/produits/`
   montre le bouton "Supprimer" sur chaque ligne, et il fonctionne
   reellement (le produit disparait de la liste).
10. `/fournisseurs/` : CRUD complet (les 3 fournisseurs de demo,
    ajout, modification, suppression).
11. `/admin/` : la connexion fonctionne (`is_staff=True`). Vous voyez
    la section "PRODUCTS" avec les 6 modeles, mais **pas** la section
    "AUTHENTIFICATION ET AUTORISATION" (Groupes/Utilisateurs) — le
    groupe Gerant n'a que les permissions de l'app `products`, pas
    celles de `auth`. Pour inspecter les groupes eux-memes, utilisez un
    compte `createsuperuser`.

### D. Verification en base (sans passer par le navigateur)

Utile pour verifier rapidement un calcul sans cliquer partout :

```bash
python manage.py shell -c "
from products.models import Produit, Vente
for p in Produit.objects.all():
    print(p.nom, p.stock, 'rupture' if p.en_rupture else ('faible' if p.stock_faible else 'ok'))
for v in Vente.objects.all():
    print(v.numero_facture, v.client, v.statut, v.total, v.nb_articles)
"
```

## 5. Reproduire le protocole sans navigateur (`curl`)

Pratique pour un script de verification automatisable, ou pour montrer
aux eleves ce qu'un navigateur fait "sous le capot" (cookies de
session, jeton CSRF) :

```bash
# 1) recuperer un cookie de session + le jeton CSRF du formulaire de connexion
CSRF=$(curl -s -c cookies.txt http://127.0.0.1:8000/connexion/ \
  | grep -oP 'name="csrfmiddlewaretoken" value="\K[^"]*')

# 2) se connecter (le jeton CSRF doit accompagner le POST)
curl -s -b cookies.txt -c cookies.txt \
  -d "csrfmiddlewaretoken=$CSRF&username=vendeur&password=pharmacie123" \
  --referer http://127.0.0.1:8000/connexion/ \
  http://127.0.0.1:8000/connexion/ -o /dev/null -w "%{http_code}\n"

# 3) verifier l'acces refuse sur une page reservee au gerant
curl -s -o /dev/null -w "%{http_code}\n" -b cookies.txt \
  http://127.0.0.1:8000/fournisseurs/          # -> 302 (redirection)
```

Codes HTTP a retenir pendant la demonstration : **200** (ok), **302**
(redirection — pas connecte, ou role insuffisant sur une page
`@gerant_required`), **403** (connecte mais permission Django refusee
sur une action precise), **404** (URL inexistante).

## 6. Ce qui n'est volontairement pas teste ici

`products/tests.py` reste vide : ecrire des `TestCase` automatises
pour ce protocole (par exemple pour la verification "stock
insuffisant" de l'etape 7) est un exercice a part entiere, voir
[module 09](09-aller-plus-loin.md). Ce document couvre le test
*manuel* ; les tests *automatises* restent a ecrire par les eleves.

## 7. Points a ne jamais oublier en classe

- **Ne jamais versionner `db.sqlite3`** : chaque poste doit pouvoir le
  regenerer via `migrate` + `loaddata demo` (section 2). C'est deja
  dans `.gitignore`, mais rappelez pourquoi : une base de donnees est
  un etat local, pas du code source.
- **`setup_auth` est idempotent** : le relancer ne duplique jamais les
  comptes ni les groupes (`get_or_create` partout, voir
  [module 10](10-authentification-et-permissions.md)). Pas besoin de
  le proteger d'un double lancement accidentel.
- **Ce dossier `projetfinaliser/` est le corrige** : il ne doit
  exister que sur la branche `gestion-pharmacie-final`. Le squelette a
  distribuer aux eleves, c'est `GestionPharmacie/`.
