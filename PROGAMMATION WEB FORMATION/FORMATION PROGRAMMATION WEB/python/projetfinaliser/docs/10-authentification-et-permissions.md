# 10 — Authentification et permissions

Fichiers concernes : [`products/views.py`](../products/views.py)
(fonctions `login`, `logout_view`, `est_gerant`, `gerant_required`),
[`products/urls.py`](../products/urls.py),
[`products/templates/auth/login.html`](../products/templates/auth/login.html),
[`products/templates/partials/sidebar.html`](../products/templates/partials/sidebar.html),
[`products/management/commands/setup_auth.py`](../products/management/commands/setup_auth.py),
[`GestionPharmacie/settings.py`](../GestionPharmacie/settings.py)

## Objectif du module

Jusqu'ici, `auth/login.html` existait visuellement mais n'importe quel
mot de passe "fonctionnait" (rien n'etait verifie), et toutes les
pages etaient accessibles a n'importe qui, connecte ou non. Ce module
branche `django.contrib.auth` pour de vrai et introduit une
distinction que tout developpeur Django doit savoir expliquer :

- **Authentification** : *qui etes-vous ?* — verifier une identite
  (nom d'utilisateur + mot de passe).
- **Autorisation (permissions)** : *qu'avez-vous le droit de faire ?*
  — une fois identifie, certaines pages ou actions restent interdites
  selon le role du compte.

## Authentification : connexion et session

`authenticate()` verifie les identifiants sans rien modifier ; `login()`
demarre la session (un cookie signe cote client, les donnees cote
serveur) qui garde l'utilisateur connecte d'une requete a l'autre :

```python
def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'auth/login.html')
```

`authenticate` renvoie `None` si les identifiants sont faux — pas
d'exception a attraper, juste un test. Le formulaire, lui, redevient
un formulaire Django ordinaire : `method="post"`, `{% csrf_token %}`,
et des champs `name="username"` / `name="password"` que
`request.POST.get(...)` va lire cote vue (module 03 pour ce meme
reflexe sur les autres formulaires).

`logout_view` fait l'inverse en une ligne (`auth_logout(request)`)
puis renvoie vers la connexion.

## Proteger les vues avec `@login_required`

Le decorateur `@login_required` de `django.contrib.auth.decorators`
s'ajoute au-dessus de **toute** vue qui ne doit etre visible qu'une
fois connecte — c'est-a-dire toutes, sauf `login` :

```python
@login_required
def produits_liste(request):
    ...
```

Si `request.user` n'est pas connecte, Django redirige automatiquement
vers `LOGIN_URL` (defini dans `settings.py`) en ajoutant
`?next=/produits/` a l'URL, pour revenir sur la bonne page juste apres
la connexion :

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
```

## Permissions : deux niveaux, deux outils

Une pharmacie distingue en general deux roles : le **Gerant**, qui
gere aussi les fournisseurs et les parametres du logiciel, et le
**Vendeur**, qui traite les ventes au quotidien sans toucher a ces
deux zones. On modelise ca avec deux outils Django complementaires.

### Page reservee a un role : `user_passes_test`

Pour un module entier (Fournisseurs, Parametres), la question est
"ce compte a-t-il le bon *role* ?", pas "cette action precise
est-elle autorisee ?". On s'appuie sur le champ `is_staff`, deja
fourni par le modele `User` de Django, plutot que d'inventer un
nouveau champ :

```python
def est_gerant(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def gerant_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not est_gerant(request.user):
            messages.error(request, "Cette page est reservee aux gerants.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@gerant_required
def fournisseurs_liste(request):
    ...
```

`gerant_required` empile deux verifications : `@login_required`
(la personne est-elle connectee ?) puis le test `est_gerant` (a-t-elle
le bon role ?). Le meme champ `is_staff` est directement lisible cote
template, sans code Python supplementaire, pour cacher les liens que
l'utilisateur ne peut de toute facon pas ouvrir :

```django
{% if request.user.is_staff or request.user.is_superuser %}
  <li>... lien Fournisseurs ...</li>
{% endif %}
```

**Cacher un lien n'est jamais une protection a lui seul** — n'importe
qui peut taper l'URL directement. C'est pour ca que `fournisseurs_liste`
reste protegee par `@gerant_required` cote vue ; le `{% if %}` dans le
template n'est qu'un confort visuel qui evite d'afficher un lien mort.

### Action precise sur un modele : les permissions Django

Pour une action ponctuelle (supprimer un produit) plutot qu'une page
entiere, Django cree automatiquement quatre permissions par modele —
`view_produit`, `add_produit`, `change_produit`, `delete_produit` —
verifiables avec `user.has_perm(...)` ou, plus court, le decorateur
`permission_required` :

```python
@login_required
@permission_required('products.delete_produit', raise_exception=True)
@require_POST
def produits_delete(request, pk):
    ...
```

`raise_exception=True` renvoie une page 403 (accès refuse) plutot que
de rediriger vers la connexion — utile ici puisque la personne *est*
deja connectee, elle n'a simplement pas cette permission precise.
Cote template, `perms.products.delete_produit` (fourni automatiquement
par le context processor `django.contrib.auth.context_processors.auth`,
deja active dans `settings.py`) permet de ne meme pas afficher le
bouton "Supprimer" si le compte n'a pas la permission :

```django
{% if perms.products.delete_produit %}
  <form method="post" action="{% url 'produits_delete' produit.pk %}">...</form>
{% endif %}
```

### Assigner les permissions : groupes et commande de gestion

Assigner une permission a chaque utilisateur un par un ne passe pas a
l'echelle. Django fournit un modele `Group` : un groupe regroupe des
permissions, un utilisateur rejoint un ou plusieurs groupes et herite
de tout ce qu'ils contiennent. `products/management/commands/setup_auth.py`
est une **commande de gestion** personnalisee (comme `migrate` ou
`loaddata`, mais ecrite par nous) qui cree deux groupes et deux
comptes de demonstration :

```bash
python manage.py setup_auth
```

- Groupe **Vendeur** : peut consulter/ajouter/modifier produits,
  clients, ventes — pas les supprimer, pas toucher aux fournisseurs.
- Groupe **Gerant** : toutes les permissions de l'app `products`, plus
  `is_staff=True` (donc acces a Fournisseurs, Parametres, et a
  `/admin/`).
- Comptes crees : `gerant` / `vendeur`, mot de passe `pharmacie123`
  pour les deux — a changer avant toute mise en production reelle.

La commande est re-lancable sans risque (`get_or_create` partout) :
elle met a jour les permissions des groupes si vous modifiez
`VENDEUR_CODENAMES` dans le fichier, sans dupliquer les comptes.

## Testez

1. Ouvrez `/` sans etre connecte : vous devez atterrir sur
   `/connexion/?next=/`.
2. Connectez-vous avec `vendeur` / `pharmacie123` : le menu
   "Fournisseurs" et "Parametres" doivent avoir disparu de la sidebar.
   Essayez quand meme `/fournisseurs/` a la main dans la barre
   d'adresse : vous devez etre renvoye a l'accueil avec un message
   d'erreur.
3. Toujours connecte en `vendeur`, ouvrez `/produits/` : le bouton
   "Supprimer" ne doit plus apparaitre sur aucune ligne. En forçant
   l'URL `/produits/<id>/supprimer/` (formulaire POST), vous devez
   obtenir une page 403.
4. Deconnectez-vous, reconnectez-vous en `gerant` / `pharmacie123` :
   cette fois "Fournisseurs", "Parametres" et le bouton "Supprimer"
   doivent etre visibles et fonctionnels. Le nom affiche en bas de la
   sidebar doit correspondre au compte connecte.
5. `/admin/` : connectez-vous avec un compte `createsuperuser` (pas
   `gerant`, qui n'est pas superutilisateur) et retrouvez les groupes
   "Gerant" / "Vendeur" dans **Authentification et autorisation ›
   Groupes**, avec leurs permissions deja cochees.

C'est la derniere brique du cours principal. Le [module 09](09-aller-plus-loin.md)
reste pertinent pour le reste des exercices (pagination, filtres,
tableau de bord dynamique, export PDF...).
