# 04 — Stock (reutiliser un modele existant)

Fichiers concernes : [`products/views.py`](../products/views.py)
(fonction `stock_liste`), [`stock/liste.html`](../products/templates/stock/liste.html),
[`products/models.py`](../products/models.py) (proprietes `en_rupture`,
`stock_faible`, `peremption_proche`)

## Objectif du module

Ce module est volontairement court : c'est l'occasion d'expliquer
qu'**une page n'a pas toujours besoin d'un nouveau modele**. La page
Stock affiche exactement les memes produits que la page Produits,
juste avec des colonnes et un calcul de statut differents.

## La vue

```python
def stock_liste(request):
    produits = Produit.objects.all()
    return render(request, 'stock/liste.html', {'produits': produits})
```

Aucune nouveaute cote vue — c'est le meme `Produit.objects` que dans
`produits_liste` (module 03), juste sans les colonnes "ventes"/"prix"
qui ne concernent pas cette page.

## Les trois proprietes calculees

Ajoutees dans `models.py` au module 01, elles prennent tout leur sens
ici, ou on les combine dans le template pour determiner le statut
affiche :

```python
@property
def en_rupture(self):
    return self.stock == 0

@property
def stock_faible(self):
    return 0 < self.stock <= self.seuil_alerte

@property
def peremption_proche(self):
    if not self.date_peremption:
        return False
    return self.date_peremption <= timezone.localdate() + timedelta(days=30)
```

Et dans le template, un `{% if %}` en cascade choisit le premier cas
qui s'applique (l'ordre compte : un produit en rupture reste "Rupture"
meme si sa date de peremption est aussi proche) :

```django
{% if produit.en_rupture %}
  <span class="status disabled">Rupture</span>
{% elif produit.peremption_proche %}
  <span class="status danger">Peremption proche</span>
{% elif produit.stock_faible %}
  <span class="status warning">Stock faible</span>
{% else %}
  <span class="status active">En stock</span>
{% endif %}
```

**Pourquoi une `@property` sur le modele plutot qu'un `{% if %}`
directement dans le template avec `produit.stock <= produit.seuil_alerte`
?** Parce que cette regle metier ("qu'est-ce qu'un stock faible ?")
doit rester definie a un seul endroit. Si demain elle change (par
exemple, un stock faible devient "moins de 20% du seuil" au lieu de
"inferieur ou egal au seuil"), on modifie une seule ligne dans
`models.py` et toutes les pages qui l'utilisent (aujourd'hui juste
Stock, mais Produits l'utilise aussi pour sa pastille "Faible") se
mettent a jour automatiquement.

## Testez

`/stock/` doit afficher les 6 produits de la fixture avec des statuts
varies : Doliprane et Creme hydratante "En stock", Amoxicilline
"Peremption proche" (sa date est a moins de 30 jours), Gel
hydroalcoolique et Tensiometre "Stock faible", Paracetamol "Rupture".
Si vous voyez ces 4 statuts differents representes, le calcul est
correct.

> **Note** : la fixture `demo.json` fixe la date de peremption
> d'Amoxicilline a une date proche du jour ou cette demo a ete
> preparee (aout 2026). Si vous rechargez ces donnees bien plus tard,
> `peremption_proche` peut ne plus etre vrai (elle compare toujours a
> `timezone.localdate()`, la date reelle du jour) — ce n'est pas un
> bug, juste la limite d'un jeu de donnees fige dans le temps.

Passez au [module 05](05-clients-fournisseurs.md).
