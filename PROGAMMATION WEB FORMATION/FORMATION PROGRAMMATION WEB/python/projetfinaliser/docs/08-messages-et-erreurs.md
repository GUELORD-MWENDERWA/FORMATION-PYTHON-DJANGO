# 08 — Messages et erreurs de formulaire

Fichiers concernes : [`products/templates/partials/messages.html`](../products/templates/partials/messages.html),
[`products/templates/base.html`](../products/templates/base.html),
[`products/static/css/style.css`](../products/static/css/style.css)
(classes `.app-message`, `.form-errors`, `.field-error`)

## Objectif du module

Relier deux mecanismes utilises depuis le module 03 mais jamais
expliques jusqu'ici : le *framework messages* de Django
(`messages.success(...)`) et l'affichage des erreurs de validation
d'un formulaire. Sans ce module, les redirections apres un
enregistrement seraient muettes, et une erreur de saisie ne serait
visible que dans les logs du serveur.

## Le framework messages

Chaque vue de creation/modification/suppression appelle, avant de
rediriger :

```python
messages.success(request, "Produit enregistre.")
return redirect('produits_liste')
```

Les messages Django ne s'affichent pas dans la reponse qui les cree
(la redirection HTTP ne contient pas de HTML) : ils sont stockes cote
serveur (dans la session ou un cookie) et **consommes une seule fois**
par la requete suivante — celle qui affiche la page de destination
apres la redirection. C'est ce qu'on appelle le pattern
Post/Redirect/Get, et c'est pour ca qu'on redirige toujours apres un
POST reussi plutot que de faire un `render()` direct : ca evite qu'un
rechargement de page (F5) ne renvoie le formulaire une seconde fois.

Le partial charge une seule fois dans `base.html` (donc disponible sur
toutes les pages qui en heritent) :

```django
{% if messages %}
  <div class="app-messages">
    {% for message in messages %}
      <div class="app-message {{ message.tags }}">{{ message }}</div>
    {% endfor %}
  </div>
{% endif %}
```

`message.tags` vaut `"success"`, `"error"`, `"warning"` ou `"info"`
selon la fonction utilisee (`messages.success`, `messages.error`...) —
ces mots correspondent directement aux classes CSS `.app-message.success`,
`.app-message.error`, etc. ajoutees dans `style.css`, qui reprennent
les memes couleurs que les pastilles `.status` deja presentes dans le
mockup d'origine (vert succes, rouge erreur...) pour rester coherent
visuellement.

## Les erreurs de formulaire

Deux niveaux d'erreurs a distinguer, visibles dans tous les
`*/form.html` depuis le module 03 :

**Erreur liee a un champ precis** (ex. "Nom du produit" laisse vide) :

```django
<div class="form-group full-width">
  <label for="{{ form.nom.id_for_label }}">Nom du produit</label>
  {{ form.nom }}
  {% if form.nom.errors %}<span class="field-error">{{ form.nom.errors|join:", " }}</span>{% endif %}
</div>
```

**Erreur globale au formulaire**, qui ne concerne aucun champ en
particulier (ex. "Ajoutez au moins un produit a la vente" au module 06
— aucun champ specifique n'est fautif, c'est l'ensemble qui l'est) :

```django
{% if form.non_field_errors %}
  <div class="form-errors">
    <ul>{% for error in form.non_field_errors %}<li>{{ error }}</li>{% endfor %}</ul>
  </div>
{% endif %}
```

Django alimente automatiquement `form.nom.errors` et
`form.non_field_errors` a partir des `raise forms.ValidationError(...)`
ecrits dans les methodes `clean_nom()` (erreur de champ) ou `clean()`
(erreur globale) d'un formulaire — voir `LigneVenteForm.clean()` au
module 06 pour un exemple concret.

**Point important a faire remarquer** : quand un formulaire est
invalide, la vue ne redirige jamais — elle re-affiche directement le
meme template avec `form` contenant a la fois les erreurs *et* les
valeurs deja saisies par l'utilisateur (`ProduitForm(request.POST,
...)`, pas un formulaire vide). L'utilisateur ne perd donc jamais sa
saisie a cause d'une erreur sur un seul champ.

## Testez

1. Sur `/produits/ajouter/`, laissez "Nom du produit" vide et
   remplissez le reste : apres soumission, seul le champ "Nom" doit
   afficher une erreur, et tous les autres champs doivent garder les
   valeurs que vous aviez saisies.
2. Enregistrez n'importe quel produit/client/fournisseur avec succes :
   un bandeau vert doit apparaitre en haut de la liste de destination,
   puis disparaitre si vous rechargez la page (F5) — preuve qu'il
   n'est affiche qu'une seule fois.

Passez au [module 09](09-aller-plus-loin.md), la derniere etape.
