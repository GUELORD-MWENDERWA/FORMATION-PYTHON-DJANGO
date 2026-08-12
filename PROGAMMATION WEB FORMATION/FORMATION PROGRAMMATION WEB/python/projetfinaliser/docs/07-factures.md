# 07 — Factures (vue lecture seule d'une vente)

Fichiers concernes : `products/views.py` (`factures_liste`,
`factures_detail`), `factures/liste.html`, `factures/detail.html`

## Objectif du module

Comprendre qu'**une facture n'est pas un nouveau modele** : c'est une
`Vente` (module 06) presentee differemment, pour un usage different
(document a montrer/imprimer au client) que la page Ventes (journal
interne des transactions). Beaucoup d'eleves s'attendent a devoir
creer un modele `Facture` — c'est l'occasion de montrer qu'on modelise
les *donnees*, pas les *pages*.

## Deux libelles, un seul modele

```python
@property
def numero(self):
    return f"#{self.pk}"

@property
def numero_facture(self):
    annee = self.date.year if self.date else "----"
    return f"F-{annee}-{self.pk}"
```

La page Ventes affiche `vente.numero` (`#12`), la page Factures
affiche `vente.numero_facture` (`F-2026-12`) — les deux proprietes
lisent le meme `pk`, juste formate differemment selon le contexte
d'affichage.

## Les vues sont presque identiques a une liste/detail classique

```python
def factures_liste(request):
    ventes = Vente.objects.select_related('client').prefetch_related('lignes')
    return render(request, 'factures/liste.html', {'ventes': ventes})

def factures_detail(request, pk):
    vente = get_object_or_404(
        Vente.objects.select_related('client').prefetch_related('lignes__produit'),
        pk=pk,
    )
    return render(request, 'factures/detail.html', {'vente': vente})
```

`select_related('client')` fonctionne comme au module 03
(`select_related('categorie')`) : une jointure SQL pour eviter une
requete separee par vente quand le template affiche
`vente.client`.

`prefetch_related('lignes__produit')` est different : `lignes` est le
cote "plusieurs" d'une relation (une vente a plusieurs lignes), donc
une jointure classique ne suffit pas — Django fait une deuxieme
requete separee pour precharger toutes les lignes (et, via
`__produit`, leurs produits) d'un coup, plutot qu'une requete par
ligne quand le template boucle avec `{% for ligne in vente.lignes.all %}`.
Retenez la regle simple : `select_related` pour du "un seul" (une
`ForeignKey` vue depuis le cote qui la porte), `prefetch_related` pour
du "plusieurs" (une relation inverse ou une liste).

## Le detail : `{% for ligne in vente.lignes.all %}`

```django
{% for ligne in vente.lignes.all %}
<div class="data-row">
  <div class="data-cell grow">{{ ligne.produit }}</div>
  <div class="data-cell shrink">{{ ligne.quantite }}</div>
  <div class="data-cell">{{ ligne.prix_unitaire }} €</div>
  <div class="data-cell">{{ ligne.total }} €</div>
</div>
{% endfor %}

<div class="invoice-totals">
  <div class="cart-total-row"><span>Sous-total</span><span>{{ vente.sous_total }} €</span></div>
  <div class="cart-total-row"><span>Remise</span><span>{{ vente.remise }} €</span></div>
  <div class="cart-total-row grand-total"><span>Total</span><span>{{ vente.total }} €</span></div>
</div>
```

`ligne.total`, `vente.sous_total` et `vente.total` sont les
`@property` definies au module 01 :

```python
@property                                          # sur LigneVente
def total(self):
    return self.quantite * self.prix_unitaire

@property                                          # sur Vente
def sous_total(self):
    return sum((ligne.total for ligne in self.lignes.all()), start=0)

@property
def total(self):
    return self.sous_total - self.remise
```

Aucun total n'est stocke en base : tout est recalcule a l'affichage a
partir des lignes reelles. Avantage direct pour les eleves : il est
impossible d'avoir une facture dont le total affiche ne correspond
plus a la somme de ses lignes (un bug classique quand on stocke un
total en dur et qu'on oublie de le recalculer apres une modification).

## Le bouton Imprimer

```django
<button type="button" class="btn btn-primary" onclick="window.print()">Imprimer</button>
```

`window.print()` ouvre la boite de dialogue d'impression du
navigateur. La mise en forme "papier" (masquer la sidebar, la barre
mobile, les boutons d'action) est deja geree par la regle
`@media print` presente dans `style.css` depuis le mockup d'origine —
rien a faire de plus cote CSS.

## Testez

1. `/factures/` doit lister les memes ventes que `/ventes/`, avec un
   numero au format `F-2026-N` et le meme total.
2. Cliquez sur un numero de facture : la page de detail doit afficher
   le bon client (ou "Client de passage"), les bonnes lignes de
   produits, et un total coherent avec le sous-total moins la remise.
3. Cliquez "Imprimer" : la boite de dialogue d'impression du
   navigateur doit s'ouvrir, sans la sidebar ni les boutons d'action
   dans l'apercu.

Passez au [module 08](08-messages-et-erreurs.md).
