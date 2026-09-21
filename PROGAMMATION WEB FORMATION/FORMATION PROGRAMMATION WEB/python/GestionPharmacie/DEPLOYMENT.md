# Guide de déploiement — GestionPharmacie

Ce document explique comment le projet passe d'un environnement de **développement local** à un environnement de **production**, et détaille les étapes pour le déployer sur **Render**. Il est écrit pour être suivi en formation : chaque brique ajoutée est expliquée avec son rôle, pas seulement la commande à taper.

> Précision : les principes appliqués ici (variables d'environnement, Postgres, fichiers statiques, serveur WSGI) sont ceux de tout hébergeur "12-factor" — Heroku, Render, Railway, Northflank fonctionnent tous sur le même modèle. Le projet a d'abord été préparé en visant Northflank puis le déploiement a finalement été fait sur Render ; l'essentiel de la configuration (`settings.py`, `requirements.txt`, `Procfile`) ne change pas d'un hébergeur à l'autre, seule la section 6 ci-dessous est spécifique à Render.

## 1. Ce qui a changé depuis la version « cours » du projet

Avant cette session, `GestionPharmacie` était un projet Django classique de formation : modèles, vues, gabarits, avec une configuration codée en dur (`SECRET_KEY` en clair dans `settings.py`, pas de `.env`, pas de serveur de production) et plusieurs fichiers/fonctionnalités manquants ou cassés. Cette section liste tout ce qui a changé, par thème, pour que vous sachiez exactement ce qui a été touché avant de merger `feature-dev` dans `main`.

### 1.1 Fichiers qui manquaient purement et simplement

Sans eux, un clone frais du dépôt ne pouvait pas fonctionner :

- **`products/forms.py`** — n'existait pas : aucun formulaire (`ProduitForm`, `ClientForm`, `FournisseurForm`, `VenteForm`, `LigneVenteFormSet`...) n'était disponible, donc les pages de création/édition plantaient.
- **`products/migrations/0001_initial.py`, `0002_...py`, `0003_...py`** — absentes, donc `python manage.py migrate` ne créait aucune table sur un clone neuf.
- **`requirements.txt`, `Procfile`, `.env.example`** — n'existaient pas avant la mise en production (voir section 3).

### 1.2 Bugs corrigés (l'application plantait ou ne faisait pas ce qu'elle devait)

Dans `products/forms.py`, `products/models.py` et `products/views.py` :

- `produits_delete` redirigeait vers un nom d'URL inexistant (`produit_liste` au lieu de `produits_liste`) → `NoReverseMatch` systématique.
- `VenteForm.__init__` était orthographié `__int__` → le champ "Client de passage" restait mort, jamais initialisé.
- `LigneVenteForm.clean()` appelait `super().clean` sans les parenthèses → plantage garanti à la validation d'une ligne de vente.
- `LigneVenteForm.Meta.model` était écrit comme une annotation de type (`model: LigneVente`) au lieu d'une affectation (`model = LigneVente`).
- `ClientForm` référençait un widget pour un champ `notes` qui n'existe pas sur le modèle (le champ s'appelle `note`).
- Le formset de ligne de vente (`BaseLigneVenteFormSet`) acceptait de valider une vente sans aucune ligne remplie.
- `Vente.Statut.EN_ENTENTE` / `ANNULERR` étaient des fautes de frappe, corrigées en `EN_ATTENTE` / `ANNULEE` ; la propriété de couleur du badge (`status_css`) ne correspondait ni au bon statut ni au nom attendu par les gabarits (`statut_css`) → le badge de statut ne s'affichait jamais.
- `ventes_form` était un stub sans traitement du formulaire : il était **impossible d'enregistrer une vente**. Implémentation complète avec `VenteForm` + `LigneVenteFormSet` et décrément du stock à la validation.

### 1.3 Sécurité durcie

- Ajout de `@permission_required` sur les 3 vues de suppression (produit/client/fournisseur) : avant, seul `@login_required` les protégeait, donc n'importe quel utilisateur connecté pouvait supprimer en postant directement sur l'URL.
- Ajout de `@login_required` manquant sur `factures_detail`, `statistiques`, `notifications`, `parametres`.
- La vue de connexion respecte désormais `?next=` au lieu de rediriger systématiquement vers l'accueil.

### 1.4 Interface et routes

- Enregistrement de tous les modèles (`Categorie`, `Fournisseur`, `Client`, `Produit`, `Vente`) dans Django admin (`products/admin.py`), avec listes, filtres et recherche.
- Ajout des routes manquantes : modifier/supprimer par module (produits, clients, fournisseurs), déconnexion.
- Gabarits HTML/CSS pour le CRUD complet (produits, clients, fournisseurs, ventes, factures), sidebar responsive avec tiroir mobile.

### 1.5 Nettoyage du dépôt

- Le dossier `env/` (environnement virtuel Python, ~6500 fichiers, binaires et `site-packages`) était suivi par erreur dans Git depuis un ancien commit, alourdissant considérablement le dépôt. Il a été retiré du suivi (les fichiers restent sur le disque) et remplacé par `requirements.txt`, qui liste les vraies dépendances.
- Suppression du dossier `test_template/`, qui ne servait plus.

### 1.6 Passage en configuration « prête pour la production »

Détaillé en section 3, mais en résumé : `SECRET_KEY`/`DEBUG`/`ALLOWED_HOSTS`/`DATABASE_URL` sont passés d'un codage en dur dans `settings.py` (dont une `SECRET_KEY` commitée en clair) à une lecture depuis l'environnement via `django-environ`, avec bascule automatique sur SQLite en local si `DATABASE_URL` est absente.

### 1.7 Choix final de l'hébergeur : Render

La configuration a d'abord été pensée pour Northflank, puis le déploiement a finalement été fait sur **Render**. Deux ajustements ont été nécessaires pour que ça fonctionne correctement sur Render (détails en section 6) :

- Le `Procfile` ne précisait pas de port d'écoute pour `gunicorn` (il retombait sur `127.0.0.1:8000` par défaut) ; Render assigne dynamiquement un port via la variable `$PORT` et exige que l'application écoute sur `0.0.0.0`. Le `Procfile` lance désormais `gunicorn ... --bind 0.0.0.0:${PORT:-8000}`.
- Ajout de `RENDER_EXTERNAL_HOSTNAME` dans `settings.py` : Render expose automatiquement le nom de domaine du service dans cette variable, qui est ajoutée à `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` sans avoir à la recopier à la main dans les variables d'environnement.

## 2. Le principe général : un seul code, deux configurations

La règle d'or d'une application prête pour la production est de **ne jamais coder en dur** la configuration (mots de passe, adresses autorisées, base de données). Tout passe par des **variables d'environnement**, lues au démarrage.

```
Code Django (identique partout)
        │
        ├── en local   → lit le fichier .env (non versionné)
        └── en prod    → lit les variables définies sur Render
```

C'est ce que fait [GestionPharmacie/settings.py](GestionPharmacie/settings.py) via le paquet `django-environ` :

```python
env = environ.Env(DEBUG=(bool, False))
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(str(env_file))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
```

En local, le fichier `.env` existe et fournit les valeurs. En production, il n'y a pas de fichier `.env` : Render injecte les variables directement dans l'environnement du conteneur, et `django-environ` les lit exactement de la même façon.

### Variables utilisées par le projet

| Variable | Rôle | Valeur typique en local | Valeur typique en production |
|---|---|---|---|
| `SECRET_KEY` | Clé de signature Django (sessions, tokens CSRF, réinitialisation de mot de passe) | une valeur de test | une valeur longue et aléatoire, **différente**, jamais commitée |
| `DEBUG` | Active les pages d'erreur détaillées et désactive les protections strictes | `True` | `False` |
| `ALLOWED_HOSTS` | Liste blanche des domaines autorisés à servir l'app (anti "Host header attack") | `127.0.0.1,localhost` | `votre-service.onrender.com` (+ domaine perso éventuel) — complétée automatiquement par `RENDER_EXTERNAL_HOSTNAME` (voir 1.7) |
| `CSRF_TRUSTED_ORIGINS` | Origines HTTPS de confiance pour valider les formulaires (POST) | vide | `https://votre-service.onrender.com` |
| `DATABASE_URL` | Chaîne de connexion à la base de données | absente → bascule sur SQLite (`db.sqlite3`) | fournie par la base PostgreSQL Render |
| `EMAIL_BACKEND` | Où partent les emails envoyés par Django | `django.core.mail.backends.console.EmailBackend` (affiché dans le terminal) | backend SMTP réel si besoin |

Le fichier [.env.example](.env.example) sert de modèle : il montre **quelles variables sont attendues** sans révéler de vraies valeurs. C'est lui qui est versionné dans Git ; `.env` (les vraies valeurs) est ignoré par [.gitignore](.gitignore) et ne doit **jamais** être commité.

### Le bloc de sécurité conditionnel

Toujours dans `settings.py` :

```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    X_FRAME_OPTIONS = 'DENY'
```

Ces réglages (redirection HTTPS forcée, cookies sécurisés, HSTS) ne s'activent **que si `DEBUG=False`**. En local, on travaille en HTTP simple sans certificat, donc les activer casserait le développement — d'où la séparation.

## 3. Les briques ajoutées pour la production

| Paquet ([requirements.txt](requirements.txt)) | Rôle |
|---|---|
| `django-environ` | Lit `.env` en local et les variables d'environnement en production ; sépare la config du code. |
| `gunicorn` | Serveur WSGI de production. `manage.py runserver` n'est pas conçu pour tenir une charge réelle — `gunicorn` le remplace en prod. |
| `whitenoise` | Sert les fichiers CSS/JS/images de l'admin directement depuis l'application, sans avoir besoin d'un serveur web séparé (nginx, CDN). |
| `psycopg[binary]` | Pilote PostgreSQL pour Django (nécessaire dès que `DATABASE_URL` pointe vers Postgres). |
| `Pillow` | Traitement des images (utilisé par le champ `image` du modèle produit). |

### WhiteNoise et les fichiers statiques

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
```

`CompressedManifestStaticFilesStorage` compresse (gzip/brotli) chaque fichier statique et lui donne un nom unique basé sur son contenu (cache busting), pour que les navigateurs puissent les mettre en cache très longtemps sans risquer de servir une vieille version après une mise à jour.

### Le `Procfile`

```
web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn GestionPharmacie.wsgi:application --bind 0.0.0.0:${PORT:-8000} --log-file -
```

C'est la commande exécutée à chaque démarrage du conteneur en production :

1. `migrate --noinput` : applique les migrations en attente sur la base de données à chaque déploiement.
2. `collectstatic --noinput` : rassemble tous les fichiers statiques dans `staticfiles/` pour que WhiteNoise puisse les servir.
3. `gunicorn ... --bind 0.0.0.0:${PORT:-8000} --log-file -` : démarre le serveur applicatif. Render assigne dynamiquement le port d'écoute via la variable `$PORT` et route le trafic public vers `0.0.0.0` — sans ce `--bind` explicite, gunicorn écoute par défaut sur `127.0.0.1:8000`, injoignable depuis l'extérieur du conteneur. `${PORT:-8000}` retombe sur `8000` si `$PORT` n'est pas définie (utile en local). `--log-file -` envoie les logs vers la sortie standard, que Render capture et affiche dans son interface.

## 4. Développement en local (rappel pour les élèves)

```bash
python3 -m venv env
source env/bin/activate          # Windows : env\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# puis éditer .env :
#   SECRET_KEY=<n'importe quelle chaîne pour le local>
#   DEBUG=True
#   ALLOWED_HOSTS=127.0.0.1,localhost

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Sans `DATABASE_URL` dans `.env`, l'application bascule automatiquement sur SQLite (`db.sqlite3`), c'est voulu pour simplifier le développement.

## 5. Comment tester le projet

### Tests automatisés

`products/tests.py` est aujourd'hui un fichier vide (stub généré par `startapp`) : il n'y a pas encore de suite de tests automatisés. `python manage.py test` fonctionne (il ne trouvera simplement aucun test à exécuter) — c'est un axe d'amélioration naturel du projet, mais en attendant, la checklist manuelle ci-dessous couvre les parcours qui ont été corrigés ou ajoutés pendant cette session.

### Checklist manuelle de bout en bout

À faire en local (`python manage.py runserver`), avec un compte superutilisateur (`python manage.py createsuperuser`) et, idéalement, un second compte utilisateur **sans** les permissions de suppression pour tester les autorisations :

1. **Connexion**
   - [ ] Se connecter sur `/connexion/` : redirection vers l'accueil.
   - [ ] Accéder à une page protégée sans être connecté (ex. `/produits/`) : redirection vers `/connexion/?next=/produits/`, puis retour sur `/produits/` après connexion (et non l'accueil).
   - [ ] Se déconnecter via `/deconnexion/`.

2. **Produits**
   - [ ] Créer un produit (`/produits/ajouter/`), le modifier (`/produits/<id>/modifier`), vérifier qu'il apparaît dans `/produits/` et dans `/stock/`.
   - [ ] Le supprimer en étant superutilisateur : ça fonctionne et redirige correctement vers `/produits/` (plus de `NoReverseMatch`).
   - [ ] Tenter de supprimer un produit avec le compte sans permission : doit renvoyer un `403 Forbidden`, pas une suppression silencieuse.

3. **Clients / Fournisseurs**
   - [ ] Créer/modifier un client, y compris le champ note (vérifier que le formulaire n'erreure plus sur un widget `notes` inexistant).
   - [ ] Créer/modifier/supprimer un fournisseur ; vérifier que le bouton de suppression est bien masqué/désactivé pour un utilisateur sans permission.

4. **Ventes** (le parcours le plus fragile avant les corrections)
   - [ ] Créer une vente avec un client existant, puis avec « Client de passage » : le libellé doit bien s'afficher et fonctionner (bug `__int__`/`__init__` corrigé).
   - [ ] Ajouter une ou plusieurs lignes de vente et valider : le stock du produit doit être décrémenté du montant vendu.
   - [ ] Essayer de valider une vente **sans aucune ligne remplie** : doit être rejetée avec un message d'erreur, pas acceptée.
   - [ ] Essayer de vendre une quantité supérieure au stock disponible : doit être rejetée.
   - [ ] Vérifier que le badge de statut de la vente affiche la bonne couleur pour chaque statut (`EN_ATTENTE`, `ANNULEE`, etc. — plus les anciennes fautes de frappe `EN_ENTENTE`/`ANNULERR`).

5. **Factures et pages protégées**
   - [ ] Ouvrir `/factures/` puis le détail d'une facture (`/factures/<id>/`) : accessible uniquement connecté.
   - [ ] Vérifier que `/statistiques/`, `/notifications/` et `/parametres/` redirigent vers la connexion si on n'est pas authentifié.

6. **Admin Django**
   - [ ] Se connecter sur `/admin/` avec le superutilisateur et vérifier que `Categorie`, `Fournisseur`, `Client`, `Produit`, `Vente` (avec ses lignes en inline) sont bien enregistrés, listés, filtrables et cherchables.

7. **Configuration production (avant de déployer)**
   - [ ] Passer `DEBUG=False` dans `.env` local et lancer `python manage.py check --deploy` : ne doit remonter aucune alerte bloquante.
   - [ ] Lancer `python manage.py collectstatic --noinput` : doit se terminer sans erreur et remplir `staticfiles/`.
   - [ ] Remettre `DEBUG=True` ensuite pour reprendre le développement normalement.

## 6. Déploiement sur Render

### Point d'attention important : dépôt monorepo

Ce projet Django n'est **pas à la racine** du dépôt GitHub `FORMATION-PYTHON-DJANGO` : il se trouve dans le sous-dossier

```
PROGAMMATION WEB FORMATION/FORMATION PROGRAMMATION WEB/python/GestionPharmacie/
```

Render doit savoir chercher `requirements.txt`, `Procfile` et `manage.py` dans ce sous-dossier, pas à la racine du dépôt. Lors de la création du service, renseignez ce chemin dans le champ **Root Directory**. Sans ça, le build échoue en ne trouvant pas `requirements.txt`.

### Étape 1 — Créer une base PostgreSQL

1. Dans le dashboard Render, **New + → PostgreSQL**.
2. Donner un nom (ex. `gestionpharmacie-db`), choisir une région et le plan **Free** (suffisant pour un projet pédagogique).
3. Une fois créée, Render affiche une **Internal Database URL** et une **External Database URL**. L'interne est plus rapide et ne consomme pas de quota externe : c'est celle à utiliser si le service web est dans la même région Render, ce qui est le cas ici.

### Étape 2 — Remplir le formulaire « New Web Service »

Render affiche un unique formulaire (Source Code → Name → Root Directory → Build/Start Command → Compute → Environment Variables) qui crée et déploie le service en une fois. Valeur exacte à mettre dans chaque champ :

| Champ du formulaire | Valeur à saisir | Pourquoi |
|---|---|---|
| **Source Code** | dépôt GitHub `GUELORD-MWENDERWA/FORMATION-PYTHON-DJANGO` | déjà le bon dépôt si Render l'a détecté automatiquement |
| **Name** | `gestionpharmacie` (ou un nom de votre choix) | devient l'URL publique : `<name>.onrender.com`. Le nom pré-rempli `FORMATION-PYTHON-DJANGO` fonctionne aussi mais donne une URL moins lisible |
| **Project** | `gestion-pharmacie` | déjà correctement présélectionné |
| **Environment** | `Production` | valeur par défaut, à garder |
| **Language** | `Python 3` | déjà correct |
| **Branch** | `main` | déjà à jour : `feature-dev` y a été fusionné avec tout le travail de cette session |
| **Region** | à votre choix (ex. `Virginia (US East)`), **mais retenez-la** | la base PostgreSQL de l'étape 1 doit être créée **dans la même région** pour pouvoir utiliser l'Internal Database URL (plus rapide, pas de quota externe) |
| **Root Directory** | `PROGAMMATION WEB FORMATION/FORMATION PROGRAMMATION WEB/python/GestionPharmacie` | **champ le plus important** : le dépôt GitHub a deux dossiers imbriqués avant d'arriver au projet Django (`PROGAMMATION WEB FORMATION/` puis `FORMATION PROGRAMMATION WEB/`, orthographes différentes — copier-coller exactement cette valeur, sans quoi le build ne trouve pas `requirements.txt`) |
| **Build Command** | `pip install -r requirements.txt` | remplace le texte pré-rempli |
| **Start Command** | `python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn GestionPharmacie.wsgi:application --bind 0.0.0.0:$PORT --log-file -` | remplace le `gunicorn your_application.wsgi` pré-rempli ; c'est le même contenu que le [Procfile](Procfile), mais le préciser explicitement ici est plus fiable que de compter sur la détection automatique du `Procfile` dans un sous-dossier de monorepo |
| **Compute** | `Free` pour tester (0.1 CPU / 512 Mo, déjà sélectionné) | voir les limites (pas de Shell, pas de disque persistant, mise en veille) détaillées plus bas ; passer sur un plan payant pour un usage réel |

Dans la section **Environment Variables** du même formulaire, ajouter :

| Key | Value |
|---|---|
| `SECRET_KEY` | cliquer sur **Generate** (Render génère une valeur aléatoire sûre) — sinon utiliser `python -c "import secrets; print(secrets.token_urlsafe(50))"` en local et coller le résultat |
| `DEBUG` | `False` |
| `DATABASE_URL` | l'**Internal Database URL** de la base PostgreSQL créée à l'étape 1 (si l'étape 1 n'est pas encore faite, la créer d'abord dans la **même région**, puis revenir copier l'URL ici) |

`ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` **n'ont pas besoin d'être ajoutées ici** : Render expose automatiquement le domaine du service dans `RENDER_EXTERNAL_HOSTNAME`, que `settings.py` ajoute lui-même à ces deux listes (voir section 1.7). Ne les rajoutez que si vous branchez un domaine personnalisé en plus du sous-domaine `onrender.com`.

Cliquer sur **Deploy Web Service** en bas du formulaire pour lancer la création et le premier déploiement.

### Étape 3 — Suivre le déploiement

Render fournit une URL du type `gestionpharmacie.onrender.com` et redéploie automatiquement à chaque `git push` sur la branche `main`. La **Start Command** s'exécute à chaque démarrage : migrations, `collectstatic`, puis lancement de `gunicorn`. Suivre l'onglet **Logs** pour vérifier qu'il n'y a pas d'erreur (une erreur fréquente au premier essai : `DisallowedHost`, voir la section Dépannage).

### Étape 4 — Créer un compte administrateur

Le formulaire `createsuperuser` interactif a besoin d'un terminal, ce qui dépend du plan Render :

- **Plan payant (Starter et plus)** : onglet **Shell** du service dans le dashboard Render, puis `python manage.py createsuperuser`.
- **Plan Free (pas d'accès Shell)** : lancer la commande **depuis votre machine locale**, en pointant temporairement sur la base de production via son **External Database URL** :
  ```bash
  DATABASE_URL="<external-database-url-de-render>" python manage.py createsuperuser
  ```
  Cela crée directement le compte dans la base Postgres de production sans avoir besoin d'un shell sur le serveur.

### Point d'attention : les images produits ne sont pas persistantes par défaut

Le modèle produit stocke une image (`media/produits/...`, voir [products/models.py](products/models.py)). Un service Render est **éphémère** : à chaque redéploiement ou redémarrage, tout ce qui a été écrit sur le disque (donc les images téléversées via l'admin ou le formulaire) est perdu, sauf si un **disque persistant** est attaché.

Render propose des **Persistent Disks**, mais uniquement sur les plans payants (pas sur le plan Free) : attacher un disque monté sur le dossier `media/` du service réglerait le problème pour ce projet pédagogique. Pour un usage plus sérieux, on migrerait vers un stockage objet externe (S3-compatible, ex. Cloudflare R2) via `django-storages` — bonne discussion à avoir avec les élèves sur la différence entre disque local et stockage persistant dans le cloud.

### Point d'attention : mise en veille du plan Free

Sur le plan **Free**, Render met le service en veille après ~15 minutes sans requête entrante, et la requête suivante déclenche un redémarrage à froid qui peut prendre 30 à 60 secondes avant que la page réponde. C'est normal pour un projet de formation, mais bon à savoir avant une démonstration en direct (accéder à l'URL quelques minutes avant pour "réveiller" le service).

## 7. Checklist avant chaque mise en production

- [ ] `SECRET_KEY` de production différente de celle utilisée en local, jamais commitée.
- [ ] `DEBUG=False` en production.
- [ ] `RENDER_EXTERNAL_HOSTNAME` est bien renseignée par Render (automatique) ; si un domaine personnalisé est utilisé en plus, l'ajouter à `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` (avec `https://` pour ce dernier).
- [ ] `DATABASE_URL` pointe vers la base PostgreSQL Render, pas vers SQLite.
- [ ] Disque persistant attaché (plan payant) si des images/fichiers sont téléversés en prod.
- [ ] `.env` n'est jamais poussé sur GitHub (vérifier avec `git status`/`git check-ignore -v .env`).

## 8. Dépannage courant

| Symptôme | Cause probable | Solution |
|---|---|---|
| `DisallowedHost at /` | `RENDER_EXTERNAL_HOSTNAME` pas encore lue (ancien déploiement) ou domaine personnalisé non ajouté | Redéployer après la mise à jour de `settings.py` ; ajouter le domaine perso à `ALLOWED_HOSTS` si besoin |
| `CSRF verification failed` sur un formulaire | `CSRF_TRUSTED_ORIGINS` manquant ou sans `https://` (cas d'un domaine perso) | Ajouter `https://<domaine>` dans `CSRF_TRUSTED_ORIGINS` |
| `Bad Gateway` / le service ne répond jamais | `gunicorn` n'écoute pas sur `0.0.0.0:$PORT` | Vérifier que la Start Command inclut bien `--bind 0.0.0.0:$PORT` |
| CSS/JS de l'admin absents (page blanche/moche) | `collectstatic` non exécuté ou `STATIC_ROOT` absent | Vérifier que la Start Command s'exécute bien en entier dans les logs de déploiement |
| Erreur de connexion à la base au démarrage | `DATABASE_URL` absente ou mauvaise URL (interne vs externe) | Vérifier la variable dans l'onglet Environment ; utiliser l'Internal Database URL si le service web est dans la même région |
| Images produits disparues après un redéploiement | Pas de disque persistant sur `media/` (plan Free) | Passer sur un plan payant et attacher un disque Render monté sur `media/`, ou migrer vers un stockage S3-compatible |
| Le build échoue en cherchant `requirements.txt` | Mauvais *Root Directory* (dépôt monorepo) | Renseigner le sous-dossier exact du projet dans les réglages du service |
| Le service met du temps à répondre après une période d'inactivité | Mise en veille du plan Free | Normal (voir section 6) ; passer sur un plan payant pour éviter la mise en veille |
